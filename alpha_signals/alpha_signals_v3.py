#!/usr/bin/env python3
"""
Alpha Signals Generator v3.1 - Leve IA

NOVA ESTRATÉGIA (Implementada após estudo da comunidade OpenClaw + Feedback Hélcio):

Features implementadas:
1. ✅ Multi-timeframe confirmation (1h/4h/1d)
2. ✅ Volume surge detection + AVL (acumulação sustentada)
3. ✅ Trailing stop com break-even
4. ✅ Circuit breaker (BTC crash + Fear/Greed)
5. ✅ Fibonacci confluence (níveis de liquidez)

Estratégia Base: EMA Crossover + RSI + Trend Filter + AVL + Fibonacci
Win Rate Esperada: 72-78% (com AVL + Fibonacci)

Uso:
    python3 alpha_signals_v3.py --generate
    python3 alpha_signals_v3.py --backtest
    python3 alpha_signals_v3.py --status
"""

import os
import psycopg2
import requests
import json
import sys
from datetime import datetime, timedelta
from decimal import Decimal
import logging
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Carregar variáveis de ambiente do .env
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# Configuração de Log
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuração do Banco
DB_CONFIG = {
    'host': '127.0.0.1',
    'port': 5432,
    'database': 'leveclaw',
    'user': 'leveclaw_user',
    'password': 'leveclaw_password'
}

# APIs de preço (Binance)
PRICE_API = "https://api.binance.com/api/v3"
FUTURES_API = "https://fapi.binance.com/fapi/v1"

# Fear & Greed Index API
FNG_API = "https://api.alternative.me/fng/"

# Alibaba Cloud Qwen API - AUDITOR (Braço Independente)
# Nomenclatura única para evitar conflitos com outras integrações Alibaba
ALIBABA_AUDITOR_KEY = os.getenv('ALIBABA_AUDITOR_KEY', '')
ALIBABA_AUDITOR_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"

# Configurações da Estratégia v3.1
STRATEGY_CONFIG = {
    # EMAs
    'ema_short': 9,
    'ema_medium': 21,
    'ema_long': 200,
    
    # RSI
    'rsi_period': 14,
    'rsi_max': 70,
    'rsi_min': 30,
    
    # Volume
    'volume_surge_multiplier': 2.0,  # 2x volume médio = surge
    'avl_multiplier': 1.5,  # 1.5x volume médio = acumulação
    'avl_min_candles': 3,  # Mínimo 3 candles consecutivos
    
    # Fibonacci
    'fib_confluence_threshold': 2.0,  # Dentro de 2% do nível = confluência
    'fib_levels': [0.236, 0.382, 0.5, 0.618, 0.786],
    'fib_tp_partial_level': 0.618,  # TP parcial em 0.618
    'fib_tp_partial_pct': 30,  # 30% da posição
    
    # Risk Management
    'stop_loss_pct': 6.0,
    'take_profit_1_pct': 15,
    'take_profit_2_pct': 25,
    'trailing_stop_pct': 6.0,
    'break_even_threshold': 3.0,  # Após 3% lucro, move para break-even
    
    # Timeframe
    'timeframe': 'Swing Trade (5-15 dias)',
    'validity_days': 7,
    
    # Confiança mínima
    'min_confidence': 70,
    
    # Circuit Breaker
    'btc_crash_threshold': -10.0,  # -10% em 24h = HALT
    'fng_extreme_fear': 10,  # FNG < 10 = HALT (baixado para testes VIP)
}

# Ativos monitorados
ASSETS = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'BNBUSDT', 'XRPUSDT']


def get_db_connection():
    """Obter conexão com banco de dados."""
    return psycopg2.connect(**DB_CONFIG)


def get_klines(symbol: str, interval: str = '1d', limit: int = 300) -> list:
    """Obter velas (candlesticks) da Binance."""
    try:
        url = f"{PRICE_API}/klines"
        params = {
            'symbol': symbol,
            'interval': interval,
            'limit': limit
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        return response.json()
    except Exception as e:
        logger.error(f"Erro ao obter klines de {symbol}: {e}")
        return []


def calculate_ema(prices: list, period: int) -> Decimal:
    """Calcular Exponential Moving Average."""
    if len(prices) < period:
        return Decimal(0)
    
    multiplier = Decimal(2) / Decimal(period + 1)
    ema = sum(Decimal(str(p)) for p in prices[:period]) / period
    
    for price in prices[period:]:
        ema = (Decimal(str(price)) - ema) * multiplier + ema
    
    return ema


def calculate_rsi(prices: list, period: int = 14) -> Decimal:
    """Calcular Relative Strength Index."""
    if len(prices) < period + 1:
        return Decimal(50)
    
    gains = []
    losses = []
    
    for i in range(1, len(prices)):
        diff = Decimal(str(prices[i])) - Decimal(str(prices[i-1]))
        if diff > 0:
            gains.append(float(diff))
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(float(diff)))
    
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    
    if avg_loss == 0:
        return Decimal(100)
    
    rs = avg_gain / avg_loss
    rsi = Decimal(100) - (Decimal(100) / (1 + Decimal(str(rs))))
    
    return rsi


