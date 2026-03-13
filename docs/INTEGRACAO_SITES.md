# 🍃 LEVE IA - INTEGRAÇÃO NOS SITES

**Guia prático: O que colocar em levecoin.io e levenopix.com.br**

---

## 🎯 OBJETIVO

Ter os agentes da Leve IA **rodando diretamente nos sites**:
- 🎧 **Support Agent** → Chat de suporte 24/7
- 💼 **Sales Agent** → Captura de leads qualificada
- 🤖 **Cabral** → Decisões estratégicas (backend)

---

## 📦 O QUE INSTALAR

### **1. WIDGET DE CHAT (Suporte + Vendas)**

**Código para colocar no `<head>` de TODAS as páginas:**

```html
<!-- Leve IA Chat Widget -->
<script>
  (function() {
    window.LeveChatConfig = {
      apiEndpoint: 'https://api.leveia.com/chat',
      telegramBot: '@Agent_180181Renato_bot',
      welcomeMessage: 'Olá! Sou o Support Agent da Leve IA. 🍃\nComo posso te ajudar hoje?',
      theme: {
        primaryColor: '#00D4AA',
        position: 'bottom-right'
      }
    };
    
    var script = document.createElement('script');
    script.src = 'https://api.leveia.com/widget/levechat.js';
    script.async = true;
    document.head.appendChild(script);
  })();
</script>
```

**O que faz:**
- ✅ Abre chat no canto inferior direito
- ✅ Conecta com Support Agent (responde em < 30s)
- ✅ Captura leads pro Sales Agent
- ✅ Redireciona pro Telegram se necessário

---

### **2. API ENDPOINTS (Backend)**

**No seu servidor (n8n ou Node.js), crie:**

#### **POST /api/chat**
```javascript
// Recebe mensagem do usuário
// Encaminha para Support Agent via Telegram API
// Retorna resposta em < 30 segundos

{
  "userId": "12345",
  "message": "Como compro LEVE?",
  "sessionId": "abc-123"
}
```

#### **POST /api/lead**
```javascript
// Captura lead qualificado
// Envia para Sales Agent
// Salva no CRM

{
  "name": "João Silva",
  "email": "joao@email.com",
  "telegram": "@joao",
  "interest": "compra_usdt",
  "budget": "1000-5000"
}
```

---

### **3. PIXEL DE RASTREAMENTO**

**Para o Sales Agent prospectar:**

```html
<!-- Leve IA Tracking Pixel -->
<script>
  (function() {
    var pixel = document.createElement('img');
    pixel.src = 'https://api.leveia.com/track?' + 
      'event=pageview&' +
      'url=' + encodeURIComponent(window.location.href) + '&' +
      'referrer=' + encodeURIComponent(document.referrer) + '&' +
      'userId=' + (localStorage.getItem('leve_user_id') || '');
    pixel.style.display = 'none';
    document.body.appendChild(pixel);
  })();
</script>
```

**O que faz:**
- ✅ Rastreia comportamento no site
- ✅ Identifica leads quentes (visitaram pricing, voltaram 3x)
- ✅ Sales Agent aborda no momento certo

---

## 🚀 IMPLEMENTAÇÃO RÁPIDA

### **OPÇÃO 1: n8n (Mais fácil)**

**Workflow pronto:**

1. **Webhook** (`/api/chat`) → Recebe mensagem
2. **Telegram Bot** → Envia para @Agent_180181Renato_bot
3. **Delay** → Aguarda resposta do Support Agent
4. **Webhook Response** → Retorna pra página

**Importe este workflow:**
```
/root/openclaw/n8n_workflow_leveis_arrecadacao.json
```

---

### **OPÇÃO 2: Node.js (Mais controle)**

**Instale:**
```bash
npm install express axios body-parser cors
```

**Crie `server.js`:**
```javascript
const express = require('express');
const axios = require('axios');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

// Chat endpoint
app.post('/api/chat', async (req, res) => {
  const { userId, message, sessionId } = req.body;
  
  // Envia para Telegram (Support Agent)
  const telegramResponse = await axios.post(
    'https://api.telegram.org/bot<BOT_TOKEN>/sendMessage',
    {
      chat_id: '1176846104',
      text: `🎧 NOVO CHAT\nUser: ${userId}\nMensagem: ${message}`
    }
  );
  
  // Aguarda resposta (webhook do Telegram)
  // ...implementar webhook receiver...
  
  res.json({ status: 'received', waitingForResponse: true });
});

// Lead capture
app.post('/api/lead', async (req, res) => {
  const lead = req.body;
  
  // Salva no CRM
  // Envia para Sales Agent
  
  console.log('🔔 NOVO LEAD:', lead);
  
  res.json({ status: 'captured', leadId: Date.now() });
});

app.listen(3000, () => {
  console.log('🍃 Leve IA API rodando na porta 3000');
});
```

