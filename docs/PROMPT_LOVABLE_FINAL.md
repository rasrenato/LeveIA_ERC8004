Crie um redesign completo e profissional do site levecoin.io (já existe, mas está "amador" - precisa de upgrade urgente).

## 🎯 CONTEXTO

**Site atual:** https://levecoin.io (no ar, mas design amador)

**Objetivo:** Recriar com design profissional (estilo Stripe/Coinbase) mantendo funcionalidades e adicionando transparência on-chain dos contratos.

**Leve IA:** Criptomoeda BEP-20 na BSC que facilita cripto para leigos com transparência total.

---

## 📦 CONTRATOS INTELIGENTES (MOSTRAR TODOS NO SITE)

### 1. 🪙 Token LEVE V2 (Principal)
```
Endereço: 0x67e463AcC3B35406B0f35C8Ed531da89f9670861
Rede: Binance Smart Chain (BSC)
Max Supply: 500.000.000 LEVE
Holders: 53+ (meta: 100+)
BscScan: https://bscscan.com/token/0x67e463AcC3B35406B0f35C8Ed531da89f9670861
```

### 2. 🔒 Vesting Pré-venda (USDT)
```
Endereço: 0xD8E4226eD752fCc7488410C6d34f73007FD66059
Função: Venda com vesting (anti-dump)
Moeda: USDT (BSC)
```

### 3. 💰 Venda PIX (Brasil)
```
Endereço: 0x87FAe24D2C69aF7F9a1CB340293F683E77Ae1A30
Função: Venda direta via PIX
Moeda: BRL
```

### 4. 🏦 Cofre Migration
```
Endereço: 0x4474Ad931757466B401ABE0B93445E8cB21ddCc6
Função: Migração entre contratos
```

---

## 🎨 IDENTIDADE VISUAL

**Cores:**
- Primária: #00D4AA (verde água)
- Secundária: #FFFFFF
- Fundo: #F8F9FA
- Texto: #1A1A1A
- Sucesso: #00D4AA
- Erro: #FF4444

**Logo:** 🍃
**Estilo:** Stripe + Coinbase (limpo, moderno, confiável)

---

## 📄 PÁGINAS PARA CRIAR

### **1. HOMEPAGE (/)**

**Hero Section:**
```
┌─────────────────────────────────────────────┐
│  🍃 LEVE IA                                 │
│  Verifiable AI is the only AI               │
│                                             │
│  Facilitando cripto para leigos com         │
│  transparência total via Blockchain         │
│                                             │
│  [🚀 Comprar LEVE]  [📊 Dashboard]         │
│                                             │
│  🪙 53+ Holders | 🔒 Vesting | ✅ BSC      │
└─────────────────────────────────────────────┘
```

**Section: Contratos (Cards)**
```
┌─────────────────────────────────────────────┐
│  📦 CONTRATOS INTELIGENTES                  │
│  Transparência total on-chain               │
├─────────────────────────────────────────────┤
│  ┌────────────┐ ┌────────────┐             │
│  │ 🪙 Token   │ │ 🔒 Vesting │             │
│  │ LEVE V2    │ │ USDT       │             │
│  │ 0x67e463..│ │ 0xD8E422..│             │
│  │ [BscScan]  │ │ [Comprar]  │             │
│  └────────────┘ └────────────┘             │
│  ┌────────────┐ ┌────────────┐             │
│  │ 🏦 Migration│ │ 💰 PIX    │             │
│  │ Cofre      │ │ Brasil     │             │
│  │ 0x4474Ad..│ │ 0x87FAe2..│             │
│  │ [BscScan]  │ │ [Comprar]  │             │
│  └────────────┘ └────────────┘             │
└─────────────────────────────────────────────┘
```

**Section: Stats On-Chain (Tempo Real)**
```
┌─────────────────────────────────────────────┐
│  📊 AO VIVO - DADOS ON-CHAIN                │
├─────────────────────────────────────────────┤
│  Holders: 53+ 🟢                            │
│  Price: $0.XX USDT 🟢                       │
│  Market Cap: $XXX,XXX 🟢                    │
│  Volume 24h: $XX,XXX 🟢                     │
│                                             │
│  🎯 META GATE.IO                            │
│  Arrecadado: $XX,XXX / $30,000             │
│  ████████░░░░░░░░░░ 45%                    │
│  [Quero contribuir →]                       │
└─────────────────────────────────────────────┘
```

**Section: Alpha Signals Preview**
```
┌─────────────────────────────────────────────┐
│  📊 ALPHA SIGNALS - Sinais de Trading       │
│  Prova de yield on-chain                    │
├─────────────────────────────────────────────┤
│  [2-3 cards de sinais de exemplo]           │
│  [Ver todos os sinais →]                    │
└─────────────────────────────────────────────┘
```

---

### **2. DASHBOARD (/dashboard)**

**Conteúdo:**
- Alpha Signals completo (todos os sinais)
- Gráfico de preço (24h, 7d, 30d)
- Holders growth (gráfico)
- Volume (gráfico)
- Transações recentes (lista)
- Progresso Gate.io