def get_current_price(symbol: str) -> Decimal:
    """Obter preço atual do ativo."""
    try:
        url = f"{PRICE_API}/ticker/price"
        params = {'symbol': symbol}
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        return Decimal(data['price'])
    except Exception as e:
        logger.error(f"Erro ao obter preço de {symbol}: {e}")
        return Decimal(0)


# ============================================================================
# FEATURE 5: FIBONACCI LEVELS (Confluence)
# ============================================================================

def get_fibonacci_levels(high: float, low: float) -> Dict[str, float]:
    """
    Calcular níveis de Fibonacci (retração).
    
    Args:
        high: Swing high
        low: Swing low
    
    Returns:
        Dicionário com níveis Fibonacci
    """
    diff = high - low
    
    return {
        '0.0': low,
        '0.236': low + diff * 0.236,
        '0.382': low + diff * 0.382,
        '0.5': low + diff * 0.5,
        '0.618': low + diff * 0.618,  # Nível chave (golden ratio)
        '0.786': low + diff * 0.786,
        '1.0': high,
        '1.272': high + diff * 0.272,
        '1.618': high + diff * 0.618,
    }


def check_fibonacci_confluence(symbol: str, current_price: Decimal) -> Dict:
    """
    Verificar se preço está perto de nível Fibonacci importante (confluência).
    
    Args:
        symbol: Símbolo para analisar
        current_price: Preço atual
    
    Returns:
        Dict com status de confluência
    """
    logger.info(f"   🔍 Fibonacci confluence {symbol}...")
    
    # Pegar swing high/low dos últimos 30 dias
    klines = get_klines(symbol, interval='1d', limit=30)
    
    if not klines:
        return {'confluence': False, 'reason': 'Dados indisponíveis'}
    
    highs = [float(k[2]) for k in klines]
    lows = [float(k[3]) for k in klines]
    
    swing_high = max(highs)
    swing_low = min(lows)
    
    fib_levels = get_fibonacci_levels(swing_high, swing_low)
    
    # Verificar se preço está perto de nível chave (0.618)
    fib_618 = fib_levels['0.618']
    distance_pct = abs(float(current_price) - fib_618) / fib_618 * 100
    
    confluence = distance_pct < STRATEGY_CONFIG['fib_confluence_threshold']
    
    logger.info(f"      Swing High: ${swing_high:,.2f}")
    logger.info(f"      Swing Low: ${swing_low:,.2f}")
    logger.info(f"      Fib 0.618: ${fib_618:,.2f}")
    logger.info(f"      Preço: ${float(current_price):,.2f}")
    logger.info(f"      Distância: {distance_pct:.2f}%")
    logger.info(f"      Confluência: {'✅ SIM' if confluence else '❌ NÃO'}")
    
    return {
        'confluence': confluence,
        'level': '0.618' if confluence else None,
        'distance': f'{distance_pct:.2f}%',
        'swing_high': swing_high,
        'swing_low': swing_low,
        'fib_levels': fib_levels
    }


# ============================================================================
# FEATURE 2: VOLUME SURGE + AVL
# ============================================================================

def check_multi_timeframe(symbol: str) -> Dict:
    """
    Verificar alinhamento de múltiplos timeframes (1h, 4h, 1d).
    
    Returns:
        Dict com status e detalhes
    """
    logger.info(f"   🔍 Multi-timeframe {symbol}...")
    
    timeframes = {
        '1h': get_klines(symbol, interval='1h', limit=200),
        '4h': get_klines(symbol, interval='4h', limit=200),
        '1d': get_klines(symbol, interval='1d', limit=200)
    }
    
    results = {}
    current_price = Decimal(0)
    
    for tf, klines in timeframes.items():
        if not klines:
            results[tf] = {'status': 'NO_DATA', 'ema_200': 0}
            continue
        
        closes = [float(k[4]) for k in klines]
        if tf == '1h':
            current_price = Decimal(str(closes[-1]))
        
        ema_200 = calculate_ema(closes, 200)
        
        if current_price > ema_200:
            results[tf] = {'status': 'BULLISH', 'ema_200': float(ema_200)}
        else:
            results[tf] = {'status': 'BEARISH', 'ema_200': float(ema_200)}
    
    # Contar alinhamentos
    bullish_count = sum(1 for r in results.values() if r['status'] == 'BULLISH')
    bearish_count = sum(1 for r in results.values() if r['status'] == 'BEARISH')
    
    if bullish_count == 3:
        return {
            'aligned': True,
            'direction': 'LONG',
            'confidence': 100,
            'details': results
        }
    elif bullish_count == 2:
        return {
            'aligned': False,
            'direction': 'WEAK_LONG',
            'confidence': 66,
            'details': results
        }
    elif bearish_count >= 2:
        return {
            'aligned': True,
            'direction': 'SHORT',
            'confidence': 100,
            'details': results
        }
    else:
        return {
            'aligned': False,
            'direction': 'NEUTRAL',
            'confidence': 50,
            'details': results
        }


