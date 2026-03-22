#!/usr/bin/env python3
"""
Result Tracker - Leve IA
Atualiza automaticamente o status (WIN/LOSS) dos sinais de trading

Executa a cada 1 hora para verificar sinais ativos e atualizar:
- status: 'active' → 'WIN' ou 'LOSS'
- pnl: PnL percentual final

Uso:
    python3 result_tracker.py
    python3 result_tracker.py --once  # Roda uma vez e sai
"""

import psycopg2
import requests
from datetime import datetime
import logging
import json
import sys
from typing import List, Tuple, Optional

# Configuração de Log
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('/opt/leveclaw/backend/logs/result-tracker.log')
    ]
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

# Binance API
BINANCE_API = "https://api.binance.com/api/v3"

# Configurações
CHECK_AGE_HOURS = 48  # Verifica sinais ativos das últimas 48h


def get_current_price(symbol: str) -> Optional[float]:
    """
    Busca preço atual na Binance
    
    Args:
        symbol: Símbolo no formato 'BTC/USDT'
    
    Returns:
        Preço atual ou None se erro
    """
    try:
        # Converter formato: BTC/USDT → BTCUSDT
        binance_symbol = symbol.replace('/', '')
        
        response = requests.get(
            f"{BINANCE_API}/ticker/price?symbol={binance_symbol}",
            timeout=5
        )
        response.raise_for_status()
        
        data = response.json()
        price = float(data['price'])
        
        logger.info(f"   💰 {symbol}: ${price:,.2f}")
        return price
        
    except Exception as e:
        logger.error(f"   ❌ Erro ao buscar preço de {symbol}: {e}")
        return None


def check_signal_status(
    direction: str,
    current_price: float,
    entry_min: float,
    entry_max: float,
    targets: list,
    stop_loss: float
) -> Tuple[Optional[str], float]:
    """
    Verifica se sinal atingiu WIN ou LOSS
    
    Args:
        direction: LONG ou SHORT
        current_price: Preço atual do ativo
        entry_min: Entrada mínima
        entry_max: Entrada máxima
        targets: Lista de alvos [{'tp': price, 'percentage': pct}]
        stop_loss: Preço de stop-loss
    
    Returns:
        (novo_status, pnl_percentual)
    """
    entry_avg = (entry_min + entry_max) / 2
    
    # Calcular PnL percentual
    if direction == 'LONG':
        pnl_pct = ((current_price - entry_avg) / entry_avg) * 100
    else:  # SHORT
        pnl_pct = ((entry_avg - current_price) / entry_avg) * 100
    
    # Verificar se atingiu alvo ou stop
    if direction == 'LONG':
        # LONG: Win se preço >= target, Loss se preço <= stop
        hit_target = any(current_price >= float(t['tp']) for t in targets)
        hit_stop = current_price <= float(stop_loss)
    else:
        # SHORT: Win se preço <= target, Loss se preço >= stop
        hit_target = any(current_price <= float(t['tp']) for t in targets)
        hit_stop = current_price >= float(stop_loss)
    
    # Determinar status
    if hit_target:
        return ('WIN', pnl_pct)
    elif hit_stop:
        return ('LOSS', pnl_pct)
    else:
        return (None, pnl_pct)  # Ainda ativo


