#!/usr/bin/env python3
"""
Expire Alpha Signals - Script para expirar sinais ativos antigos ou inválidos.

Regras de expiração:
1. Tempo: Sinais com mais de 7 dias (created_at < NOW() - INTERVAL '7 days')
2. Distância: Sinais onde o preço atual está muito longe da entrada (>20%)
3. Status automático: Usa a mesma lógica de validade do alpha_signals_v3.py

Uso:
    python3 expire_signals.py
    python3 expire_signals.py --dry-run (apenas mostra, não atualiza)
    python3 expire_signals.py --verbose
"""

import os
import sys
import psycopg2
import requests
from datetime import datetime, timedelta
from decimal import Decimal
import logging
import argparse
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# Configuração de Log
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuração do Banco
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 5432)),
    'database': os.getenv('DB_NAME', 'leveclaw'),
    'user': os.getenv('DB_USER', 'leveclaw_user'),
    'password': os.getenv('DB_PASSWORD', 'leveclaw_password')
}

# API Binance para preços
PRICE_API = "https://api.binance.com/api/v3"

# Thresholds
MAX_AGE_DAYS = 7
MAX_DISTANCE_PCT = 20.0  # Se preço atual está >20% longe da entrada média

def get_db_connection():
    """Estabelecer conexão com PostgreSQL."""
    return psycopg2.connect(**DB_CONFIG)

def get_current_price(symbol: str) -> Decimal:
    """Obter preço atual do ativo (Binance)."""
    try:
        # Converter símbolo para formato Binance (ex: BTC -> BTCUSDT)
        if not symbol.endswith('USDT'):
            symbol = f"{symbol}USDT"
        
        url = f"{PRICE_API}/ticker/price"
        params = {'symbol': symbol}
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        return Decimal(data['price'])
    except Exception as e:
        logger.error(f"Erro ao obter preço de {symbol}: {e}")
        return Decimal(0)

def check_signal_validity(signal, current_price=None):
    """
    Verificar validade do sinal (baseado no alpha_signals_v3.py).
    
    Args:
        signal: Dicionário com dados do sinal
        current_price: Preço atual (opcional, será buscado se não fornecido)
    
    Returns:
        Tuple (is_valid, reason)
    """
    try:
        # 1. Verificar expiração por tempo
        created_at = signal['created_at']
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
        
        expires_at = created_at + timedelta(days=MAX_AGE_DAYS)
        if datetime.now() > expires_at:
            return False, 'Tempo expirado (7 dias)'
        
        # 2. Se não temos preço atual, não podemos verificar distância
        if current_price is None:
            return True, 'Ativo (sem verificação de preço)'
        
        # 3. Verificar distância da entrada
        entry_min = signal['entry_min']
        entry_max = signal['entry_max']
        entry_avg = (entry_min + entry_max) / 2
        
        distance_pct = abs(float(current_price) - entry_avg) / entry_avg * 100
        if distance_pct > MAX_DISTANCE_PCT:
            return False, f'Distância grande ({distance_pct:.1f}% > {MAX_DISTANCE_PCT}%)'
        
        return True, 'Ativo'
    except Exception as e:
        logger.error(f"Erro ao verificar validade do sinal {signal.get('id')}: {e}")
        return False, f'Erro na verificação: {e}'

