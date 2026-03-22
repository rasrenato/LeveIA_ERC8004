# ERC-8183 BSC Deployment Guide

**Rede:** Binance Smart Chain (BSC)  
**Chain ID:** 56  
**Gas Token:** BNB  
**Custo Estimado:** ~$5-10 por deploy

---

## 📋 **PRÉ-REQUISITOS:**

### **1. BNB na Wallet:**

```
Wallet: 0x077e8d29e11ff1c0ccb236e0380d0053dcba2b1c
Necessário: 0.1-0.2 BNB (~$20-35)
```

### **2. Configurar Hardhat para BSC:**

```javascript
// hardhat.config.js
networks: {
  bsc: {
    url: "https://bsc-dataseed.binance.org/",
    chainId: 56,
    accounts: [process.env.PRIVATE_KEY]
  },
  bscTestnet: {
    url: "https://data-seed-prebsc-1-s1.binance.org:8545/",
    chainId: 97,
    accounts: [process.env.PRIVATE_KEY]
  }
}
```

---

## 🚀 **COMANDO DE DEPLOY:**

### **Testnet (Recomendado Primeiro):**

```bash
export PRIVATE_KEY="sua-chave-privada"
export BSC_TESTNET_RPC="https://data-seed-prebsc-1-s1.binance.org:8545/"

npx hardhat run scripts/deploy.js --network bscTestnet
```

### **Mainnet (Produção):**

```bash
export PRIVATE_KEY="sua-chave-privada"
export BSC_MAINNET_RPC="https://bsc-dataseed.binance.org/"

npx hardhat run scripts/deploy.js --network bsc
```

---

## 📊 **CUSTOS ESTIMADOS (BSC):**

| Contrato | Gas | BNB | USD |
|----------|-----|-----|-----|
| ERC8183 | ~2,000,000 | ~0.01 BNB | ~$5 |
| ReputationHook | ~1,000,000 | ~0.005 BNB | ~$2.50 |
| **TOTAL** | **~3,000,000** | **~0.015 BNB** | **~$7.50** |

---

## 🔍 **VERIFICAÇÃO NO BSCSCAN:**

Após deploy:

```bash
npx hardhat verify --network bsc <CONTRACT_ADDRESS> <TREASURY> <FEE_BPS>
```

**Links:**
- Testnet: https://testnet.bscscan.com
- Mainnet: https://bscscan.com

---

## 🔗 **INTEGRAÇÃO COM TOKEN LEVE:**

**Token LEVE (BEP-20):**
```
Endereço: 0x67e463AcC3B35406B0f35C8Ed531da89f9670861
Rede: BSC Mainnet
```

**Configurar no contrato:**
```javascript
const tokenAddress = "0x67e463AcC3B35406B0f35C8Ed531da89f9670861";
```

---

## ✅ **CHECKLIST PRÉ-DEPLOY:**

- [ ] BNB na wallet (0.1-0.2 BNB)
- [ ] Private key configurada
- [ ] Hardhat configurado para BSC
- [ ] Testes passando (7/7)
- [ ] Token LEVE endereço configurado
- [ ] Treasury address configurado

---

## 📝 **PÓS-DEPLOY:**

1. [ ] Verificar contrato no BSCScan
2. [ ] Adicionar ao site Leve IA
3. [ ] Atualizar documentação
4. [ ] Testar com token LEVE
5. [ ] Anunciar para holders

---

**Pronto para deploy na BSC!**
