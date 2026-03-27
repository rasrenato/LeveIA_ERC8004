#!/usr/bin/env python3
"""
Testar Chainlink Oracle na Base Mainnet

Endpoints:
- BTC/USD: 0xF4030086522a5bEEa4988F8cA5B36dbC97BeE88c
- ETH/USD: 0x71041dddad3595F9CEd3DcCFBe3D1F4b0a16Bb70
"""

from web3 import Web3
import json

# Configuração
BASE_RPC = "https://mainnet.base.org"
CHAINLINK_BTC = "0xF4030086522a5bEEa4988F8cA5B36dbC97BeE88c"
CHAINLINK_ETH = "0x71041dddad3595F9CEd3DcCFBe3D1F4b0a16Bb70"

# ABI mínima do Chainlink
CHAINLINK_ABI = [
    {
        "inputs": [],
        "name": "latestRoundData",
        "outputs": [
            {"internalType": "uint80", "name": "roundId", "type": "uint80"},
            {"internalType": "int256", "name": "answer", "type": "int256"},
            {"internalType": "uint256", "name": "startedAt", "type": "uint256"},
            {"internalType": "uint256", "name": "updatedAt", "type": "uint256"},
            {"internalType": "uint80", "name": "answeredInRound", "type": "uint80"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "decimals",
        "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
        "stateMutability": "view",
        "type": "function"
    }
]

def main():
    print("="*60)
    print("🔗 TESTANDO CHAINLINK ORACLE - BASE MAINNET")
    print("="*60)
    
    # Conectar à Base Mainnet
    print("\n1️⃣ Conectando à Base Mainnet...")
    w3 = Web3(Web3.HTTPProvider(BASE_RPC))
    
    if w3.is_connected():
        print(f"   ✅ Conectado!")
        print(f"   📊 Chain ID: {w3.eth.chain_id}")
        print(f"   📈 Último bloco: {w3.eth.block_number}")
    else:
        print(f"   ❌ Falhou!")
        return
    
    # Testar BTC/USD
    print("\n2️⃣ Testando BTC/USD Feed...")
    btc_contract = w3.eth.contract(address=CHAINLINK_BTC, abi=CHAINLINK_ABI)
    
    try:
        decimals = btc_contract.functions.decimals().call()
        round_data = btc_contract.functions.latestRoundData().call()
        
        price = round_data[1] / (10 ** decimals)
        updated_at = round_data[3]
        
        print(f"   ✅ BTC/USD: ${price:,.2f}")
        print(f"   🕐 Atualizado: {updated_at}")
        print(f"   🔢 Decimals: {decimals}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    # Testar ETH/USD
    print("\n3️⃣ Testando ETH/USD Feed...")
    eth_contract = w3.eth.contract(address=CHAINLINK_ETH, abi=CHAINLINK_ABI)
    
    try:
        decimals = eth_contract.functions.decimals().call()
        round_data = eth_contract.functions.latestRoundData().call()
        
        price = round_data[1] / (10 ** decimals)
        updated_at = round_data[3]
        
        print(f"   ✅ ETH/USD: ${price:,.2f}")
        print(f"   🕐 Atualizado: {updated_at}")
        print(f"   🔢 Decimals: {decimals}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    print("\n" + "="*60)
    print("✅ TESTE CONCLUÍDO!")
    print("="*60)

if __name__ == "__main__":
    main()
