# 🍃 LEVE IA - TESTE DE INTEGRAÇÃO NO SITE

**Para:** Equipe de Desenvolvimento app.leve.app.br  
**De:** Renato Abreu  
**Data:** 08/Mar/2026  
**Prioridade:** ALTA  
**Tempo estimado:** 30-60 minutos

---

## 🎯 OBJETIVO

Integrar os agentes de IA da Leve IA no site para:
- 🎧 **Suporte automático 24/7** (responde em < 30 segundos)
- 💼 **Captura de leads qualificada** (Sales Agent aborda visitantes)
- 📊 **Dashboard Alpha Signals** integrado

---

## 📦 O QUE IMPLEMENTAR (PASSO A PASSO)

### **1️⃣ WIDGET DE CHAT (Prioridade MÁXIMA)**

**Onde:** Em TODAS as páginas do `app.leve.app.br`

**Código para adicionar no `<head>`:**

```html
<!-- Leve IA Support Agent Widget -->
<script>
  (function() {
    window.LeveChatConfig = {
      // Configuração básica
      botName: 'Support Agent Leve IA',
      botAvatar: '🍃',
      welcomeMessage: 'Olá! Sou o Support Agent da Leve IA. 🍃\n\nComo posso te ajudar hoje?',
      
      // Cores (ajustar para identidade visual Leve IA)
      theme: {
        primaryColor: '#00D4AA',
        secondaryColor: '#ffffff',
        position: 'bottom-right' // ou 'bottom-left'
      },
      
      // Endpoints (configurar backend)
      endpoints: {
        sendMessage: '/api/chat/send',
        receiveMessage: '/api/chat/receive',
        getHistory: '/api/chat/history'
      },
      
      // Comportamento
      autoOpen: false, // não abrir sozinho
      responseTimeout: 30000, // 30 segundos
      offlineMessage: 'Estamos online 24/7! Respondo em instantes.'
    };
    
    // Carregar widget
    var script = document.createElement('script');
    script.src = 'https://api.leveia.com/widget/levechat.js';
    script.async = true;
    document.head.appendChild(script);
  })();
</script>
```

**O que isso faz:**
- ✅ Abre botão de chat no canto inferior direito
- ✅ Visitante clica → abre janela de chat
- ✅ Mensagem vai para Support Agent (via Telegram/Backend)
- ✅ Resposta chega em < 30 segundos

---

### **2️⃣ BACKEND API (Recebimento de Mensagens)**

**Onde:** No backend do app.leve.app.br (Node.js, Python, etc.)

**Endpoint 1: Enviar mensagem para Support Agent**

```javascript
// POST /api/chat/send
// Recebe mensagem do visitante

app.post('/api/chat/send', async (req, res) => {
  const { userId, message, sessionId } = req.body;
  
  // Opção A: Encaminhar para Telegram (Support Agent)
  await fetch('https://api.telegram.org/bot<BOT_TOKEN>/sendMessage', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      chat_id: '1176846104', // ID do Renato/Support Agent
      text: `🎧 NOVO CHAT - SITE\n\n👤 User: ${userId}\n💬 Mensagem: ${message}\n🔗 Session: ${sessionId}`
    })
  });
  
  // Opção B: Encaminhar para webhook OpenClaw (mais automático)
  await fetch('https://gateway.openclaw.ai/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      agent: 'support-agent',
      userId: userId,
      message: message,
      sessionId: sessionId
    })
  });
  
  res.json({ 
    status: 'received', 
    waitingForResponse: true,
    estimatedTime: '30 segundos'
  });
});
```

**Endpoint 2: Receber resposta do Support Agent**

```javascript
// Webhook que recebe resposta do Support Agent
// POST /api/chat/receive

app.post('/api/chat/receive', async (req, res) => {
  const { sessionId, message, agent } = req.body;
  
  // Enviar de volta para o visitante (WebSocket ou Server-Sent Events)
  io.to(sessionId).emit('chat-message', {
    from: 'support-agent',
    message: message,
    timestamp: new Date().toISOString()
  });
  
  res.json({ status: 'delivered' });
});
```

