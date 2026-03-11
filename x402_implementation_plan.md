# Plano de Implementação do Protocolo x402 para Leve IA

## 📋 Visão Geral
Implementação do protocolo x402 da Coinbase para monetização dos sinais do Alpha Engine da Leve IA, seguindo o modelo 'Pay-Per-Use' validado pela CoinGecko.

## 🎯 Objetivos
1. Criar endpoint protegido por pagamento para acesso aos sinais do Alpha Engine
2. Implementar fluxo de pagamento automático em USDC na rede Base
3. Fornecer script cliente para consumo automatizado por agentes de IA
4. Utilizar carteira do Renato como Merchant Wallet

## 🔧 Arquitetura Técnica

### 1. Servidor Flask com x402
- **Framework**: Flask (leve e rápido)
- **Protocolo**: x402 v2.0.0
- **Rede**: Base (eip155:8453)
- **Token**: USDC
- **Preço**: $0.01 por requisição (modelo CoinGecko)

### 2. Endpoint Principal
- **URL**: `/api/v1/alpha/predictions`
- **Método**: GET
- **Resposta**: JSON do arquivo `/root/openclaw/reports/alpha_prediction_latest.json`
- **Proteção**: 402 Payment Required

### 3. Fluxo de Pagamento
```
Cliente → GET /predictions → 402 Payment Required
Cliente → Assina pagamento USDC → GET /predictions com PAYMENT-SIGNATURE
Servidor → Verifica via Facilitator → 200 OK + JSON
```

## 📁 Estrutura de Arquivos

```
/root/openclaw/x402_implementation/
├── server/
│   ├── app.py              # Servidor Flask com x402
│   ├── requirements.txt    # Dependências
│   └── config.py          # Configurações
├── client/
│   ├── alpha_client.py    # Cliente Python para consumo
│   └── example_usage.py   # Exemplo de uso
└── docs/
    └── api_spec.md        # Documentação da API
```

## 🚀 Implementação

### Passo 1: Configurar Servidor Flask com x402

```python
# server/app.py
from flask import Flask, jsonify
from x402.mechanisms.evm import EVMSigner
from x402.mechanisms.evm.schemes.exact import ExactEVMPayment
import json
import os

app = Flask(__name__)

# Configurações
MERCHANT_WALLET = "0x077e8d29e11ff1c0ccb236e0380d0053dcba2b1c"
PRICE_USDC = 0.01  # $0.01 por requisição
NETWORK = "eip155:8453"  # Base network
FACILITATOR_URL = "https://facilitator.cdp.coinbase.com"

@app.route('/api/v1/alpha/predictions', methods=['GET'])
def get_predictions():
    """Endpoint protegido por x402 para sinais do Alpha Engine"""
    # Lógica de verificação de pagamento via x402
    # Retorna 402 se não houver pagamento válido
    # Retorna JSON dos sinais se pagamento válido
    
    try:
        with open('/root/openclaw/reports/alpha_prediction_latest.json', 'r') as f:
            predictions = json.load(f)
        return jsonify(predictions)
    except FileNotFoundError:
        return jsonify({"error": "Predictions file not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

### Passo 2: Implementar Middleware x402

```python
# server/x402_middleware.py
from x402 import PaymentRequired, PaymentVerifier
from x402.mechanisms.evm.schemes.exact import ExactEVMPayment
import base64
import json

class X402Middleware:
    def __init__(self, merchant_wallet, price_usdc, network):
        self.merchant_wallet = merchant_wallet
        self.price_usdc = price_usdc
        self.network = network
        
    def create_payment_requirements(self):
        """Cria requisitos de pagamento para resposta 402"""
        requirements = {
            "scheme": "exact",
            "network": self.network,
            "amount": str(self.price_usdc),
            "currency": "USDC",
            "recipient": self.merchant_wallet,
            "description": "Leve IA Alpha Engine Predictions",
            "expires_at": None  # Sem expiração
        }
        return requirements
    
    def verify_payment(self, payment_signature_header):
        """Verifica assinatura de pagamento"""
        # Decodifica header PAYMENT-SIGNATURE
        # Verifica via Facilitator da Coinbase
        # Retorna True se válido
        pass
```

### Passo 3: Cliente Python para Consumo

```python
# client/alpha_client.py
import httpx
from x402 import X402Client
from x402.mechanisms.evm import EVMSigner
import json

