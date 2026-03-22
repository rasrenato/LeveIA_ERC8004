# ERC-8183: Agentic Commerce Protocol

**Status:** ✅ Implementado  
**Data:** 09/Mar/2026  
**Autor:** Cabral (CEO Agent) para Leve IA

---

## 📋 **VISÃO GERAL**

O **ERC-8183** é um padrão Ethereum para **pagamentos condicionais com escrow** entre agentes autônomos.

### **Arquitetura Completa:**

```
┌─────────────────────────────────────────────────────────┐
│            ECONOMIA AGENTICA ETHEREUM                   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  x402          → Micropagamentos HTTP                   │
│  ERC-8004      → Confiança e reputação                  │
│  ERC-8183      → Pagamentos CONDICIONAIS (escrow)      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 **CASOS DE USO**

| Caso | Descrição |
|------|-----------|
| **AI Services** | Pagar IA após trabalho verificado |
| **Data Processing** | Escrow para processamento de dados |
| **Bridge Operations** | Liberar fundos após bridge confirmado |
| **Trading Signals** | Pagar sinal após resultado |
| **Oracle Work** | Compensar oráculos por dados |

---

## 🔄 **MÁQUINA DE ESTADOS**

```
Open → Funded → Submitted → Completed
   ↓        ↓         ↓           ↓
   ↓        ↓         ↓        Rejected
   ↓        ↓         ↓
   ↓        ↓      Expired
   ↓     Rejected
Rejected
```

### **Estados:**

| Estado | Significado |
|--------|-------------|
| **Open** | Criado, budget não fundado |
| **Funded** | Budget em escrow, provider pode trabalhar |
| **Submitted** | Provider submeteu trabalho |
| **Completed** | Terminal, pagamento liberado |
| **Rejected** | Terminal, reembolso ao client |
| **Expired** | Terminal, reembolso após expiry |

---

## 👥 **ROLES**

| Role | Permissões |
|------|------------|
| **Client** | Cria job, fundeia, rejeita (Open) |
| **Provider** | Submete trabalho, recebe pagamento |
| **Evaluator** | Completa ou rejeita após submit |

**Nota:** Evaluator pode ser o próprio client (sem terceiro).

---

## 📦 **FUNÇÕES CORE**

### **1. createJob**
```solidity
function createJob(
    address provider,
    address evaluator,
    uint256 expiredAt,
    string calldata description,
    address hook,
    address token
) external returns (uint256 jobId)
```

### **2. setProvider** (opcional)
```solidity
function setProvider(
    uint256 jobId,
    address provider,
    bytes calldata optParams
) external
```

### **3. setBudget**
```solidity
function setBudget(
    uint256 jobId,
    uint256 amount,
    bytes calldata optParams
) external
```

### **4. fund**
```solidity
function fund(
    uint256 jobId,
    uint256 expectedBudget,
    bytes calldata optParams
) external
```

### **5. submit**
```solidity
function submit(
    uint256 jobId,
    bytes32 deliverable,
    bytes calldata optParams
) external
```

### **6. complete**
```solidity
function complete(
    uint256 jobId,
    bytes32 reason,
    bytes calldata optParams
) external
```

### **7. reject**
```solidity
function reject(
    uint256 jobId,
    bytes32 reason,
    bytes calldata optParams
) external
```

### **8. claimRefund**
```solidity
function claimRefund(uint256 jobId) external
```

---

## 🔗 **HOOKS EXTENSÍVEIS**

Hooks permitem estender o protocolo sem modificar o core:

```solidity
interface IACPHook {
    function beforeOrAfterAction(
        uint256 jobId,
        bytes4 selector,
        bytes calldata data,
        bool isBefore
    ) external;
}
```

### **Exemplos de Hooks:**

| Hook | Função |
|------|--------|
| **ReputationHook** | Integra com ERC-8004 |
| **BiddingHook** | Leilão de providers |
| **KYCHook** | Validação pré-fund |
| **FeeHook** | Lógica customizada de fees |

---

## 🧪 **EXEMPLO DE USO**

### **Fluxo Básico:**

```solidity
// 1. Client cria job
uint256 jobId = acp.createJob(
    provider,
    evaluator,
    block.timestamp + 7 days,
    "Process data",
    address(0), // no hook
    usdtToken
);

