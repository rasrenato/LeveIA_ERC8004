# 🍃 PROMPT PARA LOVABLE.DEV - LEVECOIN.IO

**Copie e cole este prompt no lovable.dev para implementar a integração da Leve IA no levecoin.io**

---

## 📋 PROMPT COMPLETO (copiar tudo)

```
Crie uma integração completa de IA de atendimento para o site levecoin.io (plataforma de venda de criptomoeda Leve IA - BEP-20 na Binance Smart Chain).

## 🎯 OBJETIVO

Implementar 3 features principais:
1. Widget de chat com Support Agent (resposta em < 30 segundos)
2. Captura de leads com Sales Agent (follow-up automático)
3. Dashboard Alpha Signals integrado (sinais de trading em tempo real)

## 🎨 IDENTIDADE VISUAL

- **Cores principais:** Verde água (#00D4AA), Branco (#FFFFFF), Preto (#1A1A1A)
- **Logo:** 🍃 (emoji de folha)
- **Tom:** Moderno, limpo, confiável, tecnológico
- **Referência:** Estilo Stripe + Coinbase

## 📦 FEATURE 1: WIDGET DE CHAT (Prioridade MÁXIMA)

### Componente: ChatFlotingButton

**Localização:** Canto inferior direito (fixed, bottom: 24px, right: 24px)

**Requisitos:**
- Botão redondo (60x60px) com emoji 🍃
- Badge de "Online 24/7" quando visível
- Animação de pulse a cada 5 segundos
- Ao clicar: abre modal de chat (400px width, 600px height)

### Componente: ChatModal

**Estrutura:**
```
┌─────────────────────────────────┐
│ 🍃 Support Agent Leve IA    ✕  │ ← Header
├─────────────────────────────────┤
│                                 │
│ [Bot]: Olá! Sou o Support       │
│ Agent da Leve IA. 🍃           │
│ Como posso te ajudar?          │
│                                 │
│              [User]: Como compro?│
│                                 │
│ [Bot]: É simples! Clique em...  │
│                                 │
├─────────────────────────────────┤
│ Digite sua mensagem...    [➤]  │ ← Input
└─────────────────────────────────┘
```

**Comportamento:**
- Mensagens do bot alinhadas à esquerda (bg: #f0f0f0)
- Mensagens do usuário alinhadas à direita (bg: #00D4AA, texto: branco)
- Scroll automático para última mensagem
- Indicador de "digitando..." quando aguardando resposta
- Timeout de 30 segundos para resposta (mostrar "Ainda estou aqui?")

**API Integration:**
```javascript
// Enviar mensagem
POST /api/chat/send
Body: { userId, message, sessionId }
Response: { status: 'received', waitingForResponse: true }

// Receber resposta (webhook ou polling)
POST /api/chat/receive
Body: { sessionId, message, from: 'support-agent' }
```

**Mensagens padrão do bot:**
- Welcome: "Olá! Sou o Support Agent da Leve IA. 🍃\n\nComo posso te ajudar hoje?"
- Waiting: "Estou verificando sua dúvida, um momento..."
- Timeout: "Ainda estou por aqui! Me chame se precisar. 🍃"
- Offline: "Estamos online 24/7! Respondo em instantes."

---

## 📦 FEATURE 2: CAPTURA DE LEADS

### Componente: LeadCaptureModal

**Trigger:** 
- Após 30 segundos na página, OU
- Exit intent (mouse sai da janela), OU
- Clique em "Quero receber sinais"

**Estrutura:**
```html
<div class="modal-overlay">
  <div class="modal-content">
    <h3>🍃 Quer receber sinais de trading grátis?</h3>
    <p>O Alpha Signals da Leve IA manda sinais com prova de yield on-chain.</p>
    
    <form>
      <input type="text" placeholder="Seu nome" required />
      <input type="email" placeholder="Seu email" required />
      <input type="tel" placeholder="Seu Telegram (opcional)" />
      
      <select>
        <option value="">Quero saber mais sobre...</option>
        <option value="alpha_signals">Alpha Signals (Sinais de Trading)</option>
        <option value="compra_leve">Comprar LEVE (Pré-venda)</option>
        <option value="parceria">Parceria</option>
      </select>
      
      <button type="submit">
        🚀 Quero receber sinais grátis
      </button>
    </form>
  </div>
