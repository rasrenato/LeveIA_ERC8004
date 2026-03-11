# Alpha Engine x402 Server

Servidor FastAPI que implementa o protocolo x402 para venda de sinais do Alpha Engine.

## 📋 Visão Geral

Este servidor permite que usuários paguem $0.10 USDC na rede Base para acessar as predições do Alpha Engine (BTC, ETH, BNB).

### Características

- ✅ **Protocolo x402 simplificado**: Verificação de pagamento USDC na blockchain
- ✅ **FastAPI**: API moderna e rápida com documentação automática
- ✅ **Web3.py**: Integração com a Base Chain
- ✅ **Cliente de exemplo**: Demonstração completa do fluxo
- ✅ **Seguro**: Verificação de transações na blockchain
- ✅ **Pronto para produção**: Fácil deploy e configuração

## 🚀 Instalação Rápida

### 1. Pré-requisitos

```bash
# Python 3.8+
python3 --version

# Git (opcional)
git --version
```

### 2. Instalação

```bash
# Clone o repositório (se aplicável)
# cd /root/openclaw

# Torne o script executável
chmod +x start_x402_server.sh

# Instale dependências
pip install -r requirements_x402.txt
```

### 3. Configuração

O servidor já vem configurado com:

- **Carteira do Renato**: `0x077e8d29e11ff1c0ccb236e0380d0053dcba2b1c`
- **Preço**: $0.10 USDC
- **Rede**: Base (mainnet)
- **Arquivo de predições**: `/root/openclaw/reports/alpha_prediction_latest.json`

## 🏃 Execução

### Método 1: Script de inicialização (recomendado)

```bash
./start_x402_server.sh
```

### Método 2: Manualmente

```bash
# Ative o ambiente virtual (se criado)
source venv/bin/activate

# Execute o servidor
python3 x402_server.py
```

O servidor iniciará na porta 8000. Acesse:
- http://localhost:8000 - Página inicial
- http://localhost:8000/docs - Documentação interativa da API
- http://localhost:8000/redoc - Documentação alternativa

## 📡 Endpoints da API

### GET `/`
Informações do servidor.

### GET `/health`
Health check do servidor e conexão com blockchain.

### GET `/prediction-sample`
Amostra do formato das predições (sem pagamento).

### POST `/verify-payment`
Verifica se um pagamento USDC foi realizado.

**Body:**
```json
{
  "tx_hash": "0x...",
  "user_address": "0x..."
}
```

### GET `/alpha-prediction`
Retorna as predições completas após verificação de pagamento.

**Parâmetros:**
- `tx_hash` (obrigatório): Hash da transação
- `user_address` (obrigatório): Endereço do usuário

## 💰 Fluxo de Pagamento

### Para usuários:

1. **Envie $0.10 USDC** para `0x077e8d29e11ff1c0ccb236e0380d0053dcba2b1c` na rede Base
2. **Guarde o hash da transação**
3. **Use seu endereço Ethereum** que enviou o pagamento
4. **Acesse a API** com tx_hash e user_address

### Verificação realizada:

1. ✅ Transação existe na blockchain
2. ✅ Foi enviada pelo user_address informado
3. ✅ Destino é a carteira do Renato
4. ✅ Valor ≥ $0.10 USDC
5. ✅ Transação nos últimos 5 minutos

## 🧪 Cliente de Exemplo

### Executar demonstração:

```bash
python3 x402_client_example.py
```

### Cliente interativo:

```bash
python3 x402_client_example.py
# Escolha a opção para usar cliente interativo
```

### Exemplo de código:

```python
from x402_client_example import X402Client

client = X402Client("http://localhost:8000")

# Verifica pagamento
verification = client.verify_payment("SEU_HASH", "SEU_ENDERECO")
if verification["verified"]:
    # Obtém predições
    predictions = client.get_predictions("SEU_HASH", "SEU_ENDERECO")
    print(predictions)
```

## 🔧 Configuração Avançada

### Variáveis de ambiente (opcional)

Crie um arquivo `.env`:

```bash
# Porta do servidor
PORT=8000

# Host do servidor
HOST=0.0.0.0

# URL da Base RPC (alternativa)
BASE_RPC_URL=https://mainnet.base.org

# Carteira (altere com cuidado)
RENATO_WALLET=0x077e8d29e11ff1c0ccb236e0380d0053dcba2b1c

# Preço em USDC
PRICE_USDC=0.10

# Janela de pagamento (minutos)
PAYMENT_WINDOW_MINUTES=5
```

### Deploy em produção

1. **Use um process manager** como systemd, supervisor ou pm2
2. **Configure um reverse proxy** como Nginx ou Caddy
3. **Use HTTPS** com certificado SSL (Let's Encrypt)
4. **Monitore logs** e métricas

#### Exemplo systemd service (`/etc/systemd/system/alpha-x402.service`):

```ini
[Unit]
Description=Alpha Engine x402 Server
After=network.target

[Service]
Type=simple
User=renato
WorkingDirectory=/root/openclaw
Environment="PATH=/root/openclaw/venv/bin"
ExecStart=/root/openclaw/venv/bin/python3 x402_server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

## 🐛 Solução de Problemas

### "Arquivo de predições não encontrado"
- Verifique se o Alpha Engine está gerando predições
- Confirme o caminho: `/root/openclaw/reports/alpha_prediction_latest.json`

### "Não conectado à Base Chain"
- Verifique conexão com internet
- Tente uma RPC alternativa:
  - `https://base-mainnet.g.alchemy.com/v2/SEU_KEY`
  - `https://base.publicnode.com`

### "Transação não encontrada"
- Aguarde alguns blocos para confirmação
- Verifique se está na rede Base
- Confirme o hash da transação

### Erros de pagamento
- Valor mínimo: $0.10 USDC
- Janela máxima: 5 minutos após transação
- Destino correto: `0x077e8d29e11ff1c0ccb236e0380d0053dcba2b1c`

## 🔒 Segurança

### Boas práticas:

1. **Mantenha as chaves privadas seguras** - nunca no código
2. **Use variáveis de ambiente** para dados sensíveis
3. **Limite acesso** com firewall/iptables
4. **Monitore logs** para atividades suspeitas
5. **Atualize dependências** regularmente

### Auditoria recomendada:

- [ ] Revisar lógica de verificação de pagamento
- [ ] Testar com diferentes valores e cenários
- [ ] Verificar tratamento de erros
- [ ] Testar limites e edge cases

## 📊 Monitoramento

### Logs do servidor:
```bash
# Visualizar logs em tempo real
tail -f nohup.out  # ou logs do systemd

# Verificar saúde
curl http://localhost:8000/health
```

### Métricas sugeridas:
- Transações verificadas por hora
- Erros de pagamento
- Tempo de resposta da API
- Conexão com blockchain

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Crie um Pull Request

## 📄 Licença

Este projeto é para uso interno da Leve IA.

## 📞 Suporte

Para suporte ou dúvidas:
- Verifique a documentação em `/docs`
- Consulte os exemplos em `x402_client_example.py`
- Revise os logs do servidor

---

**Arquiteto de Infraestrutura - Leve IA**  
*Implementação segura e prática do protocolo x402 para monetização do Alpha Engine*