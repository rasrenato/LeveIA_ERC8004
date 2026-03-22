#!/usr/bin/env python3
"""
Expire Alpha Signals - Versão simples (apenas por tempo)

Regra: expirar sinais com created_at < NOW() - INTERVAL '7 days'

Uso:
    python3 expire_signals_simple.py
    python3 expire_signals_simple.py --dry-run
"""

import os
import sys
import psycopg2
from datetime import datetime
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

def get_db_connection():
    """Estabelecer conexão com PostgreSQL."""
    return psycopg2.connect(**DB_CONFIG)

def expire_signals_by_age(max_age_days=7, dry_run=False):
    """
    Expirar sinais ativos com mais de N dias.
    
    Args:
        max_age_days: Idade máxima em dias antes de expirar
        dry_run: Se True, apenas mostra estatísticas sem atualizar
    """
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Query para contar sinais que serão expirados
        count_query = """
            SELECT COUNT(*) 
            FROM alpha_signals 
            WHERE status = 'active' 
              AND created_at < NOW() - INTERVAL '%s days'
        """ % max_age_days
        
        cursor.execute(count_query)
        count_to_expire = cursor.fetchone()[0]
        
        # Query para ver total de ativos
        total_query = """
            SELECT COUNT(*) 
            FROM alpha_signals 
            WHERE status = 'active'
        """
        
        cursor.execute(total_query)
        total_active = cursor.fetchone()[0]
        
        logger.info(f"📊 Sinais ativos totais: {total_active}")
        logger.info(f"📊 Sinais a expirar (>{max_age_days} dias): {count_to_expire}")
        
        if count_to_expire == 0:
            logger.info(f"✅ Nenhum sinal para expirar (todos têm menos de {max_age_days} dias)")
            return {
                'total_active': total_active,
                'expired': 0,
                'remaining': total_active
            }
        
        # Mostrar alguns exemplos
        if count_to_expire > 0:
            example_query = """
                SELECT id, symbol, direction, created_at 
                FROM alpha_signals 
                WHERE status = 'active' 
                  AND created_at < NOW() - INTERVAL '%s days'
                ORDER BY created_at 
                LIMIT 5
            """ % max_age_days
            cursor.execute(example_query)
            examples = cursor.fetchall()
            
            logger.info("📝 Exemplos de sinais a expirar:")
            for ex in examples:
                signal_id, symbol, direction, created_at = ex
                logger.info(f"   - {symbol} ({direction}): {signal_id[:8]}... criado em {created_at}")
        
        # Executar UPDATE se não for dry-run
        if not dry_run:
            update_query = """
                UPDATE alpha_signals 
                SET status = 'expired', 
                    updated_at = NOW()
                WHERE status = 'active' 
                  AND created_at < NOW() - INTERVAL '%s days'
            """ % max_age_days
            
            cursor.execute(update_query)
            affected_rows = cursor.rowcount
            conn.commit()
            
            logger.info(f"✅ Expiração concluída: {affected_rows} sinais atualizados para 'expired'")
            
            # Verificar resultado
            cursor.execute(total_query)
            new_total = cursor.fetchone()[0]
            
            return {
                'total_active': total_active,
                'expired': affected_rows,
                'remaining': new_total
            }
        else:
            logger.info("⚠️  MODO DRY-RUN - Nenhuma alteração no banco")
            return {
                'total_active': total_active,
                'expired': count_to_expire,
                'remaining': total_active - count_to_expire
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
    parser = argparse.ArgumentParser(description='Expirar sinais ativos com mais de N dias')
    parser.add_argument('--dry-run', action='store_true', 
                       help='Apenas mostra o que seria feito, sem atualizar banco')
    parser.add_argument('--max-age-days', type=int, default=7,
                       help='Idade máxima em dias antes de expirar (padrão: 7)')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🔄 EXPIRADOR DE SINAIS (SIMPLES) - ALPHA SIGNALS")
    print(f"   Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   Regra: Sinais ativos com mais de {args.max_age_days} dias")
    print(f"   Modo: {'DRY-RUN' if args.dry_run else 'EXECUÇÃO REAL'}")
    print("=" * 60)
    
    try:
        results = expire_signals_by_age(max_age_days=args.max_age_days, dry_run=args.dry_run)
        
        print("\n📋 RESUMO:")
        print(f"   Sinais ativos antes: {results['total_active']}")
        print(f"   Sinais expirados: {results['expired']}")
        print(f"   Sinais ativos após: {results['remaining']}")
        print("=" * 60)
        
        if results['expired'] > 0:
            print(f"✅ {results['expired']} sinais expirados com sucesso!")
        else:
            print("ℹ️  Nenhum sinal precisou ser expirado.")
        
    except Exception as e:
        logger.error(f"Falha na execução: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()