</div>
```

**Estilos:**
- Overlay: fundo preto 50% opacity
- Modal: branco, border-radius 12px, box-shadow
- Botão: verde #00D4AA, hover: #00b894
- Input: border 1px #ddd, focus: border #00D4AA

**API Integration:**
```javascript
POST /api/lead
Body: { name, email, telegram, interest, url, userId, timestamp }
Response: { status: 'captured', leadId }
```

**Pós-submissão:**
- Salvar lead no localStorage (evitar duplicate)
- Mostrar toast de sucesso: "🍃 Obrigado! O Sales Agent vai te contactar em breve."
- Fechar modal
- Disparar evento para backend (Sales Agent aborda em < 1h)

---

## 📦 FEATURE 3: DASHBOARD ALPHA SIGNALS

### Componente: AlphaSignalsWidget

**Localização:** Página /dashboard ou home (após login)

**Estrutura:**
```html
<div class="alpha-signals-widget">
  <div class="widget-header">
    <h3>📊 Alpha Signals - Últimos Sinais</h3>
    <span class="live-indicator">🔴 AO VIVO</span>
  </div>
  
  <div class="signals-grid">
    <!-- Cards de sinais -->
    <div class="signal-card long">
      <div class="signal-header">
        <span class="pair">BTC/USDT</span>
        <span class="type LONG">LONG</span>
      </div>
      <div class="signal-body">
        <div class="metric">
          <span class="label">Entrada</span>
          <span class="value">$78,450</span>
        </div>
        <div class="metric">
          <span class="label">Alvo</span>
          <span class="value">$82,000</span>
        </div>
        <div class="metric">
          <span class="label">Stop</span>
          <span class="value">$76,200</span>
        </div>
        <div class="metric">
          <span class="label">R/R</span>
          <span class="value">1:2.5</span>
        </div>
      </div>
      <div class="signal-footer">
        <span class="pnl positive">+12.5%</span>
        <span class="time">há 2 horas</span>
      </div>
    </div>
  </div>
  
  <div class="widget-footer">
    <button>Ver todos os sinais →</button>
  </div>
</div>
```

**API Integration:**
```javascript
GET /api/alpha/signals
Response: [
  {
    id: "signal_123",
    pair: "BTC/USDT",
    type: "LONG",
    entry: 78450,
    target: 82000,
    stop: 76200,
    pnl: 12.5,
    status: "active",
    createdAt: "2026-03-08T10:00:00Z"
  }
]

// Polling: atualizar a cada 60 segundos
setInterval(loadSignals, 60000);
```

**Estilos:**
- Card LONG: border-left 4px verde (#00D4AA)
- Card SHORT: border-left 4px vermelho (#FF4444)
- PnL positivo: verde, negativo: vermelho
- Live indicator: pulse animation

---

## 🔧 COMPONENTES TÉCNICOS

### 1. UserTrackingService

**Função:** Gerar ID único e rastrear comportamento

```javascript
class UserTrackingService {
  constructor() {
    this.userId = this.getOrCreateUserId();
    this.sessionId = this.generateSessionId();
  }
  
  getOrCreateUserId() {
    let userId = localStorage.getItem('leve_user_id');
    if (!userId) {
      userId = 'user_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
      localStorage.setItem('leve_user_id', userId);
    }
    return userId;
  }
  
