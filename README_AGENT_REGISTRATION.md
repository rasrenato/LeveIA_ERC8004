# Leve IA - Agent Registration on Ethereum Mainnet

## 🎯 Visão Geral

Este projeto implementa um contrato inteligente compatível com **Agent0 SDK** e **Circle Protocol** para registrar e auditar predições de mercado da Leve IA, com provas de processamento de **10TB de dados**.

## ✨ Características Principais

### 1. **Compatibilidade com Agent0 SDK (ERC-8004)**
- Eventos padronizados para descoberta de agentes
- Getters para integração com subgraphs
- Registro de identidade de agentes

### 2. **Attestations do Circle Protocol**
- Suporte a provas de processamento de 10TB de dados
- Raízes Merkle para attestations em lote
- Verificação on-chain de inclusão

### 3. **Registro de Agente no Mainnet**
- Função `registerAgent` para registro único
- Capacidades configuráveis em JSON
- Status ativo/inativo gerenciável

### 4. **Auditoria Transparente**
- Logs imutáveis de predições
- Timestamps e hashes de entrada
- Provas criptográficas e attestations

## 📁 Estrutura do Projeto

```
contracts/
├── LeveIA_AuditRegistry.sol    # Contrato principal
scripts/
├── deploy_and_register.js      # Script de deploy e registro
├── register_agent_mainnet.sh   # Script bash para mainnet
├── estimate_gas.js            # Estimativa de custos
config/
└── agent_capabilities.json    # Configuração do agente
```

## 🚀 Como Executar

### Pré-requisitos

1. **Node.js** (v18 ou superior)
2. **npm** ou **yarn**
3. **Conta Ethereum** com ETH no Mainnet
4. **Chave API do Infura**

### Configuração

```bash
# 1. Clone o repositório
git clone <repository-url>
cd leve-ia-audit

# 2. Instale dependências
npm install

# 3. Configure variáveis de ambiente
export PRIVATE_KEY=your_private_key_here
export INFURA_API_KEY=your_infura_api_key_here
```

### Execução no Mainnet

```bash
# Torne o script executável
chmod +x scripts/register_agent_mainnet.sh

# Execute o registro
./scripts/register_agent_mainnet.sh
```

## 📊 Comando `registerAgent`

### Função do Contrato

```solidity
function registerAgent(
    string memory _agentId,
    string memory _capabilities,
    bytes32 _initialAttestationRoot
) external whenNotPaused
```

### Parâmetros

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `_agentId` | string | ID único do agente (ex: "leve-ia-market-predictor-v1") |
| `_capabilities` | string | JSON com capacidades do agente |
| `_initialAttestationRoot` | bytes32 | Raiz Merkle inicial para attestations |

### Exemplo de Capacidades JSON

```json
{
    "name": "Leve IA Market Predictor",
    "version": "1.0.0",
    "description": "AI agent for financial market predictions using 10TB data processing",
    "capabilities": [
        "market_prediction",
        "data_processing_10tb",
        "circle_attestations",
        "agent0_sdk_compatible"
    ],
    "dataProcessing": {
        "volume": "10TB",
        "attestation": "circle_protocol",
        "frequency": "daily"
    }
}
```

## 🔗 Integrações

### Agent0 SDK

O contrato emite eventos compatíveis com o Agent0 SDK:

```solidity
event AgentRegistered(
    address indexed agentAddress,
    string agentId,
    string capabilities,
    uint256 registrationTime,
    bytes32 attestationRoot
);

event PredictionLogged(
    uint256 indexed logId,
    string modelId,
    string output,
    bytes32 inputHash,
    bytes32 proof,
    bytes32 circleAttestation
);
```

### Circle Protocol

Para attestations de processamento de 10TB:

```solidity
event AttestationBatchCreated(
    uint256 indexed batchId,
    bytes32 root,
    uint256 timestamp,
    uint256 dataVolumeTB  // 10TB per batch
);
```

## 💰 Estimativa de Custos

Execute para estimar os custos de gas:

```bash
npx hardhat run scripts/estimate_gas.js --network mainnet
```

**Custos aproximados:**
- Deploy do contrato: ~1,500,000 gas
- Registro do agente: ~200,000 gas
- Criação de batch: ~100,000 gas
- Log de predição: ~150,000 gas

**Total estimado:** ~2,000,000 gas (≈ $XX USD)

## 🔍 Verificação

### 1. Verificação no Etherscan

```bash
npx hardhat verify --network mainnet <CONTRACT_ADDRESS>
```

### 2. Verificação de Registro

```javascript
const agentInfo = await registry.getAgentRegistration(agentAddress);
console.log("Agent ID:", agentInfo.agentId);
console.log("Active:", agentInfo.isActive);
```

### 3. Verificação de Attestation

```javascript
const isValid = await registry.verifyAttestationInclusion(
    batchId,
    leafHash,
    merkleProof
);
```

## 📈 Fluxo de Trabalho

1. **Registro do Agente**
   ```bash
   ./scripts/register_agent_mainnet.sh
   ```

2. **Criação de Attestation Batch (10TB)**
   ```solidity
   createAttestationBatch(root, 10);
   ```

3. **Log de Predição com Attestation**
   ```solidity
   logPrediction(modelId, inputHash, output, proof, circleAttestation);
   ```

4. **Validação por Terceiros**
   ```solidity
   attestValidation(logId, attestationHash);
   ```

## 🛡️ Segurança

### Features Implementadas

- **Ownable**: Apenas o owner pode fazer deploy e configurar
- **Pausable**: Contrato pode ser pausado em caso de emergência
- **Input Validation**: Validação de parâmetros
- **Access Control**: Controle de acesso para funções sensíveis

### Boas Práticas

1. Use uma wallet dedicada para o contrato
2. Mantenha backup das chaves privadas
3. Monitore eventos do contrato
4. Atualize capacidades conforme necessário

## 🤝 Contribuição

1. Fork o repositório
2. Crie uma branch (`git checkout -b feature/improvement`)
3. Commit suas mudanças (`git commit -am 'Add feature'`)
4. Push para a branch (`git push origin feature/improvement`)
5. Crie um Pull Request

## 📄 Licença

MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 📞 Suporte

Para questões técnicas:
- Issues no GitHub
- Telegram: @leveia_support
- Email: tech@leveia.com

---

**Leve IA - Hackathon Edition** 🚀
*Contrato técnico de orgulho para o hackathon*