"""
Blockchain API - Integração com Contrato Ethereum
Conecta ao contrato LeveIA na Ethereum Mainnet via ABI
"""

from web3 import Web3
import json
from typing import Dict, Any, Optional

# Configuração
ETHEREUM_RPC_URL = 'https://eth.llamarpc.com'
CONTRACT_ADDRESS = '0x2333cBC71805b47D64C2867Ef66682c7257B5D4f'

# Carregar ABI
with open('/root/openclaw/contracts/LeveIA_Agent_ABI.json', 'r') as f:
    CONTRACT_ABI = json.load(f)

# Provider singleton
w3 = None
contract = None

def get_web3():
    """Obter instância Web3"""
    global w3
    if not w3:
        w3 = Web3(Web3.HTTPProvider(ETHEREUM_RPC_URL))
    return w3

def get_contract():
    """Obter instância do contrato"""
    global contract
    if not contract:
        w3 = get_web3()
        contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)
    return contract

def check_connection() -> bool:
    """Verificar conexão com Ethereum"""
    w3 = get_web3()
    return w3.is_connected()

def get_audit_count() -> int:
    """Obter total de audits no contrato"""
    try:
        contract = get_contract()
        count = contract.functions.auditCount().call()
        return count
    except Exception as e:
        print(f"Erro ao obter auditCount: {e}")
        return 0

def get_audit(audit_id: int) -> Dict[str, Any]:
    """Obter dados de um audit específico"""
    try:
        contract = get_contract()
        audit = contract.functions.audits(audit_id).call()
        
        return {
            'id': audit_id,
            'timestamp': audit[0],
            'ai_model': audit[1],
            'audit_type': audit[2],
            'findings': audit[3],
            'recommendations': audit[4],
            'severity': audit[5],
            'auditor': audit[6]
        }
    except Exception as e:
        print(f"Erro ao obter audit {audit_id}: {e}")
        return {}

def get_all_audits(limit: int = 100) -> list:
    """Obter todos os audits (até limit)"""
    audits = []
    count = get_audit_count()
    
    for i in range(min(count, limit)):
        audit = get_audit(i)
        if audit:
            audits.append(audit)
    
    return audits

def get_owner() -> str:
    """Obter endereço do owner"""
    try:
        contract = get_contract()
        owner = contract.functions.owner().call()
        return owner
    except Exception as e:
        print(f"Erro ao obter owner: {e}")
        return "0x0000000000000000000000000000000000000000"

def is_paused() -> bool:
    """Verificar se contrato está pausado"""
    try:
        contract = get_contract()
        paused = contract.functions.paused().call()
        return paused
    except Exception as e:
        print(f"Erro ao verificar paused: {e}")
        return False

def get_contract_info() -> Dict[str, Any]:
    """Obter informações completas do contrato"""
    w3 = get_web3()
    
    return {
        'address': CONTRACT_ADDRESS,
        'network': 'Ethereum Mainnet',
        'chain_id': w3.eth.chain_id,
        'block_number': w3.eth.block_number,
        'audit_count': get_audit_count(),
        'owner': get_owner(),
        'paused': is_paused(),
        'connected': check_connection()
    }

# Teste rápido
if __name__ == '__main__':
    print("=== TESTE BLOCKCHAIN API ===\n")
    
    print("1. Verificando conexão...")
    if check_connection():
        print("✅ Conectado à Ethereum Mainnet")
    else:
        print("❌ Não conectado")
        exit(1)
    
    print("\n2. Obtendo informações do contrato...")
    info = get_contract_info()
    print(f"   Endereço: {info['address']}")
    print(f"   Rede: {info['network']}")
    print(f"   Chain ID: {info['chain_id']}")
    print(f"   Bloco atual: {info['block_number']:,}")
    print(f"   Total audits: {info['audit_count']}")
    print(f"   Owner: {info['owner']}")
    print(f"   Pausado: {info['paused']}")
    
    print("\n3. Obtendo audits...")
    audits = get_all_audits(limit=5)
    print(f"   Encontrados: {len(audits)} audits")
    
    for audit in audits:
        print(f"\n   Audit #{audit.get('id', 'N/A')}:")
        print(f"      Type: {audit.get('audit_type', 'N/A')}")
        print(f"      AI Model: {audit.get('ai_model', 'N/A')}")
        print(f"      Severity: {audit.get('severity', 'N/A')}")
    
    print("\n=== TESTE CONCLUÍDO ===")
