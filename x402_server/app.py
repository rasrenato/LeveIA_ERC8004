#!/usr/bin/env python3
"""
Servidor Flask com x402 para monetização do Alpha Engine da Leve IA
"""

from flask import Flask, jsonify, request, Response
import json
import os
import base64
from datetime import datetime, timedelta
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configurações
MERCHANT_WALLET = os.getenv("MERCHANT_WALLET", "0x077e8d29e11ff1c0ccb236e0380d0053dcba2b1c")
PRICE_USDC = float(os.getenv("PRICE_USDC", "0.01"))  # $0.01 por requisição
NETWORK = os.getenv("NETWORK", "eip155:8453")  # Base network
WORKSPACE_DIR = os.getenv("WORKSPACE_DIR", "/root/openclaw")
PREDICTIONS_FILE = os.getenv("PREDICTIONS_FILE", os.path.join(WORKSPACE_DIR, "reports/alpha_prediction_latest.json"))

# Facilitator da Coinbase (sandbox para testes)
FACILITATOR_URL = os.getenv("FACILITATOR_URL", "https://facilitator.cdp.coinbase.com")

def load_predictions():
    """Carrega as previsões do arquivo JSON"""
    try:
        with open(PREDICTIONS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"Arquivo de previsões não encontrado: {PREDICTIONS_FILE}")
        return {"error": "Predictions file not found", "last_update": None, "predictions": []}
    except json.JSONDecodeError as e:
        logger.error(f"Erro ao decodificar JSON: {e}")
        return {"error": "Invalid predictions file", "last_update": None, "predictions": []}

def create_payment_requirements():
    """Cria os requisitos de pagamento no formato x402"""
    expires_at = (datetime.utcnow() + timedelta(minutes=5)).isoformat() + "Z"
    
    requirements = {
        "scheme": "exact",
        "network": NETWORK,
        "amount": str(PRICE_USDC),
        "currency": "USDC",
        "recipient": MERCHANT_WALLET,
        "description": "Leve IA Alpha Engine Predictions - Crypto Market Signals",
        "expires_at": expires_at,
        "metadata": {
            "service": "alpha_engine",
            "version": "1.0",
            "provider": "Leve IA"
        }
    }
    
    return requirements

