#!/usr/bin/env python3
"""
Servidor FastAPI x402 para venda de sinais do Alpha Engine
Arquiteto de Infraestrutura - Leve IA
"""

import json
import os
import time
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from web3 import Web3
from web3.exceptions import TransactionNotFound

# Configurações
WORKSPACE_DIR = os.getenv('WORKSPACE_DIR', '/root/openclaw')
ALPHA_PREDICTION_PATH = os.getenv('ALPHA_PREDICTION_PATH', os.path.join(WORKSPACE_DIR, 'reports/alpha_prediction_latest.json'))
RENATO_WALLET = "0x077e8d29e11ff1c0ccb236e0380d0053dcba2b1c"
PRICE_USDC = 0.10  # $0.10 USDC
PAYMENT_WINDOW_MINUTES = 5

# Configuração da Base Chain
BASE_RPC_URL = "https://mainnet.base.org"
USDC_CONTRACT_ADDRESS = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"  # USDC na Base
USDC_ABI = [
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "type": "function"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "name": "from", "type": "address"},
            {"indexed": True, "name": "to", "type": "address"},
            {"indexed": False, "name": "value", "type": "uint256"}
        ],
        "name": "Transfer",
        "type": "event"
    }
]

# Inicialização do Web3
w3 = Web3(Web3.HTTPProvider(BASE_RPC_URL))
usdc_contract = w3.eth.contract(address=USDC_CONTRACT_ADDRESS, abi=USDC_ABI)

# Modelos Pydantic
class PaymentVerificationRequest(BaseModel):
    tx_hash: str = Field(..., description="Hash da transação USDC")
    user_address: str = Field(..., description="Endereço do usuário que pagou")

class PaymentVerificationResponse(BaseModel):
    verified: bool
    amount_usdc: Optional[float] = None
    timestamp: Optional[int] = None
    message: str

class AlphaPredictionResponse(BaseModel):
    success: bool
    predictions: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    timestamp: int

# Inicialização do FastAPI
app = FastAPI(
    title="Alpha Engine x402 API",
    description="API para venda de sinais do Alpha Engine usando protocolo x402",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Funções auxiliares
def load_alpha_predictions() -> Dict[str, Any]:
    """Carrega as predições do Alpha Engine"""
    try:
        with open(ALPHA_PREDICTION_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Arquivo de predições não encontrado")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Erro ao decodificar predições")

def verify_usdc_payment(tx_hash: str, user_address: str) -> PaymentVerificationResponse:
    """
    Verifica se uma transação USDC foi enviada para a carteira do Renato
    nos últimos 5 minutos.
    
    Lógica simplificada x402:
    1. Verifica se a transação existe
    2. Verifica se foi enviada pelo user_address
    3. Verifica se o destino é a carteira do Renato
    4. Verifica se o valor é >= $0.10 USDC
    5. Verifica se foi nos últimos 5 minutos
    """
    try:
        # Obtém a transação
        tx = w3.eth.get_transaction(tx_hash)
        
        # Verifica se a transação foi bem-sucedida
        tx_receipt = w3.eth.get_transaction_receipt(tx_hash)
        if not tx_receipt.status:
            return PaymentVerificationResponse(
                verified=False,
                message="Transação falhou"
            )
        
        # Verifica se é uma transação de contrato (USDC)
        if tx.to != USDC_CONTRACT_ADDRESS:
            # Pode ser uma transferência direta de ETH, mas precisamos de USDC
            return PaymentVerificationResponse(
                verified=False,
                message="Não é uma transação USDC"
            )
        
        # Obtém os logs da transação para verificar transferência USDC
        logs = tx_receipt.logs
        
        # Procura pelo evento Transfer
        transfer_event = None
        for log in logs:
            try:
                # Tenta decodificar como evento Transfer
                decoded = usdc_contract.events.Transfer().process_log(log)
                if decoded:
                    transfer_event = decoded
                    break
            except:
                continue
        
        if not transfer_event:
            return PaymentVerificationResponse(
                verified=False,
                message="Evento de transferência USDC não encontrado"
            )
        
        # Extrai informações do evento
        from_address = transfer_event['args']['from']
        to_address = transfer_event['args']['to']
        value = transfer_event['args']['value']
        
        # Obtém decimais do USDC
        decimals = usdc_contract.functions.decimals().call()
        amount_usdc = value / (10 ** decimals)
        
        # Verificações
        current_time = int(time.time())
        tx_time = tx_receipt['timestamp'] if 'timestamp' in tx_receipt else current_time
        
        # 1. Verifica se foi enviada pelo user_address
        if from_address.lower() != user_address.lower():
            return PaymentVerificationResponse(
                verified=False,
                message=f"Transação não enviada pelo endereço informado. From: {from_address}"
            )
        
        # 2. Verifica se o destino é a carteira do Renato
        if to_address.lower() != RENATO_WALLET.lower():
            return PaymentVerificationResponse(
                verified=False,
                message=f"Destino não é a carteira do Renato. To: {to_address}"
            )
        
        # 3. Verifica se o valor é suficiente
        if amount_usdc < PRICE_USDC:
            return PaymentVerificationResponse(
                verified=False,
                amount_usdc=amount_usdc,
                message=f"Valor insuficiente. Enviado: ${amount_usdc:.2f} USDC, Requerido: ${PRICE_USDC:.2f} USDC"
            )
        
        # 4. Verifica se foi nos últimos 5 minutos
        time_window = PAYMENT_WINDOW_MINUTES * 60
        if current_time - tx_time > time_window:
            return PaymentVerificationResponse(
                verified=False,
                amount_usdc=amount_usdc,
                timestamp=tx_time,
                message=f"Transação muito antiga. Tempo: {current_time - tx_time}s, Limite: {time_window}s"
            )
        
        # Todas as verificações passaram
        return PaymentVerificationResponse(
            verified=True,
            amount_usdc=amount_usdc,
            timestamp=tx_time,
            message=f"Pagamento verificado! ${amount_usdc:.2f} USDC recebidos"
        )
        
    except TransactionNotFound:
        return PaymentVerificationResponse(
            verified=False,
            message="Transação não encontrada na blockchain"
        )
    except Exception as e:
        return PaymentVerificationResponse(
            verified=False,
            message=f"Erro ao verificar transação: {str(e)}"
        )

# Endpoints
@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "service": "Alpha Engine x402 API",
        "version": "1.0.0",
        "description": "Venda de sinais do Alpha Engine usando protocolo x402",
        "price": f"${PRICE_USDC} USDC",
        "wallet": RENATO_WALLET,
        "network": "Base"
    }

