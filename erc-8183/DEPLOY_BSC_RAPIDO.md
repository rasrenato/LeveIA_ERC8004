# 🚀 Deploy ERC-8183 na BSC - Guia Rápido

**Tempo Total:** ~1 hora  
**Custo:** ~$5-10 em BNB

---

## 📋 **PRÉ-REQUISITOS:**

### **1. Ter BNB na Wallet:**

```
Wallet: 0x077e8d29e11ff1c0ccb236e0380d0053dcba2b1c
Necessário: 0.1 BNB (~$20-35)
Suficiente: 0.02 BNB (~$5-10)
```

### **2. Como Conseguir BNB:**

**Opção A: Binance**
```
1. Comprar BNB na Binance
2. Retirar para: 0x077e8d29e11ff1c0ccb236e0380d0053dcba2b1c
3. Rede: BSC (BEP-20)
4. Tempo: 5-15 minutos
```

**Opção B: PancakeSwap (Se tem USDT na BSC)**
```
1. Acessar: https://pancakeswap.finance
2. Swap: USDT → BNB
3. Conectar wallet: 0x077e...
4. Tempo: 2-5 minutos
```

**Opção C: Bridge da Base**
```
1. Bridge: USDT na Base → USDT na BSC
2. Swap: USDT → BNB (PancakeSwap)
3. Tempo: 10-20 minutos
```

---

## 🎯 **PASSO-A-PASSO DO DEPLOY:**

### **Passo 1: Transferir BNB** ⏳

```
✅ Você transfere 0.1 BNB para:
   0x077e8d29e11ff1c0ccb236e0380d0053dcba2b1c

✅ Aguardar confirmação (~5 min)
```

### **Passo 2: Configurar .env** 🔧

```bash
cd /root/openclaw/erc-8183
cp .env.example .env
nano .env

# Editar:
PRIVATE_KEY=sua-chave-privada
BSCSCAN_API_KEY=sua-api-key (opcional, pra verificar)
```

### **Passo 3: Rodar Deploy** 🚀

```bash
cd /root/openclaw/erc-8183
node scripts/deploy-bsc.js
```

### **Passo 4: Verificar no BSCScan** ✅

```bash
# Se tiver API key:
npx hardhat verify --network bsc <CONTRACT_ADDRESS> <TREASURY> <FEE_BPS>
```

---

## 📊 **CUSTOS ESTIMADOS:**

| Item | Gas | BNB | USD |
|------|-----|-----|-----|
| Deploy ERC8183 | ~2M | ~0.01 | ~$5 |
| Deploy ReputationHook | ~1M | ~0.005 | ~$2.50 |
| **TOTAL** | **~3M** | **~0.015 BNB** | **~$7.50** |

**Margem de segurança:** 0.1 BNB sobra ~0.085 BNB

---

## ✅ **CHECKLIST:**

- [ ] BNB transferido (0.1 BNB)
- [ ] BNB confirmado na wallet
- [ ] Private key no .env
- [ ] Deploy rodou com sucesso
- [ ] Contratos verificados no BSCScan
- [ ] Endereços salvos em addresses-bsc.json

---

## 🔗 **LINKS ÚTEIS:**

| Serviço | Link |
|---------|------|
| **BSCScan** | https://bscscan.com |
| **PancakeSwap** | https://pancakeswap.finance |
| **Binance** | https://binance.com |
| **Bridge Base→BSC** | https://bridge.base.org |

---

## 📝 **PÓS-DEPLOY:**

### **O Que Fazer Depois:**

1. [ ] Adicionar contratos ao site Leve IA
2. [ ] Atualizar documentação
3. [ ] Testar com token LEVE
4. [ ] Anunciar para 53+ holders
5. [ ] Integrar com Alpha Signals

### **Próximos Contratos (Fase 2):**

- [ ] ERC-8126 (Risk Scoring)
- [ ] ERC-8021 (Attribution)
- [ ] x402 Integration (código)

---

## 💬 **SUPORTE:**

**Se algo der errado:**

| Erro | Solução |
|------|---------|
| Insufficient BNB | Transferir mais 0.1 BNB |
| Private key inválida | Verificar formato no .env |
| Deploy falhou | Checar gas price, retry |
| BSCScan verify falhou | Aguardar 1-2 min, retry |

---

**Pronto para deploy! Só precisar do BNB na wallet.** 🍃