def expire_signals(dry_run=False, verbose=False):
    """
    Processo principal de expiração de sinais.
    
    Args:
        dry_run: Se True, apenas mostra ações sem atualizar banco
        verbose: Se True, mostra detalhes de cada sinal processado
    """
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Buscar todos os sinais ativos
        query = """
            SELECT 
                id, symbol, direction, entry_min, entry_max, 
                status, created_at, user_id
            FROM alpha_signals 
            WHERE status = 'active'
            ORDER BY created_at
        """
        
        cursor.execute(query)
        active_signals = cursor.fetchall()
        
        total = len(active_signals)
        logger.info(f"📊 Encontrados {total} sinais ativos para verificação")
        
        expired_time = 0
        expired_distance = 0
        still_active = 0
        errors = 0
        
        # Processar cada sinal
        for row in active_signals:
            (signal_id, symbol, direction, entry_min, entry_max, 
             status, created_at, user_id) = row
            
            signal = {
                'id': signal_id,
                'symbol': symbol,
                'direction': direction,
                'entry_min': float(entry_min) if entry_min else 0,
                'entry_max': float(entry_max) if entry_max else 0,
                'created_at': created_at,
                'user_id': user_id
            }
            
            # Obter preço atual
            current_price = get_current_price(symbol)
            if current_price == 0:
                # Se não conseguiu preço, assumir válido (não expirar por erro)
                is_valid, reason = True, 'Erro ao obter preço - mantendo ativo'
                if verbose:
                    logger.info(f"  ⚠️  {symbol} ({direction}): {reason}")
                still_active += 1
                continue
            
            # Verificar validade
            is_valid, reason = check_signal_validity(signal, current_price)
            
            if not is_valid:
                # Expirar este sinal
                action = "EXPIRAR" if not dry_run else "[DRY-RUN] Expirar"
                
                if 'Tempo expirado' in reason:
                    expired_time += 1
                else:
                    expired_distance += 1
                
                if verbose:
                    logger.info(f"  ❌ {action}: {symbol} ({direction}) - {reason}")
                    logger.info(f"     ID: {signal_id}, Criado: {created_at}")
                    logger.info(f"     Entrada: ${entry_min:,.2f}-${entry_max:,.2f}, Preço atual: ${current_price:,.2f}")
                
                if not dry_run:
                    # Atualizar status no banco
                    update_query = """
                        UPDATE alpha_signals 
                        SET status = 'expired', 
                            updated_at = NOW()
                        WHERE id = %s
                    """
                    cursor.execute(update_query, (signal_id,))
            else:
                still_active += 1
                if verbose:
                    logger.info(f"  ✅ Manter ativo: {symbol} ({direction}) - {reason}")
        
        # Commit das mudanças
        if not dry_run:
            conn.commit()
            logger.info(f"💾 Mudanças salvas no banco")
        
        # Resumo
        logger.info("=" * 60)
        logger.info(f"📋 RESUMO DA EXPIRAÇÃO")
        logger.info(f"   Total de sinais ativos: {total}")
        logger.info(f"   Expirados por tempo: {expired_time}")
        logger.info(f"   Expirados por distância: {expired_distance}")
        logger.info(f"   Mantidos ativos: {still_active}")
        logger.info(f"   Erros: {errors}")
        
        if dry_run:
            logger.info(f"   ⚠️  MODO DRY-RUN - Nenhuma alteração no banco")
        
        logger.info("=" * 60)
        
        cursor.close()
        
        return {
            'total': total,
            'expired_time': expired_time,
            'expired_distance': expired_distance,
            'still_active': still_active,
            'errors': errors
        }
        
    except Exception as e:
        logger.error(f"Erro fatal no processo de expiração: {e}")
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()

def main():
    parser = argparse.ArgumentParser(description='Expirar sinais ativos antigos')
    parser.add_argument('--dry-run', action='store_true', 
                       help='Apenas mostra o que seria feito, sem atualizar banco')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Mostrar detalhes de cada sinal processado')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🔄 EXPIRADOR DE SINAIS - ALPHA SIGNALS")
    print(f"   Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   Modo: {'DRY-RUN' if args.dry_run else 'EXECUÇÃO REAL'}")
    print("=" * 60)
    
    try:
        results = expire_signals(
            dry_run=args.dry_run,
            verbose=args.verbose
        )
        
        # Retornar código de saída apropriado
        if results['total'] == 0:
            print("ℹ️  Nenhum sinal ativo encontrado.")
            sys.exit(0)
        
    except Exception as e:
        logger.error(f"Falha na execução: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()