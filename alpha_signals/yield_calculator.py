#!/usr/bin/env python3
"""
Yield Calculator - Calcula yield de sinais da Leve IA

Funcionamento:
1. Lê sinais ativos do banco PostgreSQL
2. Busca preço atual (Chainlink ou API externa)
3. Calcula yield (WIN/LOSS)
4. Atualiza banco de dados
5. Registra hash no contrato ProofOfYield (opcional)

Uso:
    python3 yield_calculator.py --calculate
    python3 yield_calculator.py --status
"""

import psycopg2
import requests
import json
import sys
from datetime import datetime
from decimal import Decimal
from web3 import Web3

# Configuração do Banco
DB_CONFIG = {
    'host': '127.0.0.1',
    'port': 5432,
    'database': 'leveclaw',
    'user': 'leveclaw_user',
    'password': 'leveclaw_production_password_2026_change_this'
}

# Configuração Chainlink/Base
BASE_RPC = "https://mainnet.base.org"
CHAINLINK_ETH = "0x71041dddad3595F9CEd3DcCFBe3D1F4b0a16Bb70"

# Configuração ProofOfYield Contract
PROOF_OF_YIELD_ADDRESS = "0x0000000000000000000000000000000000000000"  # Atualizar após deploy
PRIVATE_KEY = "f091abca2de925b91546b09e0fe6e8f970322a1ffd34d159c2851c5c77901dfa"

# APIs de preço (fallback se Chainlink falhar)
PRICE_APIS = {
    "BTC/USDT": "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT",
    "ETH/USDT": "https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT",
    "SOL/USDT": "https://api.binance.com/api/v3/ticker/price?symbol=SOLUSDT",
    "BNB/USDT": "https://api.binance.com/api/v3/ticker/price?symbol=BNBUSDT",
}


def get_db_connection():
    """Obter conexão com banco de dados."""
    return psycopg2.connect(**DB_CONFIG)


def get_current_price(symbol: str) -> Decimal:
    """
    Obter preço atual do ativo.
    
    Tenta Chainlink primeiro, fallback para API externa.
    """
    # Tentar Chainlink para ETH
    if symbol == "ETH/USDT":
        try:
            w3 = Web3(Web3.HTTPProvider(BASE_RPC))
            if w3.is_connected():
                # ABI mínima do Chainlink
                abi = [{
                    "inputs": [],
                    "name": "latestRoundData",
                    "outputs": [
                        {"name": "answer", "type": "int256"},
                    ],
                    "stateMutability": "view",
                    "type": "function"
                }]
                
                contract = w3.eth.contract(address=CHAINLINK_ETH, abi=abi)
                price = contract.functions.latestRoundData().call()[0]
                
                # Chainlink usa 8 decimals
                return Decimal(price) / Decimal(10 ** 8)
        except Exception as e:
            print(f"⚠️ Chainlink falhou: {e}")
    
    # Fallback para API externa
    try:
        # Normalizar símbolo para formato PRICE_APIS (ex: "BTC/USDT")
        normalized_symbol = symbol.replace("/", "")  # Remove barra se existir
        
        # Se símbolo não termina com USDT, adicionar
        if not normalized_symbol.endswith("USDT"):
            normalized_symbol = normalized_symbol + "USDT"
        
        # Tentar primeiro mapeamento direto (ex: "BTC/USDT" -> URL)
        api_url = PRICE_APIS.get(symbol)
        if not api_url:
            # Tentar com formato normalizado sem barra
            symbol_with_slash = f"{normalized_symbol[:-4]}/USDT"
            api_url = PRICE_APIS.get(symbol_with_slash)
        
        # Se ainda não encontrou, construir URL Binance padrão
        if not api_url:
            api_url = f"https://api.binance.com/api/v3/ticker/price?symbol={normalized_symbol}"
        
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        price = Decimal(data['price'])
        
        return price
    except Exception as e:
        print(f"❌ Erro ao obter preço para símbolo '{symbol}': {e}")
        return Decimal(0)


def calculate_yield(entry_price: Decimal, exit_price: Decimal, direction: str) -> Decimal:
    """
    Calcular yield em porcentagem.
    
    Args:
        entry_price: Preço de entrada
        exit_price: Preço de saída (atual)
        direction: "LONG" ou "SHORT"
    
    Returns:
        Yield em porcentagem (positivo = lucro, negativo = prejuízo)
    """
    # Verificação de segurança: evitar divisão por zero
    if entry_price == Decimal(0):
        print(f"⚠️ Preço de entrada zero detectado, retornando yield 0%")
        return Decimal(0)
    
    # Se preço atual é zero (erro na API), não podemos calcular yield
    if exit_price == Decimal(0):
        print(f"⚠️ Preço atual zero detectado, retornando yield 0%")
        return Decimal(0)
    
    try:
        if direction == "LONG":
            # LONG: lucro se preço subiu
            yield_pct = ((exit_price - entry_price) / entry_price) * 100
        else:
            # SHORT: lucro se preço caiu
            yield_pct = ((entry_price - exit_price) / entry_price) * 100
        
        return yield_pct
    except ZeroDivisionError:
        print(f"❌ Erro de divisão por zero (entry_price={entry_price})")
        return Decimal(0)
    except Exception as e:
        print(f"❌ Erro ao calcular yield: {e}")
        return Decimal(0)