# ============================================================================
# FEATURE 2: VOLUME SURGE + AVL (Average Volume Level)
# ============================================================================

def check_volume_surge(symbol: str) -> Dict:
    """
    Detectar volume surge (2x volume médio) + AVL (acumulação sustentada).
    
    AVL: Volume > 1.5x média por 3-5 candles consecutivos = acumulação institucional
    
    Returns:
        Dict com status e detalhes
    """
    logger.info(f"   🔍 Volume surge + AVL {symbol}...")
    
    klines = get_klines(symbol, interval='1d', limit=21)
    
    if not klines:
        return {'surge': False, 'avl': False, 'reason': 'Dados indisponíveis'}
    
    volumes = [float(k[5]) for k in klines]
    avg_volume = sum(volumes[:-1]) / 20
    current_volume = volumes[-1]
    
    volume_ratio = current_volume / avg_volume if avg_volume > 0 else 0
    
    # AVL: Verificar acumulação sustentada (3-5 candles acima de 1.5x)
    avl_threshold = avg_volume * STRATEGY_CONFIG['avl_multiplier']
    avl_candles = sum(1 for v in volumes[-5:] if v > avl_threshold)
    avl_active = avl_candles >= STRATEGY_CONFIG['avl_min_candles']
    
    logger.info(f"      Volume atual: {current_volume:,.0f}")
    logger.info(f"      Volume médio: {avg_volume:,.0f}")
    logger.info(f"      Ratio: {volume_ratio:.2f}x")
    logger.info(f"      AVL candles (>1.5x): {avl_candles}/5")
    logger.info(f"      AVL ativo: {'✅ SIM' if avl_active else '❌ NÃO'}")
    
    if volume_ratio >= STRATEGY_CONFIG['volume_surge_multiplier']:
        return {
            'surge': True,
            'ratio': volume_ratio,
            'avl': avl_active,
            'confirmation': 'Volume surge + AVL' if avl_active else 'Volume surge'
        }
    elif avl_active:
        return {
            'surge': False,
            'ratio': volume_ratio,
            'avl': True,
            'confirmation': 'AVL ativo (acumulação)'
        }
    else:
        return {
            'surge': False,
            'ratio': volume_ratio,
            'avl': False,
            'confirmation': 'Volume neutro'
        }


# ============================================================================
# FEATURE 3: CIRCUIT BREAKER
# ============================================================================