class AlphaEngineClient:
    def __init__(self, private_key, rpc_url="https://mainnet.base.org"):
        self.private_key = private_key
        self.rpc_url = rpc_url
        self.base_url = "http://localhost:5000"  # URL do servidor
        
        # Inicializa cliente x402
        self.signer = EVMSigner(private_key)
        self.client = X402Client(signer=self.signer)
    
    def get_predictions(self):
        """Obtém previsões do Alpha Engine com pagamento automático"""
        url = f"{self.base_url}/api/v1/alpha/predictions"
        
        try:
            # Primeira tentativa (espera 402)
            response = httpx.get(url)
            
            if response.status_code == 402:
                # Processa pagamento x402
                payment_required = response.headers.get('PAYMENT-REQUIRED')
                if payment_required:
                    # Cria e assina pagamento
                    payment = self.client.create_payment(payment_required)
                    
                    # Segunda tentativa com assinatura
                    headers = {
                        'PAYMENT-SIGNATURE': payment.signature
                    }
                    response = httpx.get(url, headers=headers)
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"HTTP {response.status_code}", "details": response.text}
                
        except Exception as e:
            return {"error": str(e)}
    
    def get_prediction_for_asset(self, asset_symbol):
        """Obtém previsão específica para um ativo"""
        predictions = self.get_predictions()
        if "predictions" in predictions:
            for pred in predictions["predictions"]:
                if pred["asset"] == asset_symbol.upper():
                    return pred
        return None
```

### Passo 4: Script de Exemplo para Agentes de IA

```python
# client/example_usage.py
#!/usr/bin/env python3
"""
Exemplo de uso do cliente Alpha Engine para agentes de IA
"""

import os
from alpha_client import AlphaEngineClient

def main():
    # Configuração (em produção, use variáveis de ambiente)
    PRIVATE_KEY = os.getenv("EVM_PRIVATE_KEY")  # Chave privada da carteira do cliente
    SERVER_URL = os.getenv("ALPHA_ENGINE_URL", "http://localhost:5000")
    
    if not PRIVATE_KEY:
        print("ERRO: Defina a variável de ambiente EVM_PRIVATE_KEY")
        return
    
    # Inicializa cliente
    client = AlphaEngineClient(
        private_key=PRIVATE_KEY,
        rpc_url="https://mainnet.base.org"
    )
    
    print("🔄 Obtendo previsões do Alpha Engine...")
    
    # Obtém todas as previsões
    predictions = client.get_predictions()
    
    if "error" in predictions:
        print(f"❌ Erro: {predictions['error']}")
        return
    
    print(f"✅ Previsões obtidas com sucesso!")
    print(f"📊 Última atualização: {predictions.get('last_update')}")
    print(f"🔢 Total de ativos: {len(predictions.get('predictions', []))}")
    
    # Exemplo: análise de BTC
    btc_prediction = client.get_prediction_for_asset("BTC")
    if btc_prediction:
        print(f"\n📈 Análise BTC:")
        print(f"   Preço atual: ${btc_prediction['current_price']:,.2f}")
        print(f"   RSI: {btc_prediction['rsi']}")
        print(f"   Bias: {btc_prediction['analysis']['bias']}")
        print(f"   Probabilidade: {btc_prediction['analysis']['probability']*100:.1f}%")
        
        # Tomada de decisão automatizada
        if btc_prediction['analysis']['bias'] == "LONG_BIAS" and btc_prediction['analysis']['probability'] > 0.7:
            print("   🟢 SINAL: LONG recomendado")
        elif btc_prediction['analysis']['bias'] == "SHORT_BIAS" and btc_prediction['analysis']['probability'] > 0.7:
            print("   🔴 SINAL: SHORT recomendado")
        else:
            print("   🟡 SINAL: Aguardar melhor oportunidade")

if __name__ == "__main__":
    main()
```

## 🔐 Configuração de Segurança

### 1. Carteira do Merchant
- **Endereço**: `0x077e8d29e11ff1c0ccb236e0380d0053dcba2b1c`
- **Rede**: Base (eip155:8453)
- **Token**: USDC (contrato: `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`)

### 2. Facilitator da Coinbase
- **URL**: `https://facilitator.cdp.coinbase.com`
- **Free Tier**: 1,000 transações/mês
- **Custo após**: $0.001 por transação