---

### **3️⃣ PIXEL DE CAPTURA DE LEADS**

**Onde:** Em TODAS as páginas (antes do `</body>`)

```html
<!-- Leve IA Lead Tracking Pixel -->
<script>
  (function() {
    // Gera ID único se não existir
    let userId = localStorage.getItem('leve_user_id');
    if (!userId) {
      userId = 'user_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
      localStorage.setItem('leve_user_id', userId);
    }
    
    // Rastreia pageview
    const pixel = document.createElement('img');
    pixel.src = 'https://api.leveia.com/track?' + 
      'event=pageview&' +
      'url=' + encodeURIComponent(window.location.href) + '&' +
      'referrer=' + encodeURIComponent(document.referrer) + '&' +
      'userId=' + userId + '&' +
      'timestamp=' + Date.now();
    pixel.style.display = 'none';
    document.body.appendChild(pixel);
    
    // Detecta intenção de saída (exit intent)
    document.addEventListener('mouseleave', (e) => {
      if (e.clientY <= 0) {
        // Usuário vai sair → dispara lead
        fetch('https://api.leveia.com/track', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            event: 'exit_intent',
            userId: userId,
            url: window.location.href,
            timestamp: Date.now()
          })
        });
      }
    });
  })();
</script>
```

**O que isso faz:**
- ✅ Gera ID único para cada visitante
- ✅ Rastreia páginas visitadas
- ✅ Detecta quando visitante vai sair (exit intent)
- ✅ Sales Agent recebe alerta e aborda no chat

---

### **4️⃣ FORMULÁRIO DE CAPTURA DE LEADS**

**Onde:** Página de pricing, dashboard, ou pop-up após 30 segundos

```html
<!-- Modal de Captura de Lead -->
<div id="lead-capture-modal" style="display:none; position:fixed; top:50%; left:50%; transform:translate(-50%,-50%); background:white; padding:30px; border-radius:12px; box-shadow:0 4px 20px rgba(0,0,0,0.2); z-index:9999;">
  <h3>🍃 Quer receber sinais de trading grátis?</h3>
  <p>O Alpha Signals da Leve IA manda sinais com prova de yield on-chain.</p>
  
  <form id="lead-form" onsubmit="submitLead(event)">
    <input type="text" id="lead-name" placeholder="Seu nome" required style="width:100%; padding:12px; margin:8px 0; border:1px solid #ddd; border-radius:6px;">
    <input type="email" id="lead-email" placeholder="Seu email" required style="width:100%; padding:12px; margin:8px 0; border:1px solid #ddd; border-radius:6px;">
    <input type="tel" id="lead-telegram" placeholder="Seu Telegram (opcional)" style="width:100%; padding:12px; margin:8px 0; border:1px solid #ddd; border-radius:6px;">
    
    <select id="lead-interest" style="width:100%; padding:12px; margin:8px 0; border:1px solid #ddd; border-radius:6px;">
      <option value="">Quero saber mais sobre...</option>
      <option value="alpha_signals">Alpha Signals (Sinais de Trading)</option>
      <option value="compra_leve">Comprar LEVE (Pré-venda)</option>
      <option value="parceria">Parceria</option>
      <option value="outro">Outro</option>
    </select>
    
    <button type="submit" style="width:100%; padding:14px; background:#00D4AA; color:white; border:none; border-radius:6px; font-size:16px; cursor:pointer; margin-top:12px;">
      🚀 Quero receber sinais grátis
    </button>
  </form>
  
  <button onclick="document.getElementById('lead-capture-modal').style.display='none'" style="position:absolute; top:10px; right:15px; background:none; border:none; font-size:24px; cursor:pointer;">&times;</button>
</div>

<script>
  // Mostra modal após 30 segundos
  setTimeout(() => {
    if (!localStorage.getItem('lead_captured')) {
      document.getElementById('lead-capture-modal').style.display = 'block';
    }
  }, 30000);
  
  function submitLead(event) {
    event.preventDefault();
    
    const lead = {
      name: document.getElementById('lead-name').value,
      email: document.getElementById('lead-email').value,
      telegram: document.getElementById('lead-telegram').value,
      interest: document.getElementById('lead-interest').value,
      url: window.location.href,
      userId: localStorage.getItem('leve_user_id'),
      timestamp: Date.now()
    };
    
    // Envia para backend
    fetch('/api/lead', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(lead)
    })
    .then(res => res.json())
    .then(data => {
      localStorage.setItem('lead_captured', 'true');
      document.getElementById('lead-capture-modal').style.display = 'none';
      alert('🍃 Obrigado! O Sales Agent vai te contactar em breve.');
    });
  }
</script>
```