def update_signal_yield(conn, signal_id: str, yield_pct: Decimal, current_price: Decimal):
    """
    Atualizar yield do sinal no banco.
    """
    cursor = conn.cursor()
    
    # Determinar status
    if yield_pct > 0:
        status = "WIN"
    elif yield_pct < 0:
        status = "LOSS"
    else:
        status = "BREAKEVEN"
    
    query = """
        UPDATE alpha_signals
        SET pnl = %s,
            status = %s,
            updated_at = NOW()
        WHERE id = %s
        RETURNING *
    """
    
    cursor.execute(query, (float(yield_pct), status, signal_id))
    conn.commit()
    
    updated = cursor.fetchone()
    cursor.close()
    
    return updated


def calculate_all_active_signals():
    """
    Calcular yield para todos os sinais ativos.
    """
    print("="*60)
    print("🧮 YIELD CALCULATOR - LEVE IA")
    print("="*60)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Buscar sinais ativos
    query = """
        SELECT id, symbol, direction, entry_min, entry_max, status, pnl
        FROM alpha_signals
        WHERE status = 'active'
        ORDER BY created_at DESC
        LIMIT 50
    """
    
    cursor.execute(query)
    signals = cursor.fetchall()
    
    print(f"\n📊 Sinais ativos encontrados: {len(signals)}")
    
    results = []
    
    for signal in signals:
        signal_id, symbol, direction, entry_min, entry_max, status, pnl = signal
        
        # Calcular preço médio de entrada
        if entry_min and entry_max:
            entry_price = (Decimal(str(entry_min)) + Decimal(str(entry_max))) / 2
        elif entry_min:
            entry_price = Decimal(str(entry_min))
        else:
            print(f"⚠️ Sinal {signal_id} sem preço de entrada")
            continue
        
        # Obter preço atual
        print(f"\n🔍 Processando {symbol} {direction}...")
        current_price = get_current_price(symbol)
        
        if current_price == 0:
            print(f"   ⚠️ Preço atual indisponível")
            continue
        
        print(f"   Entrada: ${entry_price:,.2f}")
        print(f"   Atual:   ${current_price:,.2f}")
        
        # Calcular yield
        yield_pct = calculate_yield(entry_price, current_price, direction)
        
        print(f"   Yield:   {yield_pct:+.2f}%")
        
        # Atualizar banco
        updated = update_signal_yield(conn, signal_id, yield_pct, current_price)
        
        results.append({
            'signal_id': signal_id,
            'symbol': symbol,
            'direction': direction,
            'entry_price': float(entry_price),
            'current_price': float(current_price),
            'yield_pct': float(yield_pct),
            'status': updated[16] if len(updated) > 16 else status  # status column
        })
        
        # Imprimir resultado
        if yield_pct > 0:
            print(f"   ✅ WIN! +{yield_pct:.2f}%")
        elif yield_pct < 0:
            print(f"   ❌ LOSS {yield_pct:.2f}%")
        else:
            print(f"   ➖ BREAKEVEN")
    
    cursor.close()
    conn.close()
    
    # Resumo
    print("\n" + "="*60)
    print("📈 RESUMO")
    print("="*60)
    
    total_signals = len(results)
    wins = sum(1 for r in results if r['yield_pct'] > 0)
    losses = sum(1 for r in results if r['yield_pct'] < 0)
    total_yield = sum(r['yield_pct'] for r in results)
    
    print(f"Total de sinais: {total_signals}")
    print(f"Wins: {wins} ({wins/total_signals*100:.1f}%)")
    print(f"Losses: {losses} ({losses/total_signals*100:.1f}%)")
    print(f"Yield total: {total_yield:+.2f}%")
    print(f"Yield médio: {total_yield/total_signals:+.2f}%")
    
    print("\n✅ Cálculo concluído!")
    
    return results


def get_status():
    """
    Mostrar status atual dos sinais.
    """
    print("="*60)
    print("📊 STATUS DOS SINAIS - LEVE IA")
    print("="*60)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
        SELECT 
            status,
            COUNT(*) as count,
            COALESCE(AVG(pnl), 0) as avg_pnl,
            COALESCE(SUM(pnl), 0) as total_pnl
        FROM alpha_signals
        GROUP BY status
        ORDER BY count DESC
    """
    
    cursor.execute(query)
    results = cursor.fetchall()
    
    print("\nStatus | Count | Avg PnL | Total PnL")
    print("-------|-------|---------|----------")
    
    for row in results:
        status, count, avg_pnl, total_pnl = row
        print(f"{status:6} | {count:5} | {avg_pnl:+7.2f}% | {total_pnl:+9.2f}%")
    
    cursor.close()
    conn.close()


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Uso: python3 yield_calculator.py --calculate | --status")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "--calculate":
        calculate_all_active_signals()
    elif command == "--status":
        get_status()
    else:
        print(f"Comando desconhecido: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