  trackPageview(url) {
    fetch('/api/track', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        event: 'pageview',
        userId: this.userId,
        sessionId: this.sessionId,
        url: url,
        timestamp: Date.now()
      })
    });
  }
  
  trackExitIntent() {
    fetch('/api/track', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        event: 'exit_intent',
        userId: this.userId,
        url: window.location.href,
        timestamp: Date.now()
      })
    });
  }
}

// Usage
const tracker = new UserTrackingService();
tracker.trackPageview(window.location.href);

// Exit intent
document.addEventListener('mouseleave', (e) => {
  if (e.clientY <= 0) {
    tracker.trackExitIntent();
  }
});
```

### 2. ChatService

```javascript
class ChatService {
  constructor() {
    this.sessionId = null;
    this.socket = null;
  }
  
  async sendMessage(message) {
    const response = await fetch('/api/chat/send', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        userId: localStorage.getItem('leve_user_id'),
        message: message,
        sessionId: this.sessionId || Date.now().toString()
      })
    });
    
    return await response.json();
  }
  
  connectWebSocket(sessionId) {
    this.socket = new WebSocket(`wss://api.leveia.com/chat/${sessionId}`);
    
    this.socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      this.onMessageReceived(data);
    };
  }
}
```

### 3. LeadCaptureService

```javascript
class LeadCaptureService {
  async submitLead(leadData) {
    const response = await fetch('/api/lead', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        ...leadData,
        userId: localStorage.getItem('leve_user_id'),
        url: window.location.href,
        timestamp: Date.now()
      })
    });
    
    const result = await response.json();
    
    if (result.status === 'captured') {
      localStorage.setItem('lead_captured', 'true');
    }
    
    return result;
  }
  
  shouldShowModal() {
    const captured = localStorage.getItem('lead_captured');
    return !captured;
  }
}
```

---

## 🎨 ESTILOS GERAIS

### CSS Variables

```css
:root {
  --primary-color: #00D4AA;
  --primary-hover: #00b894;
  --secondary-color: #ffffff;
  --text-color: #1A1A1A;
  --text-light: #666666;
  --bg-color: #f8f9fa;
  --border-color: #e0e0e0;
  --success-color: #00D4AA;
  --error-color: #FF4444;
  --warning-color: #FFA500;
  
  --shadow-sm: 0 1px 3px rgba(0,0,0,0.1);
  --shadow-md: 0 4px 6px rgba(0,0,0,0.1);
  --shadow-lg: 0 10px 20px rgba(0,0,0,0.15);
  
  --radius-sm: 6px;
  --radius-md: 12px;
  --radius-lg: 20px;
}
```

### Animações

```css
@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