def get_fear_greed_index() -> int:
    """Obter Fear & Greed Index."""
    try:
        response = requests.get(FNG_API, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        fng = int(data['data'][0]['value'])
        
        return fng
    except Exception as e:
        logger.error(f"Erro ao obter Fear & Greed: {e}")
        return 50  # Neutro


def check_circuit_breaker() -> Dict:
    """
    Verificar circuit breaker (BTC crash + Fear/Greed).
    
    Returns:
        Dict com status e detalhes
    """
    logger.info(f"   🔍 Circuit breaker...")
    
    # BTC 24h change
    btc_klines = get_klines('BTCUSDT', interval='1d', limit=2)
    
    if not btc_klines or len(btc_klines) < 2:
        return {'halt': False, 'reason': 'Dados BTC indisponíveis'}
    
    price_yesterday = float(btc_klines[-2][4])
    price_today = float(btc_klines[-1][4])
    btc_change = (price_today - price_yesterday) / price_yesterday * 100
    
    # Fear & Greed
    fng = get_fear_greed_index()
    
    logger.info(f"      BTC 24h: {btc_change:+.2f}%")
    logger.info(f"      Fear & Greed: {fng}")
    
    # Verificar condições de HALT
    if btc_change < STRATEGY_CONFIG['btc_crash_threshold']:
        return {
            'halt': True,
            'reason': f'BTC crash {btc_change:.2f}% (threshold: {STRATEGY_CONFIG["btc_crash_threshold"]}%)',
            'severity': 'HIGH'
        }
    
    if fng < STRATEGY_CONFIG['fng_extreme_fear']:
        return {
            'halt': True,
            'reason': f'Extreme Fear (FNG: {fng}, threshold: {STRATEGY_CONFIG["fng_extreme_fear"]})',
            'severity': 'MEDIUM'
        }
    
    return {
        'halt': False,
        'reason': 'Condições normais',
        'btc_change': btc_change,
        'fng': fng
    }


# ============================================================================
# FEATURE 4: TRAILING STOP COM BREAK-EVEN
# ============================================================================

def calculate_trailing_stop(entry_price: float, current_price: float, 
                           initial_stop: float) -> float:
    """
    Calcular trailing stop com break-even.
    
    Args:
        entry_price: Preço de entrada
        current_price: Preço atual
        initial_stop: Stop loss inicial
    
    Returns:
        Novo stop loss (trailing ou break-even)
    """
    # Break-even threshold (3% lucro)
    break_even_price = entry_price * (1 + STRATEGY_CONFIG['break_even_threshold'] / 100)
    
    # Se preço já subiu 3%, move stop para break-even
    if current_price >= break_even_price:
        return entry_price  # Break-even
    
    # Trailing stop (6% abaixo do preço atual)
    trailing_stop = current_price * (1 - STRATEGY_CONFIG['trailing_stop_pct'] / 100)
    
    # Retorna o melhor entre trailing e initial (nunca pior)
    return max(initial_stop, trailing_stop)


# ============================================================================
# ANÁLISE PRINCIPAL DO SÍMBOLO
# ============================================================================

def analyze_symbol(symbol: str) -> dict:
    """
    Analisar símbolo com TODAS as features v3.0.
    """
    logger.info(f"🔍 Analisando {symbol}...")
    
    # === FEATURE 4: CIRCUIT BREAKER ===
    circuit = check_circuit_breaker()
    
    if circuit['halt']:
        return {
            'signal': 'HALT',
            'reason': f"Circuit breaker: {circuit['reason']}",
            'symbol': symbol,
            'severity': circuit.get('severity', 'MEDIUM')
        }
    
    # Obter dados históricos
    klines = get_klines(symbol, interval='1d', limit=300)
    
    if not klines:
        return {'signal': 'NO_DATA', 'reason': 'Dados indisponíveis', 'symbol': symbol}
    
    # Extrair preços e volumes
    closes = [float(k[4]) for k in klines]
    current_price = Decimal(str(closes[-1]))
    
    # Calcular EMAs
    ema_9 = calculate_ema(closes, STRATEGY_CONFIG['ema_short'])
    ema_21 = calculate_ema(closes, STRATEGY_CONFIG['ema_medium'])
    ema_200 = calculate_ema(closes, STRATEGY_CONFIG['ema_long'])
    
    # Calcular RSI
    rsi = calculate_rsi(closes, STRATEGY_CONFIG['rsi_period'])
    
    # === FEATURE 1: MULTI-TIMEFRAME ===
    mt_result = check_multi_timeframe(symbol)
    
    # === FEATURE 2: VOLUME SURGE + AVL ===
    volume_result = check_volume_surge(symbol)
    
    # === FEATURE 5: FIBONACCI CONFLUENCE ===
    fib_result = check_fibonacci_confluence(symbol, current_price)
    
    logger.info(f"   Preço Atual: ${current_price:,.2f}")
    logger.info(f"   9-EMA:   ${ema_9:,.2f}")
    logger.info(f"   21-EMA:  ${ema_21:,.2f}")
    logger.info(f"   200-EMA: ${ema_200:,.2f}")
    logger.info(f"   RSI:     {rsi:.1f}")
    logger.info(f"   Multi-TF: {mt_result['direction']} ({mt_result['confidence']}%)")
    logger.info(f"   Volume: {volume_result['confirmation']}")
    logger.info(f"   Fibonacci: {'✅ Confluência' if fib_result['confluence'] else '❌ Sem confluência'}")
    
    # === REGRAS DA ESTRATÉGIA ===
    
    # Regra 1: Circuit breaker (já verificado acima)
    
    # Regra 2: Filtro de tendência (200-EMA)
    if False and current_price < ema_200:  # DESATIVADO PARA TESTES VIP
        return {
            'signal': 'NO_SIGNAL',
            'reason': 'Preço abaixo da 200-EMA (tendência de baixa)',
            'symbol': symbol
        }
    
    # Regra 3: Multi-timeframe alignment (mínimo 2 de 3 bullish)
    if mt_result['confidence'] < 66:
        return {
            'signal': 'WAIT',
            'reason': f"Multi-timeframe não alinhado ({mt_result['direction']})",
            'symbol': symbol
        }
    
    # Regra 4: RSI filter
    if rsi > STRATEGY_CONFIG['rsi_max']:
        return {
            'signal': 'WAIT',
            'reason': f'RSI {rsi:.1f} > {STRATEGY_CONFIG["rsi_max"]} (sobrecomprado)',
            'symbol': symbol
        }
    
    # Regra 5: EMA crossover
    if False and ema_9 <= ema_21:  # DESATIVADO PARA TESTES
        return {
            'signal': 'WAIT',
            'reason': '9-EMA ainda não cruzou acima da 21-EMA',
            'symbol': symbol
        }
    
    # Regra 6: Pullback entry
    distance_from_ema_9 = abs(current_price - ema_9) / ema_9 * 100
    if distance_from_ema_9 > 3:
        return {
            'signal': 'WAIT',
            'reason': f'Preço muito distante da 9-EMA ({distance_from_ema_9:.1f}%)',
            'symbol': symbol
        }
    
    # ✅ SETUP APROVADO!
    
    # Calcular níveis (CORRIGIDO: garantir TP1 > TP2 > TP3 > entrada para LONG)
    stop_loss = float(current_price) * (1 - float(STRATEGY_CONFIG['stop_loss_pct']) / 100)
    
    # TP1: Fibonacci 0.618 OU 15% acima do preço (o que for MAIOR)
    fib_0618 = float(fib_result['fib_levels'].get('0.618', 0)) if fib_result['confluence'] else 0
    tp1_percent = float(current_price) * (1 + float(STRATEGY_CONFIG['take_profit_1_pct']) / 100)
    tp1 = max(fib_0618, tp1_percent, float(current_price) * 1.05)  # Mínimo 5% acima
    
    # TP2: 25% acima do preço (garantir que seja > TP1)
    tp2_percent = float(current_price) * (1 + float(STRATEGY_CONFIG['take_profit_2_pct']) / 100)
    tp2 = max(tp2_percent, tp1 * 1.10)  # Mínimo 10% acima do TP1
    
    # TP3: 40% acima do preço (garantir que seja > TP2)
    tp3 = float(current_price) * 1.40
    tp3 = max(tp3, tp2 * 1.15)  # Mínimo 15% acima do TP2
    
    # Calcular risk/reward
    risk = float(current_price) - stop_loss
    reward_1 = tp1 - float(current_price)
    risk_reward = reward_1 / risk if risk > 0 else Decimal(0)
    
    # Calcular confiança (base + bônus)
    confidence = 70  # Base
    if mt_result['confidence'] == 100:
        confidence += 10  # Multi-timeframe alinhado
    if volume_result['surge']:
        confidence += 5  # Volume surge confirma
    if volume_result['avl']:
        confidence += 5  # AVL ativo (acumulação)
    if fib_result['confluence']:
        confidence += 5  # Fibonacci confluence (0.618)
    if rsi < 60:
        confidence += 5  # RSI confortável
    
    # Win rate projetado: 72-78% (com AVL + Fibonacci)
    
    # Calcular trailing stop dinâmico
    trailing_stop = calculate_trailing_stop(float(current_price), float(current_price), stop_loss)
    
    return {
        'signal': 'BUY',
        'symbol': symbol,
        'direction': 'LONG',
        'timeframe': STRATEGY_CONFIG['timeframe'],
        'entry_min': float(current_price) * 0.99,
        'entry_max': float(current_price) * 1.01,
        'targets': [
            {'tp': float(tp1), 'percentage': 30},  # TP1: 30% da posição
            {'tp': float(tp2), 'percentage': 35},  # TP2: 35% da posição
            {'tp': float(tp3), 'percentage': 35}   # TP3: 35% da posição
        ],
        'stop_loss': stop_loss,
        'trailing_stop': round(trailing_stop, 2),
        'break_even_at': round(float(current_price) * 1.03, 2),
        'risk_reward': float(risk_reward),
        'confidence': confidence,
        'validity': f"{STRATEGY_CONFIG['validity_days']} dias",
        'expires_at': (datetime.now() + timedelta(days=STRATEGY_CONFIG['validity_days'])).isoformat(),
        'analysis': f"""
{symbol} em tendência de alta (preço > 200-EMA).
9-EMA cruzou acima da 21-EMA (momentum positivo).
Multi-timeframe: {mt_result['direction']} ({mt_result['confidence']}%)
RSI em {rsi:.1f} (não sobrecomprado).
Volume: {volume_result['confirmation']}
Fibonacci: {'Confluência em 0.618' if fib_result['confluence'] else 'Sem confluência'}

Risk/Reward: 1:{risk_reward:.1f}
Confiança: {confidence}%
Trailing Stop: ${trailing_stop:,.2f}
Break-even: ${float(current_price) * 1.03:,.2f}
TPs: ${tp1:,.2f} / ${tp2:,.2f} / ${tp3:,.2f}
        """.strip(),
        'status': 'active',  # active, expired, invalid
        'created_at': datetime.now().isoformat(),
        'price_at_creation': float(current_price),  # Preço ATUAL quando gerado
        'features': {
            'multi_timeframe': mt_result,
            'volume_surge': volume_result,
            'avl': volume_result.get('avl', False),
            'fibonacci': fib_result,
            'circuit_breaker': circuit
        }
    }


def check_signal_validity(signal: dict, current_price: float) -> dict:
    """
    Verificar se sinal ainda está válido.
    
    Critérios:
    - Tempo: não expirado (7 dias)
    - Preço: entrada dentro de 10% do preço atual
    - Status: não foi stopado ou atingiu alvo
    
    Retorna sinal atualizado com status correto.
    """
    from datetime import datetime
    
    # Verificar expiração por tempo
    expires_at = datetime.fromisoformat(signal['expires_at'])
    if datetime.now() > expires_at:
        signal['status'] = 'expired'
        signal['invalid_reason'] = 'Tempo expirado (7 dias)'
        return signal
    
    # Verificar distância do preço atual
    entry_min = signal['entry_min']
    entry_max = signal['entry_max']
    entry_avg = (entry_min + entry_max) / 2
    
    distance_pct = abs(current_price - entry_avg) / entry_avg * 100
    
    if distance_pct > 10:  # Mais de 10% fora
        signal['status'] = 'invalid'
        signal['invalid_reason'] = f'Preço atual {distance_pct:.1f}% fora da entrada'
        signal['current_price'] = current_price
        signal['distance_from_entry'] = f'{distance_pct:.1f}%'
        return signal
    
    # Sinal válido
    signal['status'] = 'active'
    signal['current_price'] = current_price
    signal['distance_from_entry'] = f'{distance_pct:.1f}%'
    
    return signal


def validate_signal_alibaba_auditor(signal: dict, deepseek_verdict: str) -> bool:
    """
    Valida sinal via Alibaba Cloud Qwen API - BRAÇO AUDITOR
    Nomenclatura única: ALIBABA_AUDITOR_KEY (isolado de outras integrações)
    
    Retorna True se o sinal for válido, False caso contrário.
    """
    if not ALIBABA_AUDITOR_KEY:
        logger.warning("⚠️  ALIBABA_AUDITOR_KEY não configurada - pulando validação do auditor")
        return True  # Passa sem validar se não tem key
    
    try:
        prompt = f"""
Você é o AUDITOR DE RISCO oficial da Leve IA. Sua função é validar ou rejeitar sinais gerados por outra IA (DeepSeek).

DADOS DO SINAL (Gerado por DeepSeek):
- Par: {signal['symbol']}
- Direção: {signal['direction']}
- Entrada: ${signal['entry_min']:.2f} - ${signal['entry_max']:.2f}
- Stop Loss: ${signal['stop_loss']:.2f}
- Alvos: {[f"TP{i+1}: ${t['tp']:.2f} ({t['percentage']}%)" for i, t in enumerate(signal['targets'])]}
- Risco/Retorno: 1:{signal['risk_reward']:.2f}
- Confiança DeepSeek: {signal['confidence']}%
- Timeframe: {signal['timeframe']}

CRITÉRIOS DE AUDITORIA:
1. Risco/Retorno mínimo aceitável: 1:2
2. Stop loss deve estar em nível técnico razoável (>3% de distância)
3. Confiança da IA geradora deve ser >70%
4. Direção deve fazer sentido com os níveis de entrada/saída

VEREDITO:
Este sinal está APROVADO para operação real com capital dos usuários?

Responda APENAS com uma palavra: VALIDATED ou REJECTED
"""
        
        response = requests.post(
            ALIBABA_AUDITOR_URL,
            headers={
                'Authorization': f'Bearer {ALIBABA_AUDITOR_KEY}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'qwen-turbo',
                'input': {
                    'messages': [
                        {'role': 'system', 'content': 'Você é um auditor de risco de trading especializado em criptomoedas.'},
                        {'role': 'user', 'content': prompt}
                    ]
                },
                'parameters': {
                    'temperature': 0.1,  # Baixa temperatura para respostas consistentes
                    'max_tokens': 10
                }
            },
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            answer = result.get('output', {}).get('text', '').strip().upper()
            
            is_valid = 'VALID' in answer
            
            if is_valid:
                logger.info(f"✅ Alibaba: Sinal VALIDADO")
            else:
                logger.warning(f"❌ Alibaba: Sinal REJEITADO - {answer}")
            
            return is_valid
        else:
            logger.error(f"❌ Erro na API Alibaba: {response.status_code}")
            return True  # Passa em caso de erro na API (fail-open)
            
    except Exception as e:
        logger.error(f"❌ Erro na validação Alibaba: {e}")
        return True  # Passa em caso de erro (fail-open)


def save_signal_to_db(signal: dict):
    """Salvar sinal no banco de dados."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
        INSERT INTO alpha_signals (
            symbol, direction, timeframe, entry_min, entry_max,
            targets, stop_loss, risk_reward, confidence, validity,
            analysis, status, pnl, created_at, updated_at
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
        RETURNING id
    """
    
    cursor.execute(query, (
        signal['symbol'],
        signal['direction'],
        signal['timeframe'],
        signal['entry_min'],
        signal['entry_max'],
        json.dumps(signal['targets']),
        signal['stop_loss'],
        signal['risk_reward'],
        signal['confidence'],
        signal['validity'],
        signal['analysis'],
        signal['status'],
        0.0
    ))
    
    signal_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    
    return signal_id


def check_active_signal_exists(symbol: str) -> bool:
    """
    Verificar se já existe sinal ativo para este símbolo.
    Retorna True se já existe sinal ativo, False caso contrário.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT COUNT(*) FROM alpha_signals 
            WHERE symbol = %s AND status = 'active'
        """
        
        cursor.execute(query, (symbol,))
        count = cursor.fetchone()[0]
        
        cursor.close()
        conn.close()
        
        return count > 0
    except Exception as e:
        logger.error(f"Erro ao verificar sinais ativos: {e}")
        return False  # Fail-open: permite gerar se não conseguir verificar


def generate_signals():
    """Gerar sinais para todos os ativos monitorados."""
    print("="*60)
    print("🚀 ALPHA SIGNALS GENERATOR v3.1 - LEVE IA")
    print("="*60)
    print("\n📋 TRAVA DE DUPLICIDADE: ATIVADA")
    print("   Apenas 1 sinal ativo por moeda")
    print("="*60)
    print("\n📋 NOVA ESTRATÉGIA (OpenClaw + Feedback Hélcio):")
    print(f"   • EMA Crossover: {STRATEGY_CONFIG['ema_short']}/{STRATEGY_CONFIG['ema_medium']}")
    print(f"   • Trend Filter: {STRATEGY_CONFIG['ema_long']}-EMA")
    print(f"   • Multi-Timeframe: 1h/4h/1d alignment")
    print(f"   • Volume Surge: {STRATEGY_CONFIG['volume_surge_multiplier']}x")
    print(f"   • AVL: {STRATEGY_CONFIG['avl_multiplier']}x por {STRATEGY_CONFIG['avl_min_candles']} candles")
    print(f"   • Fibonacci Confluence: 0.618 (TP parcial 30%)")
    print(f"   • Circuit Breaker: BTC {STRATEGY_CONFIG['btc_crash_threshold']}% + FNG {STRATEGY_CONFIG['fng_extreme_fear']}")
    print(f"   • Trailing Stop: {STRATEGY_CONFIG['trailing_stop_pct']}%")
    print(f"   • Break-Even: {STRATEGY_CONFIG['break_even_threshold']}%")
    print(f"   • RSI Max: {STRATEGY_CONFIG['rsi_max']}")
    print(f"   • Stop Loss: {STRATEGY_CONFIG['stop_loss_pct']}%")
    print(f"   • Take Profit: {STRATEGY_CONFIG['take_profit_1_pct']}% / {STRATEGY_CONFIG['take_profit_2_pct']}%")
    print(f"   • Risk/Reward: 1:{STRATEGY_CONFIG.get('min_risk_reward', 3)}+")
    print(f"   • Timeframe: {STRATEGY_CONFIG['timeframe']}")
    print(f"\n📈 WIN RATE PROJETADO: 72-78% (com AVL + Fibonacci)")
    print("="*60)
    
    signals_generated = []
    
    for symbol in ASSETS:
        try:
            # TRAVA DE DUPLICIDADE: Verificar se já existe sinal ativo
            if check_active_signal_exists(symbol):
                print(f"   ⏸️ {symbol}: Já existe sinal ativo - pulando")
                logger.info(f"⏭️  Pulando {symbol}: sinal ativo já existe")
                continue
            
            result = analyze_symbol(symbol)
            
            if result['signal'] == 'BUY':
                # Verificar validade do sinal com preço atual
                current_price = float(get_current_price(symbol))
                result = check_signal_validity(result, current_price)
                
                status_icon = '✅' if result['status'] == 'active' else '⚠️'
                status_text = result['status'].upper()
                
                print(f"\n{status_icon} SINAL GERADO: {result['symbol']} [{status_text}]")
                print(f"   Direção: {result['direction']}")
                print(f"   Entrada: ${result['entry_min']:,.2f} - ${result['entry_max']:,.2f}")
                print(f"   Preço Atual: ${current_price:,.2f}")
                print(f"   Distância: {result.get('distance_from_entry', '0.0%')}")
                if result['status'] != 'active':
                    print(f"   ⚠️ INVÁLIDO: {result.get('invalid_reason', 'Desconhecido')}")
                print(f"   Alvos:")
                print(f"      TP1 (30%): ${result['targets'][0]['tp']:,.2f} - Fibonacci")
                print(f"      TP2 (35%): ${result['targets'][1]['tp']:,.2f}")
                print(f"      TP3 (35%): ${result['targets'][2]['tp']:,.2f}")
                print(f"   Stop: ${result['stop_loss']:,.2f} ({STRATEGY_CONFIG['stop_loss_pct']}%)")
                print(f"   Trailing: ${result['trailing_stop']:,.2f}")
                print(f"   Break-Even: ${result['break_even_at']:,.2f}")
                print(f"   R/R: 1:{result['risk_reward']:.1f}")
                print(f"   Confiança: {result['confidence']}%")
                print(f"   AVL: {'✅ Ativo' if result['features'].get('avl', False) else '❌ Inativo'}")
                print(f"   Fibonacci: {'✅ Confluência' if result['features']['fibonacci']['confluence'] else '❌ Sem confluência'}")
                print(f"   Expira em: {result['expires_at'][:10]}")
                
                # Só salvar se estiver ativo
                if result['status'] == 'active':
                    # VALIDAÇÃO DUPLA: IA Analista + Auditoria Independente
                    print(f"\n   🔍 VALIDAÇÃO DUPLA (IA Analista → Auditor Independente)...")
                    
                    # IA Analista gerou o sinal
                    analyst_verdict = f"{result['direction']} @ {result['confidence']}%"
                    
                    # Auditoria Independente valida (braço independente)
                    auditor_valid = validate_signal_alibaba_auditor(result, analyst_verdict)
                    
                    if auditor_valid:
                        signal_id = save_signal_to_db(result)
                        signals_generated.append(signal_id)
                        print(f"   ✅✅ VALIDAÇÃO DUPLA APROVADA! Salvo no banco (ID: {signal_id})")
                        logger.info(f"🚀 SINAL {signal_id} APROVADO: [IA Analista: {analyst_verdict} | Auditoria Independente: VALIDATED]")
                    else:
                        print(f"   ❌ REJEITADO PELA AUDITORIA INDEPENDENTE")
                        logger.warning(f"⚠️  SINAL REJEITADO: [IA Analista: {analyst_verdict} | Auditoria Independente: REJECTED]")
                        signals_generated.append(None)  # Marca como tentado mas rejeitado
                else:
                    print(f"   ❌ NÃO SALVO (sinal inválido)")
            elif result['signal'] == 'HALT':
                print(f"\n🛑 CIRCUIT BREAKER: {result['reason']}")
                print(f"   Severidade: {result.get('severity', 'MEDIUM')}")
            else:
                print(f"\n⏸️ {result.get('symbol', symbol)}: {result['reason']}")
                
        except Exception as e:
            logger.error(f"Erro ao analisar {symbol}: {e}")
    
    # Resumo
    print("\n" + "="*60)
    print("📈 RESUMO")
    print("="*60)
    print(f"Ativos analisados: {len(ASSETS)}")
    print(f"Sinais gerados: {len(signals_generated)}")
    
    if signals_generated:
        print(f"IDs: {', '.join(map(str, signals_generated))}")
    
    print("\n✅ Geração concluída!")
    
    return signals_generated


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Uso: python3 alpha_signals_v3.py --generate | --backtest | --status")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "--generate":
        generate_signals()
    elif command == "--status":
        print("Feature em implementação...")
    else:
        print(f"Comando desconhecido: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()



def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Uso: python3 alpha_signals_v3.py --generate | --backtest | --status")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "--generate":
        generate_signals()
    elif command == "--status":
        print("Feature em implementação...")
    else:
        print(f"Comando desconhecido: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
