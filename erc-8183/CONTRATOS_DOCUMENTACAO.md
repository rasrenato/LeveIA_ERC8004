# 📚 DOCUMENTAÇÃO DOS CONTRATOS - LEVE IA

**Data:** 2026-03-11  
**Rede:** BSC (Binance Smart Chain)  
**Status:** ✅ Compilados e Prontos para Deploy

---

## 🎯 RESUMO DOS CONTRATOS

| Contrato | Funções | Descrição |
|----------|---------|-----------|
| **ERC8183** | 19 | Commercial Layer - Jobs com escrow |
| **ERC8126** | 19 | Risk Scoring - Reputação de agentes |
| **ERC8021** | 22 | Attribution - Revenue sharing |
| **ReputationHook_v2** | 5 | Hook para eventos de reputação |
| **VestingGateIO** | 20 | Vesting para Gate.IO listing |

---

## 📄 1. ERC8183 - Commercial Layer

**Arquivo:** `contracts/ERC8183.sol`  
**Funções:** 19 públicas

### Principais Funções:

| Função | Parâmetros | Descrição |
|--------|------------|-----------|
| `createJob()` | provider, evaluator, expiredAt, description, hook, token | Cria job com escrow |
| `complete()` | jobId, reason, optParams | Completa job e libera pagamento |
| `reject()` | jobId, reason, optParams | Rejeita job e faz reembolso |
| `claimRefund()` | jobId | Claim de refund após expiry |
| `fund()` | jobId, amount | Fundeia job com tokens |

### Eventos:
- `JobCreated`
- `JobCompleted`
- `JobRejected`
- `JobRefunded`

---

## 📄 2. ERC8126 - Risk Scoring

**Arquivo:** `contracts/ERC8126.sol`  
**Funções:** 19 públicas

### Configurações:

| Constante | Valor | Descrição |
|-----------|-------|-----------|
| `MAX_SCORE()` | 1000 | Score máximo |
| `BASE_FAILURE_PENALTY()` | -50 | Penalidade por falha |
| `BASE_SUCCESS_BONUS()` | +25 | Bônus por sucesso |
| `SLASHING_PERCENTAGE()` | 10% | Porcentagem de slashing |

### Principais Funções:

| Função | Descrição |
|--------|-----------|
| `updateScore()` | Atualiza score do agente |
| `getScore()` | Retorna score atual |
| `getReputationLevel()` | Nível de reputação |
| `slash()` | Penaliza agente por mau comportamento |

---

## 📄 3. ERC8021 - Attribution

**Arquivo:** `contracts/ERC8021.sol`  
**Funções:** 22 públicas

### Configurações:

| Constante | Valor |
|-----------|-------|
| `MAX_REVENUE_SHARE()` | 100% |
| `MAX_WEIGHT()` | 1000 |

### Principais Funções:

| Função | Descrição |
|--------|-----------|
| `createAttribution()` | Cria atribuição de receita |
| `updateAttribution()` | Atualiza atribuição |
| `getAttribution()` | Retorna atribuição |
| `distributeRevenue()` | Distribui receita entre agentes |

---

## 📄 4. ReputationHook_v2

**Arquivo:** `contracts/ReputationHook_v2.sol`  
**Funções:** 5 públicas

### Integração:
- Integrado com ERC-8004 (Reputation Registry)
- Emite eventos quando jobs são completados/rejeitados
- Compatível com Agent0 SDK

### Principais Funções:

| Função | Descrição |
|--------|-----------|
| `beforeOrAfterAction()` | Callback antes/depois de ações |
| `updateRegistry()` | Atualiza endereço do registry |
| `erc8004Registry()` | Retorna registry de reputação |
| `erc8183()` | Retorna contrato ERC-8183 |

---

## 📄 5. VestingGateIO

**Arquivo:** `contracts/VestingGateIO.sol`  
**Funções:** 20 públicas

### Configurações:

| Constante | Valor |
|-----------|-------|
| `PERCENTAGE_DIVISOR()` | 10000 |

### Principais Funções:

| Função | Descrição |
|--------|-----------|
| `createVestingSchedule()` | Cria schedule de vesting |
| `calculateReleasable()` | Calcula quanto pode liberar |
| `release()` | Libera tokens vestidos |
| `cancelSchedule()` | Cancela schedule |

---

## 🔧 PRÉ-REQUISITOS PARA DEPLOY

### 1. Wallet com BNB
- Mínimo: **0.02 BNB** (~$12 USD)
- Para deploy de todos os contratos

### 2. Endereços Necessários
- **Treasury:** `0x077e8d29e11ff1c0ccb236e0380d0053dcba2b1c`
- **Token LEVE:** `0x67e463AcC3B35406B0f35C8Ed531da89f9670861`

### 3. Ordem de Deploy Sugerida
1. **ERC8183** (Commercial Layer) - Base
2. **ERC8126** (Risk Scoring) - Independente
3. **ERC8021** (Attribution) - Independente
4. **ReputationHook_v2** - Precisa de ERC8183
5. **VestingGateIO** - Precisa do Token LEVE

---

## 📋 SCRIPTS DE DEPLOY PRONTOS

| Script | Função |
|--------|--------|
| `scripts/deploy-reputation-v2.js` | Deploy ReputationHook |
| `scripts/deploy-erc8183.js` | Deploy ERC8183 |
| `scripts/deploy-all.js` | Deploy de todos |

---

## 🚀 COMANDO PARA DEPLOY

```bash
cd /root/openclaw/erc-8183
npx hardhat run scripts/deploy-all.js --network bsc
```

**Tempo estimado:** 2-5 minutos  
**Custo estimado:** 0.015-0.025 BNB

---

## 📞 SUPORTE

**Dúvidas?** Consulte:
- `README.md` - Visão geral
- `IMPLEMENTACAO_COMPLETA.md` - Detalhes técnicos
- `DEPLOY_BSC_RAPIDO.md` - Guia rápido de deploy

---

**Status:** ✅ PRONTO PARA DEPLOY  
**Última Atualização:** 2026-03-11