---

### **5️⃣ ENDPOINT DE CAPTURA DE LEADS**

**Onde:** Backend do app.leve.app.br

```javascript
// POST /api/lead
// Recebe lead capturado

app.post('/api/lead', async (req, res) => {
  const lead = req.body;
  
  console.log('🔔 NOVO LEAD CAPTURADO:', lead);
  
  // 1. Salva no banco de dados
  await db.collection('leads').insertOne({
    ...lead,
    status: 'new',
    source: 'website',
    createdAt: new Date()
  });
  
  // 2. Envia para Sales Agent (Telegram)
  await fetch('https://api.telegram.org/bot<BOT_TOKEN>/sendMessage', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      chat_id: '1176846104',
      text: `💼 NOVO LEAD - SITE\n\n👤 Nome: ${lead.name}\n📧 Email: ${lead.email}\n✈️ Telegram: ${lead.telegram || 'N/A'}\n🎯 Interesse: ${lead.interest}\n🔗 Página: ${lead.url}\n\n🍃 Sales Agent deve abordar em < 1 hora!`
    })
  });
  
  // 3. Envia email de confirmação para lead
  await sendEmail({
    to: lead.email,
    subject: '🍃 Bem-vindo à Leve IA!',
    body: `Olá ${lead.name},\n\nObrigado pelo interesse na Leve IA!\n\nNosso Sales Agent vai te contactar em breve.\n\nEnquanto isso, conheça nosso dashboard: https://coinmarketleve.com\n\n🍃 Leve IA - Verifiable AI is the only AI`
  });
  
  res.json({ 
    status: 'captured', 
    leadId: Date.now(),
    message: 'Lead capturado com sucesso!'
  });
});
```

---

## ✅ CHECKLIST DE IMPLEMENTAÇÃO

### **Frontend (app.leve.app.br):**

- [ ] Adicionar código do Widget de Chat no `<head>` de todas as páginas
- [ ] Adicionar Pixel de Tracking antes do `</body>`
- [ ] Adicionar Modal de Captura de Leads (página de pricing ou após 30s)
- [ ] Testar widget abrindo/fechando
- [ ] Testar envio de mensagem no chat

### **Backend (API):**

- [ ] Criar endpoint `POST /api/chat/send`
- [ ] Criar endpoint `POST /api/chat/receive` (webhook)
- [ ] Criar endpoint `POST /api/lead`
- [ ] Configurar integração com Telegram (bot token)
- [ ] Configurar envio de email de confirmação
- [ ] Salvar leads no banco de dados

### **Testes:**

- [ ] Abrir site → Widget aparece no canto?
- [ ] Clicar no chat → Abre janela?
- [ ] Enviar mensagem → Chega no Telegram?
- [ ] Support Agent responde → Aparece no chat?
- [ ] Preencher form de lead → Salva no banco?
- [ ] Lead chega no Telegram do Sales Agent?

---

## 🧪 ROTEIRO DE TESTE (QA)

**Tempo estimado:** 15 minutos

### **Teste 1: Chat de Suporte**

1. Abrir `app.leve.app.br`
2. Aguardar widget carregar (canto inferior direito)
3. Clicar no botão do chat
4. Digitar: "Olá, como funciona o Alpha Signals?"
5. **Esperar até 30 segundos**
6. **Verificar:** Resposta chegou? Foi útil?

**Critério de sucesso:** Resposta em < 30s, tom humano, resolve dúvida.

---

### **Teste 2: Captura de Lead**

1. Abrir `app.leve.app.br/pricing` (ou qualquer página)
2. Aguardar 30 segundos (modal deve aparecer)
3. Preencher formulário com dados de teste
4. Clicar em "Quero receber sinais grátis"
5. **Verificar:** 
   - Modal fechou?
   - Mensagem de sucesso apareceu?
   - Lead chegou no Telegram?
   - Email de confirmação chegou?

**Critério de sucesso:** Lead salvo, notificação enviada, email recebido.

---

### **Teste 3: Exit Intent**

1. Abrir `app.leve.app.br`
2. Mover mouse rapidamente para fora da página (cima)
3. **Verificar:** Modal de captura apareceu?

**Critério de sucesso:** Modal dispara antes do usuário sair.

---

## 📊 MÉTRICAS PARA ACOMPANHAR

**Dashboard de acompanhamento (sugerido):**

| Métrica | Meta | Atual |
|---------|------|-------|
| Chats iniciados/dia | 50+ | - |
| Respostas em < 30s | 95%+ | - |
| Leads capturados/dia | 10+ | - |
| Conversão lead → cliente | 20%+ | - |
| Satisfação (CSAT) | 4.5/5 | - |

---

## 🚀 DEPOIS DE IMPLEMENTADO

**O que acontece automaticamente:**

1. ✅ Visitante abre site → Widget carregado
2. ✅ Visitante manda mensagem → Support Agent responde em < 30s
3. ✅ Visitante preenche form → Sales Agent aborda em < 1h
4. ✅ Visitante sai → Pixel rastreia, Sales Agent re-engaja
5. ✅ Tudo registrado no Telegram + Banco de dados

---

## 🛠️ SUPORTE TÉCNICO

**Dúvidas durante implementação:**

- **Documentação completa:** `/root/openclaw/docs/INTEGRACAO_SITES.md`
- **Códigos de exemplo:** Neste documento
- **Suporte:** Support Agent da Leve IA (via Telegram)

**Arquivos disponíveis no servidor:**

```
/root/openclaw/docs/INTEGRACAO_SITES.md
/root/openclaw/docs/TESTE_INTEGRACAO_SITE.md (este arquivo)
/root/openclaw/n8n_workflow_leveis_arrecadacao.json
```

---

## 📅 PRAZO SUGERIDO

| Etapa | Prazo | Responsável |
|-------|-------|-------------|
| Implementação frontend | 1 dia | Dev Frontend |
| Implementação backend | 1 dia | Dev Backend |
| Testes internos | 4 horas | QA |
| Ajustes finais | 4 horas | Dev + QA |
| **Total** | **2-3 dias** | - |

---

## 🎯 ENTREGÁVEL ESPERADO

**Ao final, teremos:**

- ✅ Widget de chat funcionando em produção
- ✅ Support Agent respondendo em < 30s
- ✅ Leads capturados e notificados
- ✅ Sales Agent abordando leads em < 1h
- ✅ Métricas de acompanhamento

---

**🍃 Leve IA - Verifiable AI is the only AI**

**Criado por:** Cabral (CEO Agent)  
**Data:** 08/Mar/2026 13:45 UTC  
**Versão:** 1.0.0

---

## 📩 MENSAGEM PRONTA PARA ENVIAR PARA EQUIPE

**Copie e cole no Slack/Telegram da equipe:**

```
🚀 **NOVA FEATURE: IA DE ATENDIMENTO NO SITE**

Time, preciso implementar integração dos agentes de IA no app.leve.app.br.

**O que precisamos:**
1. Widget de chat (suporte 24/7)
2. Captura de leads (form + pixel)
3. Backend API (receber/enviar mensagens)

**Documentação completa:** [anexar este arquivo]

**Prazo:** 2-3 dias

**Impacto:**
- Suporte automático 24/7 (responde em 30s)
- Captura de leads qualificada
- Sales Agent aborda leads automaticamente

**Quem pode pegar?** Preciso de 1 frontend + 1 backend.

Dúvidas? Me chamem! 🍃
```
