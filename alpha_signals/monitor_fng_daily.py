#!/usr/bin/env python3
"""
Monitor Diário FNG + Alpha Signals

Verifica condições de mercado e gera sinais automaticamente.

Condições necessárias:
1. FNG > 20 (sair do extreme fear)
2. BTC > 200-EMA (tendência de alta)
3. BTC 24h > -10% (sem crash)

Se todas baterem: roda alpha_signals_v3.py --generate
Se não: registra log sem gerar sinais

Uso:
    python3 monitor_fng_daily.py
"""

import requests
import subprocess
import json
from datetime import datetime
import sys

# APIs
FNG_API = "https://api.alternative.me/fng/"
BINANCE_API = "https://api.binance.com/api/v3"

# Thresholds
FNG_THRESHOLD = 20
BTC_CRASH_THRESHOLD = -10.0


def get_fear_greed() -> int:
    """Obter Fear & Greed Index."""
    try:
        response = requests.get(FNG_API, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        fng = int(data['data'][0]['value'])
        
        return fng
    except Exception as e:
        print(f"Erro ao obter FNG: {e}")
        return 50  # Neutro


def get_btc_data() -> dict:
    """Obter dados do BTC (preço, 200-EMA, 24h change)."""
    try:
        # Preço atual e 24h change
        ticker_url = f"{BINANCE_API}/ticker/24hr"
        params = {'symbol': 'BTCUSDT'}
        
        ticker_response = requests.get(ticker_url, params=params, timeout=10)
        ticker_response.raise_for_status()
        ticker = ticker_response.json()
        
        current_price = float(ticker['lastPrice'])
        price_change_pct = float(ticker['priceChangePercent'])
        
        # 200-EMA (dados diários)
        klines_url = f"{BINANCE_API}/klines"
        klines_params = {'symbol': 'BTCUSDT', 'interval': '1d', 'limit': 200}
        
        klines_response = requests.get(klines_url, params=klines_params, timeout=10)
        klines_response.raise_for_status()
        klines = klines_response.json()
        
        # Calcular 200-EMA
        closes = [float(k[4]) for k in klines]
        
        multiplier = 2 / (200 + 1)
        ema = sum(closes[:200]) / 200
        
        for price in closes[200:]:
            ema = (price - ema) * multiplier + ema
        
        return {
            'price': current_price,
            'ema_200': ema,
            'change_24h': price_change_pct,
            'above_ema': current_price > ema
        }
    except Exception as e:
        print(f"Erro ao obter dados BTC: {e}")
        return {
            'price': 0,
            'ema_200': 0,
            'change_24h': 0,
            'above_ema': False
        }


def expire_old_signals():
    """Expirar sinais antigos (>7 dias)."""
    try:
        result = subprocess.run(
            ['python3', 'expire_signals_simple.py'],
            capture_output=True,
            text=True,
            cwd='/root/openclaw/alpha_signals',
            timeout=30
        )
        
        return {
            'success': True,
            'stdout': result.stdout,
            'stderr': result.stderr
        }
    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'error': 'Timeout após 30 segundos'
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def run_alpha_signals():
    """Rodar alpha_signals_v3.py --generate."""
    try:
        result = subprocess.run(
            ['python3', 'alpha_signals_v3.py', '--generate'],
            capture_output=True,
            text=True,
            cwd='/root/openclaw/alpha_signals',
            timeout=120
        )
        
        return {
            'success': True,
            'stdout': result.stdout,
            'stderr': result.stderr
        }
    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'error': 'Timeout após 120 segundos'
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def main():
    """Main entry point."""
    print("="*60)
    print("🔍 MONITOR DIÁRIO - LEVE IA ALPHA SIGNALS")
    print("="*60)
    print(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("="*60)
    
    # 1. Fear & Greed
    print("\n📊 FEAR & GREED INDEX")
    fng = get_fear_greed()
    print(f"   Valor: {fng}")
    print(f"   Threshold: {FNG_THRESHOLD}")
    
    fng_ok = fng > FNG_THRESHOLD
    print(f"   Status: {'✅ OK' if fng_ok else '❌ BLOQUEADO'}")
    
    # 2. BTC Data
    print("\n₿ BTC DATA")
    btc = get_btc_data()
    print(f"   Preço: ${btc['price']:,.2f}")
    print(f"   200-EMA: ${btc['ema_200']:,.2f}")
    print(f"   24h Change: {btc['change_24h']:+.2f}%")
    print(f"   Acima da EMA: {'✅ SIM' if btc['above_ema'] else '❌ NÃO'}")
    
    btc_ema_ok = btc['above_ema']
    btc_crash_ok = btc['change_24h'] > BTC_CRASH_THRESHOLD
    
    print(f"   Status EMA: {'✅ OK' if btc_ema_ok else '❌ BLOQUEADO'}")
    print(f"   Status Crash: {'✅ OK' if btc_crash_ok else '❌ BLOQUEADO'}")
    
    # 3. Decisão
    print("\n" + "="*60)
    print("🚀 RESULTADO")
    print("="*60)
    
    all_ok = fng_ok and btc_ema_ok and btc_crash_ok
    
    if all_ok:
        print("\n✅ **CONDIÇÕES APROVADAS!**")
        print("\n🔄 Expirando sinais antigos (>3 dias)...")
        print("-"*60)
        expire_result = expire_old_signals()
        if not expire_result['success']:
            print(f"⚠️  Aviso na expiração: {expire_result.get('error', 'Desconhecido')}")
        
        print("\n🚀 Rodando Alpha Signals v3.0...")
        print("-"*60)
        
        result = run_alpha_signals()
        
        if result['success']:
            print(result['stdout'])
            
            if result['stderr']:
                print("⚠️ Warnings:")
                print(result['stderr'])
        else:
            print(f"❌ Erro: {result.get('error', 'Desconhecido')}")
        
        print("-"*60)
        print("\n✅ Monitoramento concluído!")
        print("Próxima verificação: Amanhã 8:00 UTC")
        
    else:
        print("\n⏸️ **CONDIÇÕES NÃO APROVADAS**")
        
        reasons = []
        if not fng_ok:
            reasons.append(f"FNG {fng} < {FNG_THRESHOLD} (Extreme Fear)")
        if not btc_ema_ok:
            reasons.append(f"BTC ${btc['price']:,.0f} < 200-EMA ${btc['ema_200']:,.0f}")
        if not btc_crash_ok:
            reasons.append(f"BTC crash {btc['change_24h']:.1f}% < {BTC_CRASH_THRESHOLD}%")
        
        print("\nMotivos:")
        for reason in reasons:
            print(f"   ❌ {reason}")
        
        print("\nAção: Nenhum sinal gerado (circuit breaker ativo)")
        print("Próxima verificação: Amanhã 8:00 UTC")
    
    print("\n" + "="*60)
    print("🍃 Leve IA - Verifiable AI is the only AI")
    print("="*60)


if __name__ == "__main__":
    main()