def encode_payment_requirements(requirements):
    """Codifica os requisitos de pagamento para header HTTP"""
    requirements_json = json.dumps(requirements)
    return base64.b64encode(requirements_json.encode()).decode()

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de health check"""
    return jsonify({
        "status": "healthy",
        "service": "Leve IA Alpha Engine x402",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    })

@app.route('/api/v1/alpha/predictions', methods=['GET'])
def get_predictions():
    """
    Endpoint protegido por x402 para sinais do Alpha Engine
    
    Fluxo:
    1. Cliente faz requisição GET
    2. Servidor responde 402 com requisitos de pagamento
    3. Cliente assina pagamento e reenvia com PAYMENT-SIGNATURE
    4. Servidor verifica e retorna previsões se válido
    """
    
    # Verifica se há assinatura de pagamento
    payment_signature = request.headers.get('PAYMENT-SIGNATURE')
    
    if not payment_signature:
        # Primeira requisição - retorna 402 com requisitos de pagamento
        requirements = create_payment_requirements()
        encoded_requirements = encode_payment_requirements(requirements)
        
        logger.info(f"402 Payment Required para cliente {request.remote_addr}")
        
        response = Response(
            response=json.dumps({
                "error": "Payment required",
                "message": "Please sign the payment to access Alpha Engine predictions",
                "price": f"{PRICE_USDC} USDC",
                "merchant": MERCHANT_WALLET,
                "network": NETWORK
            }),
            status=402,
            mimetype='application/json'
        )
        
        response.headers['PAYMENT-REQUIRED'] = encoded_requirements
        response.headers['Access-Control-Expose-Headers'] = 'PAYMENT-REQUIRED'
        
        return response
    
    # TODO: Implementar verificação real da assinatura via Facilitator
    # Por enquanto, aceita qualquer assinatura para testes
    logger.info(f"Pagamento recebido de {request.remote_addr}, assinatura: {payment_signature[:20]}...")
    
    # Carrega e retorna as previsões
    predictions = load_predictions()
    
    # Adiciona metadados da transação
    if "error" not in predictions:
        predictions["x402_metadata"] = {
            "payment_received": True,
            "payment_amount": PRICE_USDC,
            "payment_currency": "USDC",
            "timestamp": datetime.utcnow().isoformat()
        }
    
    return jsonify(predictions)

@app.route('/api/v1/alpha/predictions/<asset>', methods=['GET'])
def get_prediction_for_asset(asset):
    """Endpoint para previsão específica de um ativo"""
    
    # Verifica se há assinatura de pagamento
    payment_signature = request.headers.get('PAYMENT-SIGNATURE')
    
    if not payment_signature:
        requirements = create_payment_requirements()
        encoded_requirements = encode_payment_requirements(requirements)
        
        response = Response(
            response=json.dumps({
                "error": "Payment required",
                "message": f"Please sign the payment to access {asset} prediction",
                "price": f"{PRICE_USDC} USDC",
                "asset": asset.upper()
            }),
            status=402,
            mimetype='application/json'
        )
        
        response.headers['PAYMENT-REQUIRED'] = encoded_requirements
        response.headers['Access-Control-Expose-Headers'] = 'PAYMENT-REQUIRED'
        
        return response
    
    # Carrega previsões
    predictions_data = load_predictions()
    
    if "error" in predictions_data:
        return jsonify(predictions_data), 404
    
    # Filtra por ativo
    asset_upper = asset.upper()
    for prediction in predictions_data.get("predictions", []):
        if prediction.get("asset") == asset_upper:
            # Adiciona metadados da transação
            prediction["x402_metadata"] = {
                "payment_received": True,
                "payment_amount": PRICE_USDC,
                "payment_currency": "USDC",
                "timestamp": datetime.utcnow().isoformat()
            }
            return jsonify(prediction)
    
    return jsonify({
        "error": "Asset not found",
        "message": f"No prediction available for {asset}",
        "available_assets": [p.get("asset") for p in predictions_data.get("predictions", [])]
    }), 404

@app.route('/api/v1/info', methods=['GET'])
def get_service_info():
    """Retorna informações sobre o serviço"""
    predictions = load_predictions()
    asset_count = len(predictions.get("predictions", [])) if "error" not in predictions else 0
    
    return jsonify({
        "service": "Leve IA Alpha Engine",
        "version": "1.0.0",
        "monetization": "x402 Pay-Per-Use",
        "price_per_request": f"{PRICE_USDC} USDC",
        "network": NETWORK,
        "merchant_wallet": MERCHANT_WALLET,
        "available_assets": asset_count,
        "last_update": predictions.get("last_update") if "error" not in predictions else None,
        "endpoints": {
            "predictions": "/api/v1/alpha/predictions",
            "asset_prediction": "/api/v1/alpha/predictions/{asset}",
            "health": "/health",
            "info": "/api/v1/info"
        }
    })

if __name__ == '__main__':
    # Verifica se o arquivo de previsões existe
    if not os.path.exists(PREDICTIONS_FILE):
        logger.warning(f"Arquivo de previsões não encontrado: {PREDICTIONS_FILE}")
        logger.warning("O serviço funcionará, mas retornará erro ao acessar previsões")
    
    logger.info(f"Iniciando Leve IA Alpha Engine x402 Server")
    logger.info(f"Merchant Wallet: {MERCHANT_WALLET}")
    logger.info(f"Preço: {PRICE_USDC} USDC por requisição")
    logger.info(f"Rede: {NETWORK}")
    logger.info(f"Arquivo de previsões: {PREDICTIONS_FILE}")
    
    app.run(
        host=os.getenv('HOST', '0.0.0.0'),
        port=int(os.getenv('PORT', 5000)),
        debug=os.getenv('DEBUG', 'false').lower() == 'true'
    )