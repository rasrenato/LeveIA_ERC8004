#!/bin/bash
# Script de implantação para Leve IA x402 Payment Gateway

set -e  # Sai no primeiro erro

echo "🚀 Leve IA x402 Payment Gateway - Deployment Script"
echo "=================================================="

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Funções de logging
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar se é root
if [ "$EUID" -ne 0 ]; then 
    log_warn "Recomendado executar como root para instalação de pacotes"
fi

# Configurações
VENV_DIR="venv"
SERVER_DIR="server"
CLIENT_DIR="client"
EXAMPLES_DIR="examples"
REQUIREMENTS_FILE="requirements.txt"
ENV_EXAMPLE=".env.example"
ENV_FILE=".env"

# Menu de ajuda
show_help() {
    echo "Uso: $0 [comando]"
    echo ""
    echo "Comandos:"
    echo "  install     Instalar dependências e configurar ambiente"
    echo "  start       Iniciar servidor x402"
    echo "  stop        Parar servidor x402"
    echo "  restart     Reiniciar servidor x402"
    echo "  status      Verificar status do servidor"
    echo "  test        Executar testes básicos"
    echo "  update      Atualizar código e dependências"
    echo "  clean       Limpar ambiente virtual e cache"
    echo ""
    echo "Exemplos:"
    echo "  $0 install   # Instalação inicial"
    echo "  $0 start     # Iniciar servidor"
    echo "  $0 test      # Testar funcionalidade"
}

# Instalar dependências do sistema
install_system_deps() {
    log_info "Instalando dependências do sistema..."
    
    # Verificar Python
    if ! command -v python3 &> /dev/null; then
        log_error "Python3 não encontrado. Instale com:"
        log_error "  apt update && apt install -y python3 python3-pip"
        exit 1
    fi
    
    # Verificar pip
    if ! command -v pip3 &> /dev/null; then
        log_info "Instalando pip..."
        apt update && apt install -y python3-pip
    fi
    
    # Instalar python3-venv se necessário
    if ! python3 -c "import venv" &> /dev/null; then
        log_info "Instalando python3-venv..."
        apt update && apt install -y python3.12-venv
    fi
    
    log_info "Dependências do sistema verificadas"
}

# Criar ambiente virtual
setup_venv() {
    log_info "Configurando ambiente virtual Python..."
    
    if [ ! -d "$VENV_DIR" ]; then
        python3 -m venv "$VENV_DIR"
        log_info "Ambiente virtual criado em: $VENV_DIR"
    else
        log_info "Ambiente virtual já existe em: $VENV_DIR"
    fi
    
    # Ativar ambiente virtual
    source "$VENV_DIR/bin/activate"
    
    # Atualizar pip
    pip install --upgrade pip
    
    log_info "Ambiente virtual configurado"
}

# Instalar dependências Python
install_python_deps() {
    log_info "Instalando dependências Python..."
    
    source "$VENV_DIR/bin/activate"
    
    if [ -f "$REQUIREMENTS_FILE" ]; then
        pip install -r "$REQUIREMENTS_FILE"
        log_info "Dependências instaladas de $REQUIREMENTS_FILE"
    else
        log_error "Arquivo $REQUIREMENTS_FILE não encontrado"
        exit 1
    fi
}

# Configurar arquivo .env
setup_env() {
    log_info "Configurando variáveis de ambiente..."
    
    if [ ! -f "$ENV_FILE" ]; then
        if [ -f "$ENV_EXAMPLE" ]; then
            cp "$ENV_EXAMPLE" "$ENV_FILE"
            log_warn "Arquivo $ENV_FILE criado de $ENV_EXAMPLE"
            log_warn "Edite $ENV_FILE com suas configurações antes de iniciar o servidor"
        else
            log_error "Arquivo $ENV_EXAMPLE não encontrado"
            exit 1
        fi
    else
        log_info "Arquivo $ENV_FILE já existe"
    fi
}

# Verificar arquivo de previsões
check_predictions_file() {
    log_info "Verificando arquivo de previsões..."
    
    PRED_FILE=$(grep -i "prediction_file" "$ENV_FILE" 2>/dev/null | cut -d'=' -f2 | tr -d ' ' | head -1)
    
    if [ -z "$PRED_FILE" ]; then
        WORKSPACE_DIR="${WORKSPACE_DIR:-/root/openclaw}"
        PRED_FILE="$WORKSPACE_DIR/reports/alpha_prediction_latest.json"
    fi
    
    if [ -f "$PRED_FILE" ]; then
        log_info "Arquivo de previsões encontrado: $PRED_FILE"
        
        # Verificar se é JSON válido
        if python3 -m json.tool "$PRED_FILE" > /dev/null 2>&1; then
            log_info "JSON válido detectado"
        else
            log_warn "Arquivo JSON pode ser inválido"
        fi
    else
        log_warn "Arquivo de previsões não encontrado: $PRED_FILE"
        log_warn "Crie o arquivo ou ajuste PREDICTION_FILE no .env"
    fi
}