**API:**
```javascript
GET /api/alpha/signals
GET /api/contracts/stats (BscScan proxy)
GET /api/vesting/progress
```

---

### **3. COMPRAR (/buy)**

**Seções:**
1. **Opção USDT (Global)**
   - Explicação: "Compre com USDT na BSC"
   - Contrato vesting: 0xD8E4226eD752fCc7488410C6d34f73007FD66059
   - Botão: "Conectar Wallet"
   - Widget de compra (Web3)

2. **Opção PIX (Brasil)**
   - Explicação: "Compre com PIX (Brasil)"
   - Contrato: 0x87FAe24D2C69aF7F9a1CB340293F683E77Ae1A30
   - Botão: "Gerar PIX"
   - QR Code + Copy/Paste

3. **Vesting (Segurança)**
   - Explicação: "Tokens bloqueados = Anti-dump"
   - Visual: Timeline de vesting
   - Link contrato

4. **FAQ**
   - Como compro?
   - O que é vesting?
   - Quando lista na Gate.io?
   - É seguro?

---

### **4. ALPHA (/alpha)**

**Conteúdo:**
- Dashboard Alpha Signals completo
- Performance histórica (PnL acumulado)
- Wins vs Losses (gráfico)
- Distribuição por par (pizza)
- Métricas: Win rate, melhor trade, pior trade
- Pricing: R$49/mês (fundadores)
- Botão: "Assinar Agora"

---

### **5. SOBRE (/about)**

**Conteúdo:**
- Missão Leve IA
- Equipe (Renato + Agentes IA)
- Todos os 4 contratos (links)
- Transparência (BscScan)
- Roadmap (link)

---

## 📦 FEATURES OBRIGATÓRIAS

### **FEATURE 1: WIDGET DE CHAT (Support Agent)**

**Posição:** Canto inferior direito (fixed)

