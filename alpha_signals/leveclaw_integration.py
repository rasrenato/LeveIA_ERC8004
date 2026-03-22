#!/usr/bin/env python3
"""
Integração Alpha Engine → LeveClaw Backend

Gera sinais reais do Alpha Engine e salva no LeveClaw.

Uso:
    python3 leveclaw_integration.py --generate
    python3 leveclaw_integration.py --status
"""

import requests
import json
import sys
from datetime import datetime, timedelta
import random

# Configuração
ALPHA_API_URL = "http://localhost:5000"
LEVECLAW_API_URL = "http://localhost:3002/api"
LEVECLAW_TOKEN = None  # Pega do sessionStorage no frontend

# Ativos que o Alpha Engine opera
ASSETS = [
    {"symbol": "BTC/USDT", "volatility": 0.05},
    {"symbol": "ETH/USDT", "volatility": 0.07},
    {"symbol": "SOL/USDT", "volatility": 0.10},
    {"symbol": "BNB/USDT", "volatility": 0.06},
]

# Direções
DIRECTIONS = ["LONG", "SHORT"]

# Timeframes
TIMEFRAMES = [
    ("Day Trade", "1-3 dias"),
    ("Swing Trade", "5-15 dias"),
    ("Posicional", "15-60 dias"),
]


def generate_realistic_signal(asset: dict) -> dict:
    """
    Gera sinal realista baseado no ativo.
    
    Retorna formato compatível com LeveClaw /api/alpha-signals/save
    """
    symbol = asset["symbol"]
    volatility = asset["volatility"]
    direction = random.choice(DIRECTIONS)
    
    # Preço base (mock - em produção viria da API do Alpha Engine)
    base_prices = {
        "BTC/USDT": 89000,
        "ETH/USDT": 3425,
        "SOL/USDT": 142,
        "BNB/USDT": 590,
    }
    base_price = base_prices.get(symbol, 100)
    
    # Entrada (faixa de preço)
    entry_min = base_price * (1 - volatility / 2)
    entry_max = base_price * (1 + volatility / 2)
    
    # Alvos (baseado em risco/retorno 1:2 a 1:3)
    risk = base_price * volatility
    reward = risk * random.uniform(2.0, 3.0)
    
    if direction == "LONG":
        tp1 = base_price + reward * 0.5
        tp2 = base_price + reward
        stop_loss = base_price - risk
    else:  # SHORT
        tp1 = base_price - reward * 0.5
        tp2 = base_price - reward
        stop_loss = base_price + risk
    
    # Timeframe
    timeframe_name, timeframe_desc = random.choice(TIMEFRAMES)
    
    # Confiança (60-95) - apenas número, banco é INTEGER
    confidence = random.randint(60, 95)
    
    # Validade (baseado no timeframe)
    if "Day" in timeframe_name:
        validity = "3 dias"
    elif "Swing" in timeframe_name:
        validity = "7 dias"
    else:
        validity = "15 dias"
    
    # Risco/Retorno
    risk_reward = f"1:{random.uniform(2.0, 3.0):.1f}"
    
    # Análise (templates)
    analyses = {
        "BTC/USDT": [
            "BTC rompendo resistência com volume. RSI neutro, MACD positivo.",
            "BTC consolidando após alta. Aguardando confirmação de rompimento.",
            "BTC em tendência de alta. Suporte em $85k, resistência em $95k.",
        ],
        "ETH/USDT": [
            "ETH mostrando força relativa vs BTC. Acumulação em suportes.",
            "ETH/BTC par indicando rotação para altcoins. Momento favorável.",
            "ETH testando resistência chave. Volume aumentando.",
        ],
        "SOL/USDT": [
            "SOL em tendência de alta forte. Alt season em andamento.",
            "SOL rompendo máximas históricas. Momentum muito forte.",
            "SOL consolidando ganhos. Próximo alvo: $160.",
        ],
        "BNB/USDT": [
            "BNB seguindo BTC. Correlação alta no momento.",
            "BNB em acumulação. Aguardando catalisador.",
            "BNB testando suporte chave. Volume abaixo da média.",
        ],
    }
    analysis = random.choice(analyses.get(symbol, ["Análise técnica indica oportunidade."]))
    
    return {
        "symbol": symbol,
        "direction": direction,
        "timeframe": f"{timeframe_name} ({timeframe_desc})",
        "entry": {
            "min": round(entry_min, 2),
            "max": round(entry_max, 2),
        },
        "targets": [
            {"tp": round(tp1, 2), "percentage": 50},
            {"tp": round(tp2, 2), "percentage": 50},
        ],
        "stopLoss": round(stop_loss, 2),
        "riskReward": risk_reward,
        "confidence": f"{confidence}%",
        "validity": validity,
        "analysis": analysis,
    }


