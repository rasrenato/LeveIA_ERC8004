from flask import Flask, request, jsonify, abort
import json
import os
import time
import requests
from web3 import Web3

app = Flask(__name__)

# Configurações de Infraestrutura da Leve IA
USDC_BASE_ADDRESS = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
RENATO_WALLET = "0x077e8d29e11ff1c0ccb236e0380d0053dcba2b1c"
PRICE_USDC = 1.0  # 1 USDC por sinal
BASE_RPC = "https://mainnet.base.org"

w3 = Web3(Web3.HTTPProvider(BASE_RPC))

# ABI mínima para USDC (ERC20 Transfer event)
ERC20_ABI = json.loads('[{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"}]')

def verify_payment(tx_hash, sender_address):
    """
    Verifica se o tx_hash é um envio válido de USDC para a carteira do Renato na rede Base.
    """
    try:
        receipt = w3.eth.get_transaction_receipt(tx_hash)
        if not receipt or not receipt['status']:
            return False

        usdc_contract = w3.eth.contract(address=USDC_BASE_ADDRESS, abi=ERC20_ABI)
        logs = usdc_contract.events.Transfer().process_receipt(receipt)
        
        for log in logs:
            # USDC no Base tem 6 decimais
            amount = log['args']['value'] / 1e6
            to_address = log['args']['to'].lower()
            from_address = log['args']['from'].lower()
            
            if to_address == RENATO_WALLET.lower() and from_address == sender_address.lower() and amount >= PRICE_USDC:
                return True
    except Exception as e:
        print(f"Erro na verificação: {e}")
    return False

@app.route('/api/v1/alpha-signal', methods=['GET'])
def get_alpha_signal():
    # 1. Extrair headers do protocolo x402
    tx_hash = request.headers.get('X-402-Payment-Hash')
    sender = request.headers.get('X-402-Sender')

    # 2. Se não houver pagamento, retorna 402 Payment Required
    if not tx_hash or not sender:
        return jsonify({
            "error": "Payment Required",
            "amount": PRICE_USDC,
            "currency": "USDC",
            "network": "Base",
            "recipient": RENATO_WALLET,
            "instruction": "Efetue o pagamento de 1 USDC para o endereço indicado e envie o hash no header 'X-402-Payment-Hash'"
        }), 402

    # 3. Verificar pagamento on-chain
    if not verify_payment(tx_hash, sender):
        return jsonify({"error": "Pagamento não verificado ou inválido"}), 402

    # 4. Se pago, liberar o recurso do alpha_engine.py
    report_path = "/root/openclaw/reports/alpha_prediction_latest.json"
    if os.path.exists(report_path):
        with open(report_path, 'r') as f:
            data = json.load(f)
        return jsonify(data)
    else:
        return jsonify({"error": "Sinal ainda não gerado pela engine"}), 503

if __name__ == '__main__':
    # Em produção, rodar com Gunicorn
    app.run(host='0.0.0.0', port=5000)
