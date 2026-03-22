#!/usr/bin/env python3
"""
Expire Alpha Signals - Versão avançada (tempo + distância)

Regras:
1. Tempo: Sinais com mais de N dias (padrão: 7)
2. Distância: Sinais onde preço atual está > X% da entrada (padrão: 20%)

Uso:
    python3 expire_signals_advanced.py
    python3 expire_signals_advanced.py --dry-run
    python3 expire_signals_advanced.py --max-age-days 3 --max-distance-pct 15
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

# API Binance
PRICE_API = "https://api.binance.com/api/v3"

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

def get_current_price_batch(symbols):
    """Obter preços para múltiplos símbolos de uma vez."""
    prices = {}
    
    # Binance aceita múltiplos símbolos? A API /ticker/price não suporta batch.
    # Vamos fazer uma requisição por símbolo, mas com cache.
    for symbol in symbols:
        try:
            # Garantir formato USDT
            if not symbol.endswith('USDT'):
                symbol_key = f"{symbol}USDT"
            else:
                symbol_key = symbol
            
            url = f"{PRICE_API}/ticker/price"
            params = {'symbol': symbol_key}
            
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            prices[symbol] = Decimal(data['price'])
        except Exception as e:
            logger.warning(f"Erro ao obter preço para {symbol}: {e}")
            prices[symbol] = Decimal(0)
    
    return prices

def expire_signals_advanced(max_age_days=7, max_distance_pct=20.0, dry_run=False):
    """
    Expirar sinais com base em idade e distância do preço atual.
    
    Args:
        max_age_days: Máximo de dias antes de expirar
        max_distance_pct: Máxima distância percentual da entrada
        dry_run: Se True, apenas simula
    """
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 1. Buscar todos os sinais ativos com símbolos únicos
        query = """
            SELECT 
                id, symbol, direction, entry_min, entry_max, 
                status, created_at, user_id
            FROM alpha_signals 
            WHERE status = 'active'
            ORDER BY symbol, created_at
        """
        
        cursor.execute(query)
        active_signals = cursor.fetchall()
        
        total = len(active_signals)
        logger.info(f"📊 Encontrados {total} sinais ativos")
        
        if total == 0:
            logger.info("✅ Nenhum sinal ativo encontrado")
            return {'total': 0, 'expired_age': 0, 'expired_distance': 0, 'remaining': 0}
        
        # 2. Extrair símbolos únicos para buscar preços
        symbols = set()
        for row in active_signals:
            symbols.add(row[1])  # símbolo
        
        logger.info(f"📊 Buscando preços para {len(symbols)} símbolos únicos...")
        prices = get_current_price_batch(symbols)
        
        # 3. Processar cada sinal
        expired_age = 0
        expired_distance = 0
        to_expire = []
        
        for row in active_signals:
            (signal_id, symbol, direction, entry_min, entry_max, 
             status, created_at, user_id) = row
            
            # Verificar idade
            age_days = (datetime.now() - created_at).days
            if age_days > max_age_days:
                expired_age += 1
                to_expire.append(signal_id)
                continue
            
            # Verificar distância (se temos preço)
            current_price = prices.get(symbol)
            if current_price and current_price > 0:
                entry_min_f = float(entry_min) if entry_min else 0
                entry_max_f = float(entry_max) if entry_max else 0
                
                if entry_min_f == 0 or entry_max_f == 0:
                    continue
                
                entry_avg = (entry_min_f + entry_max_f) / 2
                distance_pct = abs(float(current_price) - entry_avg) / entry_avg * 100
                
                if distance_pct > max_distance_pct:
                    expired_distance += 1
                    to_expire.append(signal_id)
        
        # 4. Executar UPDATE se houver sinais para expirar
        expired_total = len(to_expire)
        remaining = total - expired_total
        
        logger.info(f"📊 Sinais a expirar por idade: {expired_age}")
        logger.info(f"📊 Sinais a expirar por distância: {expired_distance}")
        logger.info(f"📊 Total a expirar: {expired_total}")
        logger.info(f"📊 Permanecerão ativos: {remaining}")
        
        if expired_total > 0:
            if not dry_run:
                # Atualizar em lote (usando IN)
                # Dividir em chunks para evitar query muito grande
                chunk_size = 500
                for i in range(0, len(to_expire), chunk_size):
                    chunk = to_expire[i:i+chunk_size]
                    
                    # Converter UUIDs para string
                    chunk_ids = [str(id) for id in chunk]
                    
                    # Criar placeholders
                    placeholders = ','.join(['%s'] * len(chunk_ids))
                    
                    update_query = f"""
                        UPDATE alpha_signals 
                        SET status = 'expired', 
                            updated_at = NOW()
                        WHERE id IN ({placeholders})
                    """
                    
                    cursor.execute(update_query, chunk_ids)
                
                conn.commit()
                logger.info(f"✅ {expired_total} sinais expirados com sucesso!")
            else:
                logger.info("⚠️  MODO DRY-RUN - Nenhuma alteração no banco")
        
        return {
            'total': total,
            'expired_age': expired_age,
            'expired_distance': expired_distance,
            'expired_total': expired_total,
            'remaining': remaining
        }
        
    except Exception as e:
        logger.error(f"Erro fatal: {e}")
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()

def main():
    parser = argparse.ArgumentParser(description='Expirar sinais ativos (idade + distância)')
    parser.add_argument('--dry-run', action='store_true', 
                       help='Apenas mostra o que seria feito, sem atualizar banco')
    parser.add_argument('--max-age-days', type=int, default=7,
                       help='Idade máxima em dias antes de expirar (padrão: 7)')
    parser.add_argument('--max-distance-pct', type=float, default=20.0,
                       help='Distância máxima percentual da entrada (padrão: 20%%)')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🔄 EXPIRADOR DE SINAIS (AVANÇADO) - ALPHA SIGNALS")
    print(f"   Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   Idade máxima: {args.max_age_days} dias")
    print(f"   Distância máxima: {args.max_distance_pct}%")
    print(f"   Modo: {'DRY-RUN' if args.dry_run else 'EXECUÇÃO REAL'}")
    print("=" * 60)
    
    try:
        results = expire_signals_advanced(
            max_age_days=args.max_age_days,
            max_distance_pct=args.max_distance_pct,
            dry_run=args.dry_run
        )
        
        print("\n📋 RESUMO DETALHADO:")
        print(f"   Total de sinais ativos: {results['total']}")
        print(f"   Expirados por idade: {results['expired_age']}")
        print(f"   Expirados por distância: {results['expired_distance']}")
        print(f"   Total expirados: {results['expired_total']}")
        print(f"   Permanecerão ativos: {results['remaining']}")
        print("=" * 60)
        
        if results['expired_total'] > 0:
            if args.dry_run:
                print(f"⚠️  DRY-RUN: {results['expired_total']} sinais SERIAM expirados")
            else:
                print(f"✅ {results['expired_total']} sinais expirados com sucesso!")
        else:
            print("ℹ️  Nenhum sinal precisou ser expirado.")
        
    except Exception as e:
        logger.error(f"Falha na execução: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()