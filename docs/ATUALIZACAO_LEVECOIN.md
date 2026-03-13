# 🍃 LEVE IA - ATUALIZAÇÃO DO SITE LEVECOIN.IO

**Informações para o lovable.dev e equipe de desenvolvimento**

---

## 🎯 CONTEXTO ATUAL

**Já temos um site no ar:** https://levecoin.io

**Status:** Funcional, mas "amador" comparado ao potencial.

**Objetivo:** Recriar o site com design profissional (estilo Stripe/Coinbase) mantendo as funcionalidades existentes e adicionando:
- Support Agent 24/7 (chat)
- Captura de leads (Sales Agent)
- Dashboard Alpha Signals
- Transparência total dos contratos (on-chain)

---

## 📦 CONTRATOS INTELIGENTES (MOSTRAR NO SITE)

### **1. 🪙 Token Oficial LEVE V2 (BEP-20)**
```
Endereço: 0x67e463AcC3B35406B0f35C8Ed531da89f9670861
Rede: Binance Smart Chain (BSC)
Nome: LeveAiV2
Solidity: v0.8.20 (verificado no BscScan)
Max Supply: 500.000.000 LEVE
Holders: 53+ (meta: aumentar)
BscScan: https://bscscan.com/token/0x67e463AcC3B35406B0f35C8Ed531da89f9670861
```

**O que mostrar no site:**
- ✅ Número de holders (em tempo real via API BscScan)
- ✅ Preço atual (USDT)
- ✅ Market cap
- ✅ Volume 24h
- ✅ Link direto BscScan
- ✅ Contrato verificado (badge de segurança)

---

### **2. 🏦 Cofre Migration**
```
Endereço: 0x4474Ad931757466B401ABE0B93445E8cB21ddCc6
Função: Migração de tokens entre contratos
```

**O que mostrar no site:**
- ✅ Explicação: "Migração segura entre versões do token"
- ✅ Link BscScan
- ✅ Status: Ativo

---

### **3. 🔒 Pré-venda Vesting (USDT)**
```
Endereço: 0xD8E4226eD752fCc7488410C6d34f73007FD66059
Função: Venda com vesting (tokens bloqueados, anti-dump)
Moeda: USDT (BSC)
```

**O que mostrar no site:**
- ✅ Explicação: "Vesting protege investidores - tokens bloqueados, sem dump"
- ✅ Total arrecadado (USDT)
- ✅ Tokens vendidos
- ✅ Tokens disponíveis
- ✅ Progress bar da pré-venda
- ✅ Link BscScan
- ✅ Botão: "Comprar LEVE com USDT"

---

### **4. 💰 Venda PIX (Brasil)**
```
Endereço: 0x87FAe24D2C69aF7F9a1CB340293F683E77Ae1A30
Função: Venda direta via PIX (Brasil)
```

**O que mostrar no site:**
- ✅ Explicação: "Compra direta com PIX - Brasil"
- ✅ Total arrecadado (BRL)
- ✅ Tokens vendidos
- ✅ Link BscScan
- ✅ Botão: "Comprar LEVE com PIX"

---

## 🎨 NOVO DESIGN (lovable.dev)

### **Homepage (levecoin.io)**

**Seção 1: Hero**
```
┌─────────────────────────────────────────────┐
│                                             │
│   🍃 LEVE IA                                │
│   Verifiable AI is the only AI              │
│                                             │
│   Facilitando o uso de cripto para leigos   │
│   com transparência total via Blockchain    │
│                                             │
│   [🚀 Comprar LEVE]  [📊 Ver Dashboard]    │
│                                             │
│   🪙 53+ Holders | 🔒 Vesting | ✅ BSC     │
│                                             │
└─────────────────────────────────────────────┘
```

**Seção 2: Contratos (Transparência)**
```
┌─────────────────────────────────────────────┐
│  📦 CONTRATOS INTELIGENTES                  │
│  Transparência total on-chain               │
├─────────────────────────────────────────────┤
│  ┌──────────────┐ ┌──────────────┐         │
│  │ 🪙 Token     │ │ 🔒 Vesting   │         │
│  │ LEVE V2      │ │ USDT         │         │
│  │ 0x67e463... │ │ 0xD8E422...  │         │
│  │ 53+ Holders │ │ Anti-dump    │         │
│  │ [BscScan →] │ │ [Comprar →]  │         │
│  └──────────────┘ └──────────────┘         │
│  ┌──────────────┐ ┌──────────────┐         │
│  │ 🏦 Migration │ │ 💰 PIX       │         │
│  │ Cofre        │ │ Brasil       │         │
│  │ 0x4474Ad... │ │ 0x87FAe2...  │         │
│  │ Seguro       │ │ BRL          │         │
│  │ [BscScan →] │ │ [Comprar →]  │         │
│  └──────────────┘ └──────────────┘         │
└─────────────────────────────────────────────┘
```