@app.get("/health")
async def health_check():
    """Health check do servidor"""
    return {
        "status": "healthy",
        "timestamp": int(time.time()),
        "web3_connected": w3.is_connected()
    }

@app.post("/verify-payment", response_model=PaymentVerificationResponse)
async def verify_payment(request: PaymentVerificationRequest):
    """
    Verifica se um pagamento USDC foi realizado.
    
    O cliente deve enviar o hash da transação e seu endereço.
    """
    return verify_usdc_payment(request.tx_hash, request.user_address)

@app.get("/alpha-prediction", response_model=AlphaPredictionResponse)
async def get_alpha_prediction(
    tx_hash: Optional[str] = None,
    user_address: Optional[str] = None
):
    """
    Retorna as predições do Alpha Engine após verificação de pagamento.
    
    Parâmetros opcionais:
    - tx_hash: Hash da transação USDC
    - user_address: Endereço do usuário que pagou
    
    Se os parâmetros forem fornecidos, verifica o pagamento antes de retornar as predições.
    """
    # Se não fornecer tx_hash e user_address, retorna erro
    if not tx_hash or not user_address:
        raise HTTPException(
            status_code=400,
            detail="Parâmetros tx_hash e user_address são obrigatórios para acessar as predições"
        )
    
    # Verifica o pagamento
    verification = verify_usdc_payment(tx_hash, user_address)
    
    if not verification.verified:
        raise HTTPException(
            status_code=402,  # Payment Required
            detail=verification.message
        )
    
    # Carrega e retorna as predições
    try:
        predictions = load_alpha_predictions()
        return AlphaPredictionResponse(
            success=True,
            predictions=predictions,
            timestamp=int(time.time())
        )
    except Exception as e:
        return AlphaPredictionResponse(
            success=False,
            error=str(e),
            timestamp=int(time.time())
        )

@app.get("/prediction-sample")
async def get_prediction_sample():
    """
    Retorna uma amostra do formato das predições (sem verificação de pagamento).
    Útil para clientes entenderem o que receberão.
    """
    predictions = load_alpha_predictions()
    
    # Remove dados sensíveis ou simplifica para amostra
    sample = {
        "last_update": predictions.get("last_update"),
        "assets": [p["asset"] for p in predictions.get("predictions", [])],
        "sample_prediction": {
            "asset": predictions["predictions"][0]["asset"] if predictions.get("predictions") else None,
            "current_price": predictions["predictions"][0]["current_price"] if predictions.get("predictions") else None,
            "bias": predictions["predictions"][0]["analysis"]["bias"] if predictions.get("predictions") else None,
            "probability": predictions["predictions"][0]["analysis"]["probability"] if predictions.get("predictions") else None,
        }
    }
    
    return sample

if __name__ == "__main__":
    import uvicorn
    import sys
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8000, help="Porta do servidor")
    args = parser.parse_args()
    
    print("Iniciando servidor Alpha Engine x402...")
    print(f"Preço: ${PRICE_USDC} USDC")
    print(f"Carteira: {RENATO_WALLET}")
    print(f"URL Base RPC: {BASE_RPC_URL}")
    print(f"Porta: {args.port}")
    uvicorn.run(app, host="0.0.0.0", port=args.port)