### 3. Variáveis de Ambiente
```bash
# Servidor
export MERCHANT_WALLET="0x077e8d29e11ff1c0ccb236e0380d0053dcba2b1c"
export PRICE_USDC="0.01"
export NETWORK="eip155:8453"
export FACILITATOR_URL="https://facilitator.cdp.coinbase.com"

# Cliente
export EVM_PRIVATE_KEY="sua_chave_privada_aqui"
export ALPHA_ENGINE_URL="http://seu-servidor:5000"
```

## 📊 Modelo de Monetização

### Preços (seguindo CoinGecko)
- **Preço base**: $0.01 por requisição
- **Volume discount**: A definir
- **API keys**: Opcional para clientes frequentes

### Projeção de Receita
- 100 requisições/dia = $1/dia = $30/mês
- 1,000 requisições/dia = $10/dia = $300/mês
- 10,000 requisições/dia = $100/dia = $3,000/mês

## 🚀 Deployment

### Opção 1: Servidor Dedicado
```bash
# Instalação
cd /root/openclaw/x402_implementation/server
pip install -r requirements.txt

# Execução
python app.py

# Execução em background (com systemd)
sudo cp alpha-engine-x402.service /etc/systemd/system/
sudo systemctl enable alpha-engine-x402
sudo systemctl start alpha-engine-x402
```

### Opção 2: Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

### Opção 3: Cloud Run (GCP) / Railway
- Containerização simples
- Escalabilidade automática
- Integração com load balancer

## 🔍 Testes

### Testes Unitários
```python
# tests/test_x402_integration.py
def test_payment_flow():
    # Testa fluxo completo de pagamento
    pass

def test_client_integration():
    # Testa integração do cliente
    pass

def test_error_handling():
    # Testa tratamento de erros
    pass
```

### Testes de Integração
1. Testar pagamento com USDC real (testnet primeiro)
2. Testar múltiplas requisições simultâneas
3. Testar timeout e retry logic

## 📈 Monitoramento

### Métricas a Monitorar
- **Requisições totais**: Contagem de 402 vs 200
- **Receita acumulada**: USDC recebido
- **Tempo de resposta**: P50, P95, P99
- **Erros**: Rate de 5xx, 4xx

### Logs
- Todas as transações x402 (sucesso/falha)
- IPs dos clientes (para analytics)
- Tempo de processamento

## 🔄 Integração com Alpha Engine Existente

### Atualização Automática
```python
# server/update_predictions.py
import json
import time
from datetime import datetime

def update_predictions_file():
    """Atualiza o arquivo de previsões periodicamente"""
    while True:
        try:
            # Chama Alpha Engine para gerar novas previsões
            # Salva em /root/openclaw/reports/alpha_prediction_latest.json
            # Atualiza timestamp
            pass
        except Exception as e:
            print(f"Erro ao atualizar previsões: {e}")
        time.sleep(300)  # Atualiza a cada 5 minutos
```

## 🎯 Próximos Passos

### Fase 1: MVP (1-2 dias)
1. [ ] Implementar servidor Flask básico
2. [ ] Integrar middleware x402
3. [ ] Testar com facilitator sandbox
4. [ ] Criar cliente Python

### Fase 2: Produção (3-5 dias)
1. [ ] Configurar ambiente de produção
2. [ ] Implementar monitoramento
3. [ ] Configurar SSL/TLS
4. [ ] Testes de carga

### Fase 3: Expansão (1 semana+)
1. [ ] Adicionar mais endpoints (previsões específicas)
2. [ ] Implementar cache
3. [ ] Adicionar rate limiting
4. [ ] Dashboard de analytics

## ⚠️ Considerações de Segurança

### Crítico
1. **NUNCA** commitar chaves privadas
2. Usar variáveis de ambiente para configurações sensíveis
3. Validar todas as assinaturas de pagamento
4. Implementar rate limiting para prevenir abuso

### Recomendações
1. Usar HTTPS em produção
2. Implementar CORS adequado
3. Manter logs de auditoria
4. Backup regular das transações

## 📞 Suporte

### Documentação
- [x402 Documentation](https://docs.cdp.coinbase.com/x402/welcome)
- [CoinGecko x402 Example](https://github.com/cg-brianlsh/coingecko-x402-python-v3)
- [Base Network Docs](https://docs.base.org/)

### Comunidade
- Discord da Coinbase CDP
- Fórum Base Network
- GitHub Issues do projeto x402

---

**Status**: Plano pronto para execução
**Próxima ação**: Implementar servidor MVP
**Responsável**: Arquiteto-Chefe de Infraestrutura - Leve IA