**Seção 3: Stats em Tempo Real**
```
┌─────────────────────────────────────────────┐
│  📊 AO VIVO - DADOS ON-CHAIN                │
├─────────────────────────────────────────────┤
│  Holders: 53+ 🟢                            │
│  Price: $0.XX USDT 🟢                       │
│  Market Cap: $XXX,XXX 🟢                    │
│  Volume 24h: $XX,XXX 🟢                     │
│  Total Arrecadado: $XX,XXX / $30,000       │
│  ████████░░░░░░░░░░ 45%                    │
└─────────────────────────────────────────────┘
```

**Seção 4: Alpha Signals**
```
┌─────────────────────────────────────────────┐
│  📊 ALPHA SIGNALS - SINAIS DE TRADING       │
│  Prova de yield on-chain                    │
├─────────────────────────────────────────────┤
│  [Cards de sinais - ver feature 3]          │
│                                             │
│  [Ver todos os sinais →]                    │
└─────────────────────────────────────────────┘
```

**Seção 5: Roadmap**
```
┌─────────────────────────────────────────────┐
│  📍 ROADMAP                                 │
│  https://roadmapdaleve.com.br               │
├─────────────────────────────────────────────┤
│  ✅ Fase 1: Contrato + Vesting             │
│  ✅ Fase 2: Alpha Signals                  │
│  🔄 Fase 3: Listagem Gate.io ($30k)        │
│  ⏳ Fase 4: Expansion                      │
└─────────────────────────────────────────────┘
```

---

## 📦 FEATURES PARA IMPLEMENTAR

### **FEATURE 1: WIDGET DE CHAT (Support Agent)**

**Já especificado anteriormente** - Support Agent 24/7 respondendo em < 30 segundos.

**Perguntas frequentes:**
1. "Como compro LEVE?" → Explicar USDT (levecoin.io) e PIX (levenopix.com.br)
2. "O que é vesting?" → Tokens bloqueados no contrato, anti-dump, segurança
3. "Quando lista na Gate.io?" → Arrecadando $30k restantes (mostrar progresso)
4. "É seguro?" → Contrato BSC verificado, 53+ holders, vesting
5. "Qual o preço?" → coinmarketleve.com (dados on-chain)

---

### **FEATURE 2: CAPTURA DE LEADS (Sales Agent)**

**Já especificado anteriormente** - Modal após 30s ou exit intent.

**Interesses:**
- Alpha Signals (Sinais de Trading)
- Comprar LEVE (Pré-venda USDT)
- Comprar LEVE (PIX Brasil)
- Parceria

---

### **FEATURE 3: DASHBOARD ALPHA SIGNALS**

**Já especificado anteriormente** - Sinais em tempo real, refresh 60s.

---

### **FEATURE 4: TRANSPARENTIA ON-CHAIN (NOVO!)**

**Componente:** ContractViewer

**Função:** Mostrar dados dos contratos em tempo real via API BscScan

**API BscScan:**
```javascript
// Get token holders count
https://api.bscscan.com/api?module=stats&action=tokensupply&contractaddress=0x67e463AcC3B35406B0f35C8Ed531da89f9670861

// Get token price
https://api.bscscan.com/api?module=stats&action=tokenprice&contractaddress=0x67e463AcC3B35406B0f35C8Ed531da89f9670861

// Get contract transactions
https://api.bscscan.com/api?module=account&action=txlist&address=0x67e463AcC3B35406B0f35C8Ed531da89f9670861
```

**O que mostrar:**
- Holders count (atualiza a cada 5min)
- Preço USDT (atualiza a cada 1min)
- Transações recentes (últimas 10)
- Total de tokens em circulação
- Progresso da pré-venda (USDT arrecadado / meta)

---

### **FEATURE 5: PROGRESSO GATE.IO (NOVO!)**

**Componente:** GateioProgress

**Função:** Mostrar progresso da arrecadação para listagem

**Meta:** $30.000 USD restantes (total $190k, já pagos $12k)

**Visual:**
```
┌─────────────────────────────────────────────┐
│  🎯 META GATE.IO                            │
│  Arrecadar $30.000 USD para listagem       │
├─────────────────────────────────────────────┤
│  Arrecadado: $XX,XXX                       │
│  ████████░░░░░░░░░░ 45%                    │
│  Restam: $XX,XXX                           │
│                                             │
│  [Quero contribuir →]                       │
└─────────────────────────────────────────────┘
```

---

## 🔧 INTEGRAÇÕES TÉCNICAS