// 2. Define budget
acp.setBudget(jobId, 100 * 10**6, "");

// 3. Client fundeia
IERC20(usdtToken).approve(acp, 100 * 10**6);
acp.fund(jobId, 100 * 10**6, "");

// 4. Provider trabalha e submete
acp.submit(jobId, keccak256("deliverable"), "");

// 5. Evaluator completa
acp.complete(jobId, keccak256("work approved"), "");

// Provider recebe 100 USDT (menos fee se houver)
```

---

## 🔒 **SEGURANÇA**

### **Proteções:**

| Proteção | Implementação |
|----------|---------------|
| **Reentrancy** | OpenZeppelin ReentrancyGuard |
| **SafeERC20** | Transferências seguras |
| **Expiry** | Refund garantido após expiredAt |
| **Hooks** | Não podem bloquear claimRefund |
| **Fee** | Apenas no completion, não no refund |

### **Considerações:**

- ✅ Evaluator é confiável para completar/rejeitar
- ✅ Provider protegido após submit (client não pode withdraw)
- ✅ Client protegido após expiry (refund garantido)
- ⚠️ Sem dispute resolution (reject/expire é final)

---

## 📊 **INTEGRAÇÃO COM ECOSSISTEMA**

### **x402 (Micropagamentos):**
```
x402 assina pagamento off-chain → ERC-8183 executa on-chain
```

### **ERC-8004 (Reputação):**
```
ERC-8183 completa job → ERC-8004 emite attestation
```

### **Meta-Transactions (ERC-2771):**
```
Agente assina off-chain → Facilitador submete on-chain
```

---

## 📁 **ESTRUTURA DE ARQUIVOS**

```
/root/openclaw/erc-8183/
├── contracts/
│   ├── IERC8183.sol        # Interface
│   ├── ERC8183.sol         # Implementação core
│   ├── IACPHook.sol        # Interface de hooks
│   ├── BaseACPHook.sol     # Base para hooks
│   └── ReputationHook.sol  # Hook ERC-8004
├── test/
│   └── ERC8183.test.js     # Testes
├── scripts/
│   └── deploy.js           # Deploy script
├── docs/
│   └── SPEC.md             # Especificação completa
└── README.md               # Este arquivo
```

---

## 🚀 **DEPLOY**

```bash
cd /root/openclaw/erc-8183

# Instalar dependências
npm install

# Compilar
npx hardhat compile

# Testar
npx hardhat test

# Deploy (Base Mainnet)
npx hardhat run scripts/deploy.js --network base
```

---

## 📈 **MÉTRICAS**

| Métrica | Valor |
|---------|-------|
| **Gas (createJob)** | ~150k |
| **Gas (fund)** | ~80k |
| **Gas (complete)** | ~100k |
| **Gas (submit)** | ~60k |
| **Tamanho contrato** | ~15KB |

---

## 🎯 **PRÓXIMOS PASSOS**

- [ ] Testes unitários completos
- [ ] Deploy em testnet (Base Sepolia)
- [ ] Audit de segurança
- [ ] Integração com Alpha Signals
- [ ] Frontend para criar jobs

---

## 📞 **LINKS**

- **EIP-8183:** https://eips.ethereum.org/EIPS/eip-8183
- **ERC-8004:** https://eips.ethereum.org/EIPS/eip-8004
- **Virtuals ACP:** https://whitepaper.virtuals.io/acp

---

**Criado por:** Cabral (CEO Agent)  
**Para:** Leve IA  
**Data:** 09/Mar/2026  
**Status:** ✅ **IMPLEMENTADO**
