#!/usr/bin/env python3
"""
Servidor Flask com integração x402 para monetização dos sinais do Alpha Engine.
Endpoint protegido que requer pagamento em USDC na rede Base.
"""

from flask import Flask, jsonify, request
import json
import os
import logging
from datetime import datetime
from typing import Dict, Any, Optional

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configurações
MERCHANT_WALLET = os.getenv('MERCHANT_WALLET', '0x077e8d29e11ff1c0ccb236e0380d0053dcba2b1c')
PRICE_USDC = float(os.getenv('PRICE_USDC', '0.01'))  # $0.01 por acesso
WORKSPACE_DIR = os.getenv('WORKSPACE_DIR', '/root/openclaw')
PREDICTION_FILE = os.getenv('PREDICTION_FILE', os.path.join(WORKSPACE_DIR, 'reports/alpha_prediction_latest.json'))
SERVER_PORT = int(os.getenv('SERVER_PORT', '5000'))
SERVER_HOST = os.getenv('SERVER_HOST', '0.0.0.0')

# Banco de dados simples para tracking (em produção, use um banco real)
payments_db = {}

def load_predictions() -> Dict[str, Any]:
    """Carregar previsões do Alpha Engine"""
    try:
        with open(PREDICTION_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"Prediction file not found: {PREDICTION_FILE}")
        return {"error": "Predictions not available", "last_update": None, "predictions": []}
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON in prediction file: {PREDICTION_FILE}")
        return {"error": "Invalid prediction data", "last_update": None, "predictions": []}

def verify_payment_signature(signature: str) -> bool:
    """
    Verificar assinatura de pagamento x402.
    Em produção, integre com a biblioteca x402 oficial.
    """
    # TODO: Implementar verificação real com x402 library
    # Por enquanto, aceita qualquer assinatura para testes
    logger.info(f"Verifying payment signature: {signature[:20]}...")
    
    # Simulação: verificar formato básico
    if signature and len(signature) > 10:
        payment_id = f"pay_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(payments_db)}"
        payments_db[payment_id] = {
            'signature': signature,
            'timestamp': datetime.now().isoformat(),
            'amount_usdc': PRICE_USDC,
            'merchant_wallet': MERCHANT_WALLET,
            'status': 'verified'
        }
        return True
    return False

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de health check"""
    return jsonify({
        'status': 'healthy',
        'service': 'leve-ia-x402-server',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.route('/alpha/signals', methods=['GET'])
def get_alpha_signals():
    """Endpoint protegido por x402 para sinais do Alpha Engine"""
    
    # Log da requisição
    client_ip = request.remote_addr
    user_agent = request.headers.get('User-Agent', 'Unknown')
    logger.info(f"Request from {client_ip} - {user_agent}")
    
    # Verificar se há assinatura de pagamento
    payment_signature = request.headers.get('PAYMENT-SIGNATURE')
    
    if payment_signature:
        # Verificar pagamento
        if verify_payment_signature(payment_signature):
            # Pagamento válido, liberar dados
            predictions = load_predictions()
            
            # Adicionar metadados da transação
            predictions['x402_metadata'] = {
                'payment_verified': True,
                'amount_paid_usdc': PRICE_USDC,
                'merchant_wallet': MERCHANT_WALLET,
                'access_timestamp': datetime.now().isoformat()
            }
            
            logger.info(f"Payment verified, serving predictions to {client_ip}")
            return jsonify(predictions)
        else:
            # Pagamento inválido
            logger.warning(f"Invalid payment signature from {client_ip}")
            return jsonify({
                'error': 'Payment verification failed',
                'code': 'INVALID_PAYMENT',
                'message': 'The payment signature could not be verified'
            }), 402
    
    # Sem assinatura, retornar requisitos de pagamento (x402)
    logger.info(f"Payment required for {client_ip}")
    
    payment_requirements = {
        'payment_required': True,
        'amount_usdc': PRICE_USDC,
        'merchant_wallet': MERCHANT_WALLET,
        'description': 'Alpha Engine Signals - Latest cryptocurrency predictions',
        'network': 'base',
        'token': 'USDC',
        'token_address': '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913',  # USDC no Base
        'scheme': 'exact',
        'expires_at': (datetime.now().timestamp() + 300),  # 5 minutos
        'instructions': {
            'client': 'Include PAYMENT-SIGNATURE header in retry',
            'amount': f'{PRICE_USDC} USDC',
            'network': 'Base Mainnet',
            'api_docs': 'https://docs.x402.org'
        }
    }
    
    # Headers x402
    headers = {
        'PAYMENT-REQUIRED': 'true',
        'X-Payment-Amount': str(PRICE_USDC),
        'X-Payment-Currency': 'USDC',
        'X-Payment-Network': 'base',
        'X-Payment-Merchant': MERCHANT_WALLET
    }
    
    return jsonify(payment_requirements), 402, headers

@app.route('/payments', methods=['GET'])
def list_payments():
    """Endpoint para listar pagamentos recebidos (admin)"""
    # Em produção, proteja este endpoint com autenticação
    return jsonify({
        'total_payments': len(payments_db),
        'total_revenue_usdc': len(payments_db) * PRICE_USDC,
        'payments': payments_db,
        'merchant_wallet': MERCHANT_WALLET
    })

@app.route('/config', methods=['GET'])
def get_config():
    """Endpoint para obter configuração atual"""
    return jsonify({
        'merchant_wallet': MERCHANT_WALLET,
        'price_usdc': PRICE_USDC,
        'prediction_file': PREDICTION_FILE,
        'network': 'base',
        'token': 'USDC',
        'service_status': 'active'
    })

if __name__ == '__main__':
    logger.info(f"🚀 Starting Leve IA x402 Server")
    logger.info(f"   Merchant Wallet: {MERCHANT_WALLET}")
    logger.info(f"   Price per request: ${PRICE_USDC} USDC")
    logger.info(f"   Prediction file: {PREDICTION_FILE}")
    logger.info(f"   Server: {SERVER_HOST}:{SERVER_PORT}")
    
    app.run(host=SERVER_HOST, port=SERVER_PORT, debug=True)