### **BscScan API**
```javascript
const BSCSCAN_API = 'https://api.bscscan.com/api';
const CONTRACT_ADDRESS = '0x67e463AcC3B35406B0f35C8Ed531da89f9670861';

// Get token supply
async function getTokenSupply() {
  const res = await fetch(`${BSCSCAN_API}?module=stats&action=tokensupply&contractaddress=${CONTRACT_ADDRESS}`);
  const data = await res.json();
  return data.result;
}

// Get token price
async function getTokenPrice() {
  const res = await fetch(`${BSCSCAN_API}?module=stats&action=tokenprice&contractaddress=${CONTRACT_ADDRESS}`);
  const data = await res.json();
  return data.result; // ethPrice, btcPrice, usdPrice
}

// Get holders (via token transfers)
async function getHolders() {
  const res = await fetch(`${BSCSCAN_API}?module=account&action=tokenholders&contractaddress=${CONTRACT_ADDRESS}`);
  const data = await res.json();
  return data.result;
}
```

### **Progresso Pré-venda**
```javascript
// Ler saldo USDT do contrato de vesting
const VESTING_CONTRACT = '0xD8E4226eD752fCc7488410C6d34f73007FD66059';
const USDT_CONTRACT = '0x55d398326f99059fF775485246999027B3197955';

async function getVestingProgress() {
  // Chamar contrato USDT balanceOf(VESTING_CONTRACT)
  // Retornar total arrecadado
}
```

---

## 📱 PÁGINAS DO SITE

### **1. Home (/)**
- Hero section
- Contratos (cards)
- Stats on-chain
- Alpha Signals preview
- Roadmap
- CTA: Comprar LEVE

### **2. Dashboard (/dashboard)**
- Alpha Signals completo
- Stats on-chain
- Gráficos (preço, volume, holders)
- Progresso Gate.io

### **3. Comprar (/buy)**
- Opção USDT (BSC)
- Opção PIX (Brasil)
- Explicação vesting
- Links contratos
- FAQ

### **4. Sobre (/about)**
- Missão Leve IA
- Equipe (Renato + agentes IA)
- Contratos (todos os 4)
- Transparência
- Roadmap

### **5. Alpha Signals (/alpha)**
- Dashboard completo
- Sinais em tempo real
- Performance histórica
- Pricing (R$49/mês)
- Signup

---

## ✅ CHECKLIST DE ENTREGA

### **Frontend:**
- [ ] Homepage redesign (profissional)
- [ ] ChatFloatingButton (Support Agent)
- [ ] ChatModal
- [ ] LeadCaptureModal
- [ ] AlphaSignalsWidget
- [ ] ContractViewer (BscScan integration)
- [ ] GateioProgress
- [ ] CSS variables e estilos
- [ ] Responsividade completa

### **Backend:**
- [ ] POST /api/chat/send
- [ ] POST /api/chat/receive
- [ ] POST /api/lead
- [ ] GET /api/alpha/signals
- [ ] GET /api/contracts/stats (BscScan proxy)
- [ ] GET /api/vesting/progress

### **Integrações:**
- [ ] BscScan API (holders, preço, transações)
- [ ] Telegram (Support Agent)
- [ ] Telegram (Sales Agent)
- [ ] Web3 (ler contratos BSC)

### **Testes:**
- [ ] Chat funciona
- [ ] Lead capturado
- [ ] Alpha Signals atualiza
- [ ] Dados BscScan carregam
- [ ] Responsividade
- [ ] Performance (Lighthouse 90+)

---

## 🎯 CRITÉRIOS DE SUCESSO

1. **Design:** Profissional, estilo Stripe/Coinbase
2. **Transparência:** Todos os contratos visíveis, dados on-chain
3. **Performance:** Lighthouse score 90+
4. **Conversão:** Aumentar holders de 53 para 100+ em 30 dias
5. **Suporte:** Resposta em < 30 segundos
6. **Leads:** 10+ leads/dia capturados

---

## 🔗 LINKS OFICIAIS

| Site | URL | Função |
|------|-----|--------|
| **Principal** | https://levecoin.io | Vendas USDT (global) |
| **PIX** | https://levenopix.com.br | Vendas PIX (Brasil) |
| **Dashboard** | https://coinmarketleve.com | Dados de mercado |
| **Roadmap** | https://roadmapdaleve.com.br | Roadmap oficial |
| **BscScan** | https://bscscan.com/token/0x67e463AcC3B35406B0f35C8Ed531da89f9670861 | Contrato verificado |

---

## 🍃 LEVE IA - Verifiable AI is the only AI

**Contratos:**
- Token: `0x67e463AcC3B35406B0f35C8Ed531da89f9670861`
- Vesting USDT: `0xD8E4226eD752fCc7488410C6d34f73007FD66059`
- Venda PIX: `0x87FAe24D2C69aF7F9a1CB340293F683E77Ae1A30`
- Migration: `0x4474Ad931757466B401ABE0B93445E8cB21ddCc6`

**Rede:** Binance Smart Chain (BSC)  
**Holders:** 53+ (meta: 100+ em 30 dias)  
**Meta Gate.io:** $30.000 USD restantes
