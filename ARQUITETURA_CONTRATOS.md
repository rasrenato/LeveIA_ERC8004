# 🏗️ ARQUITETURA DOS CONTRATOS LEVE IA

**Data:** 2026-03-11 14:00 UTC  
**Autor:** Cabral (CEO Agent)  
**Status:** ⚠️ **ANÁLISE DE ARQUITETURA**

---

## 📊 **SITUAÇÃO ATUAL:**

### **5 Contratos Independentes:**

```
┌─────────────────────────────────────────────────────────┐
│           ECOSSISTEMA LEVE IA (BSC)                     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. ERC-8183 (Alpha Signals)                            │
│     0x5FbDB2315678afecb367f032d93F642f64180aa3          │
│                                                         │
│  2. ERC-8004 (Reputation)                               │
│     0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512          │
│                                                         │
│  3. ERC-8126 (Risk Scoring)                             │
│     0x9fE46736679d2D9a65F0992F2272dE9f3c7fa6e0          │
│                                                         │
│  4. ERC-8021 (Attribution)                              │
│     0xCf7Ed3AccA5a467e9e704C703E8D87F634fB0Fc9          │
│                                                         │
│  5. Token LEVE (BEP-20)                                 │
│     0x67e463AcC3B35406B0f35C8Ed531da89f9670861          │
│                                                         │
│  ⚠️ PROBLEMA: Contratos NÃO se comunicam entre si!      │
│  ⚠️ Dashboard mostra só 1 endereço (ERC-8183)           │
└─────────────────────────────────────────────────────────┘
```

---

## ❌ **PROBLEMAS IDENTIFICADOS:**

### **1. No Dashboard (App.jsx):**

```javascript
// SÓ MOSTRA UM CONTRATO!
const CONTRACT_ADDRESS = '0x5FbDB2315678afecb367f032d93F642f64180aa3'
// Cadê os outros 4?
```

### **2. Comunicação Entre Contratos:**

```
ERC-8183 → ReputationHook → ERC-8004 ✅ (parcial)
ERC-8183 → ERC-8126 ❌ (NÃO tem integração)
ERC-8183 → ERC-8021 ❌ (NÃO tem integração)
ERC-8183 → Token LEVE ❌ (NÃO tem integração)
```

### **3. Ponto Único de Entrada:**

```
❌ Não tem contrato Registry/Orchestrator
❌ Dashboard precisa saber os 5 endereços manualmente
❌ Se mudar um endereço, tem que atualizar em vários lugares
```

---

## ✅ **SOLUÇÃO PROPOSTA:**

### **Opção A: Contrato Registry (RECOMENDADA)**

Criar um contrato **`LeveIARegistry`** que:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract LeveIARegistry {
    // Endereços dos contratos
    address public erc8183;      // Alpha Signals
    address public erc8004;      // Reputation
    address public erc8126;      // Risk Scoring
    address public erc8021;      // Attribution
    address public leveToken;    // Token LEVE
    address public owner;
    
    // Eventos
    event ContractUpdated(string name, address oldAddr, address newAddr);
    
    constructor(
        address _erc8183,
        address _erc8004,
        address _erc8126,
        address _erc8021,
        address _leveToken
    ) {
        owner = msg.sender;
        erc8183 = _erc8183;
        erc8004 = _erc8004;
        erc8126 = _erc8126;
        erc8021 = _erc8021;
        leveToken = _leveToken;
    }
    
    // Funções para atualizar endereços (só owner)
    function updateContract(string calldata name, address newAddr) external {
        require(msg.sender == owner, "Not owner");
        // ... lógica de update
    }
    
    // Funções para obter todos os endereços
    function getAllContracts() external view returns (
        address, address, address, address, address
    ) {
        return (erc8183, erc8004, erc8126, erc8021, leveToken);
    }
}
```

**Vantagens:**
- ✅ Ponto único de entrada
- ✅ Fácil atualizar endereços
- ✅ Dashboard consulta só o Registry
- ✅ Mais profissional e escalável

**Custo:** ~0.01 BNB (~$6.50) para deploy

---

### **Opção B: Arquivo JSON de Config (Simples)**

Manter endereços em um arquivo JSON:

```json
{
  "registry": "0x...",
  "contracts": {
    "erc8183": "0x5FbDB23...",
    "erc8004": "0xe7f1725...",
    "erc8126": "0x9fE4673...",
    "erc8021": "0xCf7Ed3A...",
    "leveToken": "0x67e463A..."
  }
}
```

**Vantagens:**
- ✅ Sem custo de deploy
- ✅ Fácil de atualizar
- ✅ Dashboard lê do JSON

**Desvantagens:**
- ❌ Não é on-chain
- ❌ Menos "blockchain native"
- ❌ Não tem eventos de atualização

---

### **Opção C: Dashboard com Múltiplos Endereços (Atual)**

Continuar como está, mas atualizar o App.jsx:

```javascript
const CONTRACTS = {
  ERC8183: '0x5FbDB23...',
  ERC8004: '0xe7f1725...',
  ERC8126: '0x9fE4673...',
  ERC8021: '0xCf7Ed3A...',
  TOKEN: '0x67e463A...'
}
```

**Vantagens:**
- ✅ Sem custo
- ✅ Já implementado

**Desvantagens:**
- ❌ Endereços hard-coded
- ❌ Se mudar, tem que redeploys
- ❌ Não escala

---

## 🎯 **MINHA RECOMENDAÇÃO:**

### **Criar LeveIARegistry AGORA!**

**Por quê:**
1. ✅ Profissional e escalável
2. ✅ Ponto único de verdade
3. ✅ Fácil de integrar com dashboard
4. ✅ Mostra maturidade pra Gate.io
5. ✅ Baixo custo (~$6.50)

**Timeline:**
- Criar contrato: 30 min
- Testar: 30 min
- Deploy na BSC: 10 min
- Atualizar dashboard: 30 min
- **Total: ~2 horas**

---

## 📋 **PRÓXIMOS PASSOS (SE APROVAR):**

| Passo | Ação | Tempo |
|-------|------|-------|
| 1 | Criar `LeveIARegistry.sol` | 30 min |
| 2 | Testar localmente | 30 min |
| 3 | Deploy na BSC | 10 min |
| 4 | Atualizar dashboard | 30 min |
| 5 | Atualizar documentação | 20 min |

---

## 💬 **RENATO, QUAL VOCÊ QUER?**

| Opção | Descrição | Custo | Minha Recomendação |
|-------|-----------|-------|-------------------|
| **A** | Contrato Registry | ~$6.50 | ⭐⭐⭐⭐⭐ |
| **B** | Arquivo JSON | $0 | ⭐⭐⭐ |
| **C** | Manter como está | $0 | ⭐⭐ |

**Me fala qual quer que eu executo AGORA!** 🍃