---

## 📊 DASHBOARD INTEGRADO

**No coinmarketleve.com:**

### **Widget de Sinais Alpha**

```html
<!-- Alpha Signals Widget -->
<div id="alpha-signals">
  <h3>📊 Alpha Signals - Últimos Sinais</h3>
  <div id="signals-container">
    <!-- Carregado via API -->
  </div>
</div>

<script>
  async function loadSignals() {
    const response = await fetch('https://api.leveia.com/alpha/signals');
    const signals = await response.json();
    
    const container = document.getElementById('signals-container');
    container.innerHTML = signals.map(signal => `
      <div class="signal-card ${signal.type}">
        <span class="pair">${signal.pair}</span>
        <span class="type">${signal.type}</span>
        <span class="entry">Entrada: ${signal.entry}</span>
        <span class="target">Alvo: ${signal.target}</span>
        <span class="stop">Stop: ${signal.stop}</span>
        <span class="pnl ${signal.pnl >= 0 ? 'positive' : 'negative'}">
          PnL: ${signal.pnl >= 0 ? '+' : ''}${signal.pnl}%
        </span>
      </div>
    `).join('');
  }
  
  loadSignals();
  setInterval(loadSignals, 60000); // Atualiza a cada 1min
</script>
```

---

## 🔗 LINKS DE CONVERSÃO

**Em TODAS as páginas:**

```html
<!-- Botões de Compra -->
<a href="https://levecoin.io" class="btn-buy-usdt">
  🌎 Comprar com USDT
</a>

<a href="https://levenopix.com.br" class="btn-buy-pix">
  🇧🇷 Comprar com PIX
</a>

<a href="https://coinmarketleve.com" class="btn-dashboard">
  📊 Ver Dashboard
</a>
```

---

## 🎯 FUNNEL COMPLETO

```
1. Visitante chega no site
   ↓
2. Pixel rastreia comportamento
   ↓
3. Se visitar pricing 2x → Sales Agent aborda
   ↓
4. Se abrir chat → Support Agent responde
   ↓
5. Se clicar compra → Redireciona levecoin.io/levenopix
   ↓
6. Após compra → Support Agent faz follow-up
   ↓
7. Cliente vira fã → Indica outros
```

---

## ✅ CHECKLIST DE IMPLANTAÇÃO

### **levecoin.io:**
- [ ] Widget de chat no `<head>`
- [ ] Pixel de rastreamento
- [ ] Botões de compra (USDT)
- [ ] Link pro dashboard
- [ ] API endpoint `/api/chat`
- [ ] API endpoint `/api/lead`

### **levenopix.com.br:**
- [ ] Widget de chat no `<head>`
- [ ] Pixel de rastreamento
- [ ] Botões de compra (PIX)
- [ ] Link pro dashboard
- [ ] API endpoint `/api/chat`
- [ ] API endpoint `/api/lead`

### **coinmarketleve.com:**
- [ ] Widget de sinais Alpha
- [ ] Atualização em tempo real (60s)
- [ ] Link de compra
- [ ] Chat de suporte

---

## 🛠️ PRECISA DE AJUDA?

**Arquivos prontos no servidor:**

| Arquivo | O que é | Onde usar |
|---------|---------|-----------|
| `/root/openclaw/n8n_workflow_leveis_arrecadacao.json` | Workflow n8n | Importar no n8n |
| `/root/openclaw/leveia-dashboard/` | Dashboard pronto | Referência |
| `/root/openclaw/coinmarketleve/` | Site pronto | Referência |

---

## 🚀 PRÓXIMOS PASSOS

1. **Hoje:** Instalar widget de chat nos 2 sites
2. **Amanhã:** Configurar API endpoints (n8n ou Node)
3. **48h:** Testar fluxo completo (chat → compra → follow-up)
4. **1 semana:** Otimizar conversão com dados do Sales Agent

---

**🍃 Leve IA - Verifiable AI is the only AI**

**Criado por:** Cabral (CEO Agent)  
**Data:** 08/Mar/2026 11:55 UTC  
**Versão:** 1.0.0