# Iniciar servidor
start_server() {
    log_info "Iniciando servidor x402..."
    
    if [ ! -f "$ENV_FILE" ]; then
        log_error "Arquivo $ENV_FILE não encontrado. Execute '$0 install' primeiro."
        exit 1
    fi
    
    source "$VENV_DIR/bin/activate"
    
    # Carregar variáveis do .env
    set -a
    source "$ENV_FILE"
    set +a
    
    # Verificar se o servidor já está rodando
    if pgrep -f "x402_server.py" > /dev/null; then
        log_warn "Servidor já está em execução"
        return
    fi
    
    # Iniciar servidor em background
    nohup python3 "$SERVER_DIR/x402_server.py" > server.log 2>&1 &
    
    SERVER_PID=$!
    echo $SERVER_PID > server.pid
    
    sleep 2  # Dar tempo para o servidor iniciar
    
    # Verificar se iniciou corretamente
    if kill -0 $SERVER_PID 2>/dev/null; then
        log_info "Servidor iniciado com PID: $SERVER_PID"
        log_info "Logs: server.log"
        
        # Testar conexão
        sleep 1
        if curl -s http://localhost:${SERVER_PORT:-5000}/health > /dev/null; then
            log_info "✅ Servidor respondendo em http://localhost:${SERVER_PORT:-5000}"
        else
            log_warn "Servidor iniciado mas não responde ao health check"
        fi
    else
        log_error "Falha ao iniciar servidor. Verifique server.log"
        exit 1
    fi
}

# Parar servidor
stop_server() {
    log_info "Parando servidor x402..."
    
    if [ -f "server.pid" ]; then
        SERVER_PID=$(cat server.pid)
        
        if kill -0 $SERVER_PID 2>/dev/null; then
            kill $SERVER_PID
            sleep 1
            
            if kill -0 $SERVER_PID 2>/dev/null; then
                kill -9 $SERVER_PID
                log_warn "Servidor finalizado com SIGKILL"
            else
                log_info "Servidor parado com sucesso"
            fi
            
            rm -f server.pid
        else
            log_warn "Servidor não está em execução (PID: $SERVER_PID)"
            rm -f server.pid
        fi
    else
        # Tentar encontrar por nome
        PIDS=$(pgrep -f "x402_server.py" || true)
        
        if [ -n "$PIDS" ]; then
            log_info "Encontrados processos: $PIDS"
            kill $PIDS 2>/dev/null || true
            sleep 1
            
            # Verificar se ainda estão rodando
            REMAINING=$(pgrep -f "x402_server.py" || true)
            if [ -n "$REMAINING" ]; then
                kill -9 $REMAINING 2>/dev/null || true
                log_warn "Processos finalizados com SIGKILL"
            fi
            
            log_info "Servidores parados"
        else
            log_info "Nenhum servidor em execução encontrado"
        fi
    fi
}

# Verificar status
check_status() {
    log_info "Verificando status do sistema..."
    
    # Verificar ambiente virtual
    if [ -d "$VENV_DIR" ]; then
        log_info "✅ Ambiente virtual: $VENV_DIR"
    else
        log_warn "❌ Ambiente virtual não encontrado"
    fi
    
    # Verificar .env
    if [ -f "$ENV_FILE" ]; then
        log_info "✅ Arquivo .env: $ENV_FILE"
        
        # Mostrar configurações importantes
        echo ""
        log_info "Configurações atuais:"
        grep -E "^(MERCHANT_WALLET|PRICE_USDC|SERVER_PORT|PREDICTION_FILE)=" "$ENV_FILE" || true
        echo ""
    else
        log_warn "❌ Arquivo .env não encontrado"
    fi
    
    # Verificar servidor
    if pgrep -f "x402_server.py" > /dev/null; then
        log_info "✅ Servidor em execução"
        
        # Tentar health check
        PORT=$(grep -i "server_port" "$ENV_FILE" 2>/dev/null | cut -d'=' -f2 | tr -d ' ' | head -1)
        PORT=${PORT:-5000}
        
        if curl -s http://localhost:$PORT/health > /dev/null; then
            log_info "✅ Health check OK"
        else
            log_warn "⚠️  Health check falhou"
        fi
    else
        log_info "❌ Servidor não está em execução"
    fi
    
    # Verificar arquivo de previsões
    check_predictions_file
}

