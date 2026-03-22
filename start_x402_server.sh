#!/bin/bash
# Script de inicialização do servidor x402 Alpha Engine

set -e

source /root/openclaw/.leveia_paths 2>/dev/null || true
WORKSPACE_DIR="${WORKSPACE_DIR:-/root/openclaw}"
PREDICTION_FILE="${PREDICTION_FILE:-$WORKSPACE_DIR/reports/alpha_prediction_latest.json}"

echo "========================================="
echo "Iniciando servidor Alpha Engine x402"
echo "========================================="

# Verifica se estamos no diretório correto
if [ ! -f "x402_server.py" ]; then
    echo "Erro: x402_server.py não encontrado!"
    echo "Execute este script do diretório /root/openclaw"
    exit 1
fi

# Instala dependências se necessário
if [ ! -d "venv" ]; then
    echo "Criando ambiente virtual..."
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements_x402.txt
else
    source venv/bin/activate
fi

# Verifica conexão com a blockchain
echo "Verificando conexão com a Base Chain..."
python3 -c "
from web3 import Web3
w3 = Web3(Web3.HTTPProvider('https://mainnet.base.org'))
if w3.is_connected():
    print('✓ Conectado à Base Chain')
    print(f'  Último bloco: {w3.eth.block_number}')
else:
    print('✗ Não conectado à Base Chain')
    print('  Verifique sua conexão com a internet')
"

# Verifica arquivo de predições
if [ -f "$PREDICTION_FILE" ]; then
    echo "✓ Arquivo de predições encontrado: $PREDICTION_FILE"
else
    echo "⚠  Arquivo de predições não encontrado em $PREDICTION_FILE"
    echo "   O Alpha Engine precisa gerar predições primeiro"
fi

# Configurações
PORT=${PORT:-8000}
HOST=${HOST:-"0.0.0.0"}

echo ""
echo "Configuração:"
echo "  Porta: $PORT"
echo "  Host: $HOST"
echo "  Preço: \$0.10 USDC"
echo "  Carteira: 0x077e8d29e11ff1c0ccb236e0380d0053dcba2b1c"
echo ""

# Inicia o servidor
echo "Iniciando servidor FastAPI..."
echo "Acesse: http://localhost:$PORT"
echo "Documentação: http://localhost:$PORT/docs"
echo ""
echo "Pressione Ctrl+C para parar o servidor"
echo ""

exec python3 x402_server.py