**Componentes:**
- ChatFloatingButton (60x60px, 🍃, #00D4AA)
- ChatModal (400x600px desktop, full mobile)

**Mensagens:**
- Welcome: "Olá! Sou o Support Agent da Leve IA. 🍃\n\nComo posso te ajudar?"
- Waiting: "Estou verificando, um momento..."
- Timeout: "Ainda estou aqui! Me chame se precisar. 🍃"

**Perguntas Frequentes:**
1. "Como compro LEVE?" → USDT (levecoin.io) ou PIX (levenopix.com.br)
2. "O que é vesting?" → Tokens bloqueados, anti-dump, segurança
3. "Quando lista na Gate.io?" → Arrecadando $30k (mostrar progresso)
4. "É seguro?" → Contrato BSC verificado, 53+ holders
5. "Qual o preço?" → coinmarketleve.com

**API:**
```javascript
POST /api/chat/send
POST /api/chat/receive
```

---

### **FEATURE 2: CAPTURA DE LEADS**

**Componente:** LeadCaptureModal

**Trigger:** 30s na página OU exit intent

**Form:**
- Nome (required)
- Email (required)
- Telegram (optional)
- Interesse (select): Alpha Signals, Comprar USDT, Comprar PIX, Parceria

**API:**
```javascript
POST /api/lead
Body: { name, email, telegram, interest, url, userId }
```

**Pós-submit:**
- Toast: "🍃 Obrigado! Sales Agent vai te contactar."
- localStorage: lead_captured = true

---

### **FEATURE 3: ALPHA SIGNALS WIDGET**

**Componente:** AlphaSignalsWidget

**Local:** /dashboard e /alpha

**Estrutura:**
```
┌─────────────────────────────────┐
│ 📊 Alpha Signals 🔴 AO VIVO    │
├─────────────────────────────────┤
│ ┌──────┐ ┌──────┐ ┌──────┐    │
│ │BTC   │ │ETH   │ │SOL   │    │
│ │LONG🟢│ │SHORT🔴│ │LONG🟢│    │
│ │Entrada│ │Entrada│ │Entrada│   │
│ │Alvo  │ │Alvo  │ │Alvo  │    │
│ │Stop  │ │Stop  │ │Stop  │    │
│ │R/R   │ │R/R   │ │R/R   │    │
│ │+12%🟢│ │-3%🔴 │ │+8%🟢 │    │
│ └──────┘ └──────┘ └──────┘    │
└─────────────────────────────────┘
```

**Cores:**
- LONG: Border verde #00D4AA
- SHORT: Border vermelha #FF4444
- PnL+: Verde, PnL-: Vermelho

**API:**
```javascript
GET /api/alpha/signals
Refresh: 60 segundos
```

---

### **FEATURE 4: BSCSCAN INTEGRATION**

**Componente:** ContractViewer

**Função:** Mostrar dados on-chain em tempo real

**API BscScan:**
```javascript
const BSCSCAN_API = 'https://api.bscscan.com/api';
const CONTRACT = '0x67e463AcC3B35406B0f35C8Ed531da89f9670861';

// Token supply
fetch(`${BSCSCAN_API}?module=stats&action=tokensupply&contractaddress=${CONTRACT}`)

// Token price
fetch(`${BSCSCAN_API}?module=stats&action=tokenprice&contractaddress=${CONTRACT}`)

// Holders
fetch(`${BSCSCAN_API}?module=account&action=tokenholders&contractaddress=${CONTRACT}`)
```

**Dados para mostrar:**
- Holders count (refresh 5min)
- Preço USDT (refresh 1min)
- Market cap
- Volume 24h
- Transações recentes

---

### **FEATURE 5: GATE.IO PROGRESS**

**Componente:** GateioProgress

**Meta:** $30.000 USD (restantes)

**Visual:**
```
┌─────────────────────────────────┐
│ 🎯 META GATE.IO                 │
│ Arrecadar $30k para listagem   │
├─────────────────────────────────┤
│ Arrecadado: $XX,XXX            │
│ ████████░░░░░░░░░░ 45%         │
│ Restam: $XX,XXX                │
│ [Quero contribuir →]           │
└─────────────────────────────────┘
```

---

## 🔧 COMPONENTES TÉCNICOS

### **UserTrackingService**
```javascript
class UserTrackingService {
  constructor() {
    this.userId = localStorage.getItem('leve_user_id') || 
      'user_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    localStorage.setItem('leve_user_id', this.userId);
  }
  
  trackPageview(url) {
    fetch('/api/track', {
      method: 'POST',
      body: JSON.stringify({ event: 'pageview', userId: this.userId, url })
    });
  }
  
  trackExitIntent() {
    fetch('/api/track', {
      method: 'POST',
      body: JSON.stringify({ event: 'exit_intent', userId: this.userId })
    });
  }
}
```

### **BscScanService**
```javascript
class BscScanService {
  async getTokenStats() {
    const res = await fetch('/api/contracts/stats');
    return await res.json();
  }
  
  async getVestingProgress() {
    const res = await fetch('/api/vesting/progress');
    return await res.json();
  }
}
```

### **ChatService**
```javascript
async function sendMessage(message) {
  const res = await fetch('/api/chat/send', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ userId, message, sessionId: Date.now() })
  });
  return await res.json();
}
```

---

## 🎨 CSS VARIABLES

```css
:root {
  --primary: #00D4AA;
  --primary-hover: #00b894;
  --text: #1A1A1A;
  --text-light: #666666;
  --bg: #F8F9FA;
  --border: #E0E0E0;
  --success: #00D4AA;
  --error: #FF4444;
  --shadow-md: 0 4px 6px rgba(0,0,0,0.1);
  --shadow-lg: 0 10px 20px rgba(0,0,0,0.15);
  --radius: 12px;
}
```

---

## 📱 RESPONSIVIDADE

**Mobile (< 768px):**
- Chat: Full screen
- Cards: 1 coluna
- Stats: Stack vertical

**Tablet (768-1024px):**
- Chat: 90% width
- Cards: 2 colunas
- Stats: 2 colunas

**Desktop (> 1024px):**
- Chat: 400x600px
- Cards: 2-4 colunas
- Stats: 4 colunas

---

## ✅ CHECKLIST

**Frontend:**
- [ ] Homepage (redesign completo)
- [ ] Dashboard (/dashboard)
- [ ] Comprar (/buy)
- [ ] Alpha (/alpha)
- [ ] Sobre (/about)
- [ ] ChatFloatingButton
- [ ] ChatModal
- [ ] LeadCaptureModal
- [ ] AlphaSignalsWidget
- [ ] ContractViewer (BscScan)
- [ ] GateioProgress
- [ ] CSS completo
- [ ] Responsividade

**Backend:**
- [ ] POST /api/chat/send
- [ ] POST /api/chat/receive
- [ ] POST /api/lead
- [ ] GET /api/alpha/signals
- [ ] GET /api/contracts/stats
- [ ] GET /api/vesting/progress
- [ ] POST /api/track

**Integrações:**
- [ ] BscScan API
- [ ] Telegram (Support Agent)
- [ ] Telegram (Sales Agent)
- [ ] Web3 (ler contratos)

**Testes:**
- [ ] Chat funciona
- [ ] Lead capturado
- [ ] Alpha atualiza (60s)
- [ ] BscScan carrega
- [ ] Responsividade
- [ ] Lighthouse 90+

---

## 🎯 CRITÉRIOS DE SUCESSO

1. **Design:** Profissional (Stripe/Coinbase level)
2. **Transparência:** 4 contratos visíveis, dados on-chain
3. **Performance:** Lighthouse 90+
4. **Conversão:** 53 → 100+ holders em 30 dias
5. **Suporte:** Resposta < 30s
6. **Leads:** 10+/dia

---

## 🔗 LINKS

- **Site:** https://levecoin.io
- **PIX:** https://levenopix.com.br
- **Dashboard:** https://coinmarketleve.com
- **Roadmap:** https://roadmapdaleve.com.br
- **BscScan:** https://bscscan.com/token/0x67e463AcC3B35406B0f35C8Ed531da89f9670861

---

**🍃 Leve IA - Verifiable AI is the only AI**