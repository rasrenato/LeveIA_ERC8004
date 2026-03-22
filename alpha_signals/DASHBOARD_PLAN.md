# 📊 Alpha Signals Dashboard - Plano de Implementação

**Data:** 05 Mar 2026 01:36 UTC
**Status:** EM ANDAMENTO
**Entrega Estimada:** 06 Mar 07:00 UTC (4-6 horas)

---

## 📋 **COMPONENTES PRINCIPAIS**

### **1. Dashboard Layout (Main)**
- Header com logo + status do agente
- Sidebar de navegação
- Grid de cards com métricas
- Chart de balance (tempo real)

### **2. Economic Status Card**
- Balance atual (USDC)
- Total Revenue
- Total Costs
- Profit/Loss
- Survival Status (🟢/🟡/🔴/💀)

### **3. Signals Leaderboard**
- Top 10 agentes
- Revenue, Win Rate, Score
- Status (active/dead)

### **4. Recent Signals Table**
- Últimos sinais enviados
- Score, Payment, Status
- Asset, Direction, Confidence

### **5. WebSocket Connection**
- Updates em tempo real
- Notificações push
- Auto-reconnect

---

## 🗂️ **ESTRUTURA DE ARQUIVOS**

```
/root/openclaw/alpha_signals/dashboard/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── Header.jsx
│   │   ├── Sidebar.jsx
│   │   ├── StatusCard.jsx
│   │   ├── BalanceChart.jsx
│   │   ├── Leaderboard.jsx
│   │   ├── SignalsTable.jsx
│   │   └── CostFooter.jsx
│   ├── hooks/
│   │   ├── useWebSocket.js
│   │   └── useEconomicData.js
│   ├── pages/
│   │   ├── Dashboard.jsx
│   │   └── AgentDetail.jsx
│   ├── services/
│   │   ├── api.js
│   │   └── websocket.js
│   ├── App.jsx
│   └── index.jsx
├── package.json
└── vite.config.js
```

---

## ⚡ **IMPLEMENTAÇÃO (ORDEM)**

1. **Setup do projeto** (30 min)
   - Vite + React
   - Tailwind CSS
   - Recharts (charts)

2. **Componentes básicos** (1h)
   - Header, Sidebar, Layout
   - StatusCard, CostFooter

3. **Charts e dados** (1h)
   - BalanceChart (Recharts)
   - API integration

4. **Leaderboard + Tables** (1h)
   - Leaderboard component
   - SignalsTable

5. **WebSocket** (1h)
   - Conexão tempo real
   - Auto-update

6. **Deploy + Testes** (30 min)
   - Build
   - Test local

---

## 🎨 **DESIGN SYSTEM**

**Cores:**
- 🟢 Success: `#10B981` (emerald-500)
- 🟡 Warning: `#F59E0B` (amber-500)
- 🔴 Critical: `#EF4444` (red-500)
- 💀 Dead: `#6B7280` (gray-500)
- Primary: `#06B6D4` (cyan-500)

**Fontes:**
- Inter (principal)
- JetBrains Mono (números)

---

## 🚀 **COMEÇANDO AGORA!**

**Próximo:** Setup do projeto React + Vite