@keyframes slideUp {
  from { transform: translateY(100%); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.chat-button {
  animation: pulse 2s infinite;
}

.modal-overlay {
  animation: fadeIn 0.2s ease-out;
}

.modal-content {
  animation: slideUp 0.3s ease-out;
}
```

---

## 📱 RESPONSIVIDADE

### Mobile (< 768px)
- Chat modal: full width, full height
- Lead modal: 90% width, margin 5% top
- Alpha Signals: 1 coluna (stack vertical)

### Tablet (768px - 1024px)
- Chat modal: 90% width, 80% height
- Lead modal: 80% width
- Alpha Signals: 2 colunas

### Desktop (> 1024px)
- Chat modal: 400px width, 600px height
- Lead modal: 500px width
- Alpha Signals: 3-4 colunas

---

## 🔌 API ENDPOINTS (Backend necessário)

### POST /api/chat/send
```json
Request: {
  "userId": "user_123",
  "message": "Como compro LEVE?",
  "sessionId": "abc-456"
}

Response: {
  "status": "received",
  "waitingForResponse": true,
  "estimatedTime": "30 segundos"
}
```

### POST /api/chat/receive
```json
Request: {
  "sessionId": "abc-456",
  "message": "É simples! Clique em...",
  "from": "support-agent"
}

Response: {
  "status": "delivered"
}
```

### POST /api/lead
```json
Request: {
  "name": "João Silva",
  "email": "joao@email.com",
  "telegram": "@joao",
  "interest": "alpha_signals",
  "url": "https://levecoin.io",
  "userId": "user_123",
  "timestamp": 1772979474057
}

Response: {
  "status": "captured",
  "leadId": "lead_789",
  "message": "Lead capturado com sucesso!"
}
```

### GET /api/alpha/signals
```json
Response: [
  {
    "id": "signal_123",
    "pair": "BTC/USDT",
    "type": "LONG",
    "entry": 78450,
    "target": 82000,
    "stop": 76200,
    "pnl": 12.5,
    "status": "active",
    "createdAt": "2026-03-08T10:00:00Z"
  }
]
```

---

## ✅ CHECKLIST DE ENTREGA

### Frontend
- [ ] ChatFloatingButton component
- [ ] ChatModal component
- [ ] LeadCaptureModal component
- [ ] AlphaSignalsWidget component
- [ ] UserTrackingService
- [ ] ChatService
- [ ] LeadCaptureService
- [ ] CSS variables e estilos
- [ ] Animações (pulse, slideUp, fadeIn)
- [ ] Responsividade (mobile, tablet, desktop)

### Backend
- [ ] POST /api/chat/send
- [ ] POST /api/chat/receive (webhook)
- [ ] POST /api/lead
- [ ] GET /api/alpha/signals
- [ ] POST /api/track
- [ ] Integração com Telegram (Support Agent)
- [ ] Integração com Telegram (Sales Agent)
- [ ] Banco de dados (leads, mensagens)

### Testes
- [ ] Chat abre/fecha
- [ ] Mensagem enviada → resposta em < 30s
- [ ] Lead capturado → email de confirmação
- [ ] Exit intent → modal aparece
- [ ] Alpha Signals → atualiza a cada 60s
- [ ] Responsividade (mobile, tablet, desktop)

---

## 🎯 CRITÉRIOS DE SUCESSO

1. **Chat:**
   - Abre em < 1 segundo
   - Resposta em < 30 segundos
   - UX fluida (sem travamentos)

2. **Lead Capture:**
   - Modal aparece após 30s ou exit intent
   - Form valida campos corretamente
   - Lead salvo no banco + notificação Telegram

3. **Alpha Signals:**
   - Atualiza automaticamente a cada 60s
   - Mostra PnL em tempo real
   - Design limpo e legível

---

## 📚 REFERÊNCIAS

- **Design:** Stripe.com, Coinbase.com
- **Chat:** Intercom, Drift
- **Lead Capture:** HubSpot, ConvertKit
- **Dashboard:** TradingView, CoinMarketCap

---

**🍃 Leve IA - Verifiable AI is the only AI**

**Contrato:** 0x67e463AcC3B35406B0f35C8Ed531da89f9670861 (BEP-20)
**Dashboard:** https://coinmarketleve.com
**Roadmap:** https://roadmapdaleve.com.br
```

---

## 📩 COMO USAR NO LOVABLE.DEV

1. **Acesse:** https://lovable.dev
2. **Crie novo projeto:** "levecoin.io Integration"
3. **Cole o prompt** acima completo
4. **Ajuste:** URLs e endpoints conforme seu backend
5. **Revise:** O lovable vai gerar o código
6. **Teste:** Siga o checklist de testes
7. **Deploy:** Suba para produção

---

## 🛠️ SUPORTE

**Dúvidas durante implementação:**

- **Documentação completa:** `/root/openclaw/docs/INTEGRACAO_SITES.md`
- **Guia de testes:** `/root/openclaw/docs/TESTE_INTEGRACAO_SITE.md`
- **Suporte:** Support Agent da Leve IA (via Telegram)

---

**🍃 Leve IA - Verifiable AI is the only AI**

**Criado por:** Cabral (CEO Agent)  
**Data:** 08/Mar/2026 14:20 UTC  
**Versão:** 1.0.0