def update_signal_in_db(
    signal_id: str,
    new_status: str,
    pnl: float
) -> bool:
    """
    Atualiza status e PnL no banco de dados
    
    Args:
        signal_id: UUID do sinal
        new_status: 'WIN' ou 'LOSS'
        pnl: PnL percentual
    
    Returns:
        True se sucesso, False se erro
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        cur.execute("""
            UPDATE alpha_signals 
            SET status = %s, 
                pnl = %s, 
                updated_at = %s 
            WHERE id = %s
        """, (new_status, pnl, datetime.now(), signal_id))
        
        conn.commit()
        cur.close()
        conn.close()
        
        return True
        
    except Exception as e:
        logger.error(f"   ❌ Erro ao atualizar sinal {signal_id}: {e}")
        return False


def check_active_signals() -> Tuple[int, int, int]:
    """
    Verifica todos os sinais ativos e atualiza status
    
    Returns:
        (total_verificados, wins, losses)
    """
    logger.info("=" * 60)
    logger.info("🔍 RESULT TRACKER - Iniciando verificação")
    logger.info("=" * 60)
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        # Buscar sinais ativos das últimas 48h
        cur.execute("""
            SELECT id, symbol, direction, entry_min, entry_max, 
                   targets, stop_loss, created_at 
            FROM alpha_signals 
            WHERE status = 'active'
              AND created_at >= NOW() - INTERVAL '%s hours'
            ORDER BY created_at ASC
        """, (CHECK_AGE_HOURS,))
        
        signals = cur.fetchall()
        total = len(signals)
        
        if total == 0:
            logger.info("✅ Nenhum sinal ativo para verificar")
            cur.close()
            conn.close()
            return (0, 0, 0)
        
        logger.info(f"📊 Sinais ativos encontrados: {total}")
        logger.info("-" * 60)
        
        wins = 0
        losses = 0
        
        for signal in signals:
            (signal_id, symbol, direction, entry_min, entry_max, 
             targets, stop_loss, created_at) = signal
            
            logger.info(f"\n🔍 Analisando sinal {signal_id[:8]}...")
            logger.info(f"   📈 {symbol} {direction}")
            logger.info(f"   💰 Entrada: ${float(entry_min):,.2f} - ${float(entry_max):,.2f}")
            logger.info(f"   🎯 Stop: ${float(stop_loss):,.2f}")
            logger.info(f"   🎯 Targets: {[t['tp'] for t in targets]}")
            
            # Buscar preço atual
            current_price = get_current_price(symbol)
            
            if current_price is None:
                logger.warning(f"   ⚠️ Pulando {symbol} (preço indisponível)")
                continue
            
            # Verificar status
            new_status, pnl = check_signal_status(
                direction=direction,
                current_price=current_price,
                entry_min=float(entry_min),
                entry_max=float(entry_max),
                targets=targets if isinstance(targets, list) else json.loads(targets) if isinstance(targets, str) else [],
                stop_loss=float(stop_loss)
            )
            
            logger.info(f"   📊 PnL Atual: {pnl:+.2f}%")
            
            if new_status:
                # Atualizar no banco
                success = update_signal_in_db(signal_id, new_status, pnl)
                
                if success:
                    if new_status == 'WIN':
                        logger.info(f"   ✅ WIN! ({pnl:+.2f}%)")
                        wins += 1
                    else:
                        logger.info(f"   ❌ LOSS ({pnl:+.2f}%)")
                        losses += 1
                else:
                    logger.error(f"   ❌ Falha ao atualizar status")
            else:
                logger.info(f"   ⏳ Ainda ativo (não atingiu target/stop)")
        
        # Resumo
        logger.info("\n" + "=" * 60)
        logger.info("📈 RESUMO DO TRACKER")
        logger.info("=" * 60)
        logger.info(f"Sinais verificados: {total}")
        logger.info(f"Wins: {wins}")
        logger.info(f"Losses: {losses}")
        logger.info(f"Ainda ativos: {total - wins - losses}")
        
        if wins + losses > 0:
            winrate = (wins / (wins + losses)) * 100
            logger.info(f"Winrate (desta execução): {winrate:.1f}%")
        
        logger.info("\n✅ Tracker concluído!")
        logger.info("=" * 60)
        
        cur.close()
        conn.close()
        
        return (total, wins, losses)
        
    except Exception as e:
        logger.error(f"❌ Erro crítico no tracker: {e}")
        return (0, 0, 0)


def get_winrate_stats() -> dict:
    """
    Busca estatísticas de winrate do banco
    
    Returns:
        Dict com estatísticas
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        cur.execute("""
            SELECT 
                COUNT(*) as total,
                COUNT(*) FILTER (WHERE status = 'WIN') as wins,
                COUNT(*) FILTER (WHERE status = 'LOSS') as losses,
                ROUND(AVG(pnl) FILTER (WHERE status IN ('WIN', 'LOSS')), 2) as avg_pnl,
                ROUND(MAX(pnl) FILTER (WHERE status = 'WIN'), 2) as best_win,
                ROUND(MIN(pnl) FILTER (WHERE status = 'LOSS'), 2) as worst_loss
            FROM alpha_signals
            WHERE status IN ('active', 'WIN', 'LOSS')
        """)
        
        row = cur.fetchone()
        
        if row and row[0] > 0:
            total, wins, losses, avg_pnl, best_win, worst_loss = row
            winrate = (wins / (wins + losses) * 100) if (wins + losses) > 0 else 0
            
            stats = {
                'total': total,
                'wins': wins,
                'losses': losses,
                'active': total - wins - losses,
                'winrate': round(winrate, 2),
                'avg_pnl': float(avg_pnl) if avg_pnl else 0,
                'best_win': float(best_win) if best_win else 0,
                'worst_loss': float(worst_loss) if worst_loss else 0
            }
        else:
            stats = {'total': 0, 'wins': 0, 'losses': 0, 'active': 0, 'winrate': 0}
        
        cur.close()
        conn.close()
        
        return stats
        
    except Exception as e:
        logger.error(f"Erro ao buscar stats: {e}")
        return {}


def main():
    """Main entry point."""
    logger.info("\n" + "=" * 60)
    logger.info("🚀 LEVE IA - RESULT TRACKER")
    logger.info(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    logger.info("=" * 60)
    
    # Executar tracker
    total, wins, losses = check_active_signals()
    
    # Buscar estatísticas gerais
    logger.info("\n📊 ESTATÍSTICAS GERAIS (Histórico)")
    logger.info("-" * 60)
    
    stats = get_winrate_stats()
    
    if stats:
        logger.info(f"Total de sinais: {stats.get('total', 0)}")
        logger.info(f"Wins: {stats.get('wins', 0)}")
        logger.info(f"Losses: {stats.get('losses', 0)}")
        logger.info(f"Ativos: {stats.get('active', 0)}")
        logger.info(f"Winrate: {stats.get('winrate', 0):.2f}%")
        logger.info(f"PnL Médio: {stats.get('avg_pnl', 0):+.2f}%")
        logger.info(f"Melhor Win: {stats.get('best_win', 0):+.2f}%")
        logger.info(f"Pior Loss: {stats.get('worst_loss', 0):+.2f}%")
    
    logger.info("\n" + "=" * 60)
    
    # Se rodando via CLI (não PM2), sair após execução
    if len(sys.argv) > 1 and sys.argv[1] == '--once':
        logger.info("👋 Modo --once: Encerrando após execução única")
        sys.exit(0)
    
    # PM2 mantém o processo vivo para próxima execução do cron
    logger.info("⏳ Aguardando próxima execução (cron PM2)...")


if __name__ == "__main__":
    main()