# Executar testes
run_tests() {
    log_info "Executando testes básicos..."
    
    source "$VENV_DIR/bin/activate"
    
    # Testar importações
    log_info "Testando importações Python..."
    python3 -c "
try:
    import flask
    import x402
    import web3
    import eth_account
    print('✅ Importações básicas OK')
except ImportError as e:
    print(f'❌ Falha na importação: {e}')
    exit(1)
"
    
    # Testar servidor (se estiver rodando)
    PORT=$(grep -i "server_port" "$ENV_FILE" 2>/dev/null | cut -d'=' -f2 | tr -d ' ' | head -1)
    PORT=${PORT:-5000}
    
    if curl -s http://localhost:$PORT/health > /dev/null; then
        log_info "✅ Servidor respondendo"
        
        # Testar endpoint principal
        RESPONSE=$(curl -s -w "%{http_code}" http://localhost:$PORT/alpha/signals -o /tmp/test_response.json)
        
        if [ "$RESPONSE" = "402" ]; then
            log_info "✅ Endpoint /alpha/signals retornando 402 (pagamento necessário)"
            
            # Verificar estrutura da resposta
            if python3 -m json.tool /tmp/test_response.json > /dev/null 2>&1; then
                log_info "✅ Resposta 402 com JSON válido"
                
                # Mostrar informações de pagamento
                AMOUNT=$(grep -o '"amount_usdc":[^,]*' /tmp/test_response.json | cut -d':' -f2)
                WALLET=$(grep -o '"merchant_wallet":"[^"]*"' /tmp/test_response.json | cut -d'"' -f4)
                
                log_info "   Preço: \$${AMOUNT} USDC"
                log_info "   Carteira: ${WALLET}"
            else
                log_warn "⚠️  Resposta 402 sem JSON válido"
            fi
        else
            log_warn "⚠️  Endpoint retornou $RESPONSE (esperado 402)"
        fi
        
        rm -f /tmp/test_response.json
    else
        log_warn "⚠️  Servidor não está rodando ou não responde"
    fi
    
    # Testar cliente
    log_info "Testando cliente..."
    if [ -f "$CLIENT_DIR/x402_client.py" ]; then
        python3 -c "
import sys
sys.path.append('.')
try:
    from client.x402_client import AlphaEngineClient
    print('✅ Cliente importado com sucesso')
    
    # Testar inicialização
    client = AlphaEngineClient()
    print('✅ Cliente inicializado')
    
    # Testar health check
    health = client.get_server_health()
    if health:
        print(f'✅ Health check: {health.get(\"status\", \"unknown\")}')
    else:
        print('⚠️  Health check falhou')
        
except Exception as e:
    print(f'❌ Erro no teste do cliente: {e}')
"
    else
        log_warn "⚠️  Arquivo do cliente não encontrado"
    fi
    
    log_info "Testes completados"
}

# Atualizar sistema
update_system() {
    log_info "Atualizando sistema..."
    
    # Parar servidor se estiver rodando
    stop_server
    
    # Atualizar código (simulação - em produção seria git pull)
    log_info "Atualizando dependências..."
    source "$VENV_DIR/bin/activate"
    pip install --upgrade -r "$REQUIREMENTS_FILE"
    
    # Verificar .env
    if [ -f "$ENV_FILE" ]; then
        log_info "Preservando configurações do .env"
    fi
    
    log_info "Sistema atualizado. Execute '$0 start' para reiniciar."
}

# Limpar ambiente
clean_environment() {
    log_info "Limpando ambiente..."
    
    # Parar servidor
    stop_server
    
    # Remover ambiente virtual
    if [ -d "$VENV_DIR" ]; then
        log_info "Removendo ambiente virtual..."
        rm -rf "$VENV_DIR"
    fi
    
    # Remover logs
    rm -f server.log
    rm -f server.pid
    
    # Remover cache Python
    find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
    find . -name "*.pyc" -delete 2>/dev/null || true
    
    log_info "Ambiente limpo"
}

# Processar comando
case "${1:-install}" in
    install)
        install_system_deps
        setup_venv
        install_python_deps
        setup_env
        check_predictions_file
        log_info "✅ Instalação completa!"
        log_info "   Edite o arquivo .env com suas configurações"
        log_info "   Execute '$0 start' para iniciar o servidor"
        ;;
        
    start)
        start_server
        ;;
        
    stop)
        stop_server
        ;;
        
    restart)
        stop_server
        sleep 2
        start_server
        ;;
        
    status)
        check_status
        ;;
        
    test)
        run_tests
        ;;
        
    update)
        update_system
        ;;
        
    clean)
        clean_environment
        ;;
        
    help|--help|-h)
        show_help
        ;;
        
    *)
        log_error "Comando desconhecido: $1"
        echo ""
        show_help
        exit 1
        ;;
esac