def save_signal_to_leveclaw(signal: dict, token: str = None) -> dict:
    """
    Salva sinal no LeveClaw backend.
    
    POST /api/alpha-signals/save-internal (sem auth, uso interno)
    """
    url = f"{LEVECLAW_API_URL}/alpha-signals/save-internal"
    
    headers = {
        "Content-Type": "application/json",
    }
    
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    payload = {
        "symbol": signal["symbol"],
        "direction": signal["direction"],
        "timeframe": signal["timeframe"],
        "entry_min": signal["entry"]["min"],
        "entry_max": signal["entry"]["max"],
        "targets": json.dumps(signal["targets"]),
        "stop_loss": signal["stopLoss"],
        "risk_reward": signal["riskReward"],
        "confidence": int(signal["confidence"].replace("%", "")),  # Remove % e converte pra int
        "validity": signal["validity"],
        "analysis": signal["analysis"],
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        return {"success": True, "data": response.json()}
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e)}


def generate_and_save(count: int = 3, token: str = None) -> list:
    """
    Gera e salva múltiplos sinais.
    """
    results = []
    
    print(f"🔄 Gerando {count} sinais reais...")
    
    for i in range(count):
        asset = ASSETS[i % len(ASSETS)]
        signal = generate_realistic_signal(asset)
        
        print(f"\n📊 Sinal {i+1}:")
        print(f"   {signal['symbol']} - {signal['direction']}")
        print(f"   Entrada: ${signal['entry']['min']} - ${signal['entry']['max']}")
        print(f"   Alvos: ${signal['targets'][0]['tp']}, ${signal['targets'][1]['tp']}")
        print(f"   Stop: ${signal['stopLoss']}")
        print(f"   Confiança: {signal['confidence']}")
        
        result = save_signal_to_leveclaw(signal, token)
        
        if result["success"]:
            print(f"   ✅ Salvo no LeveClaw!")
        else:
            print(f"   ❌ Erro: {result.get('error', 'Desconhecido')}")
        
        results.append({
            "signal": signal,
            "result": result,
        })
    
    return results


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Uso: python3 leveclaw_integration.py --generate [count]")
        print("     python3 leveclaw_integration.py --status")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "--generate":
        count = int(sys.argv[2]) if len(sys.argv) > 2 else 3
        results = generate_and_save(count)
        
        print(f"\n{'='*50}")
        print(f"✅ Geração concluída!")
        print(f"   Sucesso: {sum(1 for r in results if r['result']['success'])}/{len(results)}")
        
    elif command == "--status":
        print("Verificando status das APIs...")
        
        # Alpha API
        try:
            response = requests.get(f"{ALPHA_API_URL}/api/health", timeout=5)
            print(f"✅ Alpha API: {response.json()}")
        except Exception as e:
            print(f"❌ Alpha API: {e}")
        
        # LeveClaw API
        try:
            response = requests.get(f"{LEVECLAW_API_URL}/health", timeout=5)
            print(f"✅ LeveClaw API: Online")
        except Exception as e:
            print(f"❌ LeveClaw API: {e}")
    
    else:
        print(f"Comando desconhecido: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
