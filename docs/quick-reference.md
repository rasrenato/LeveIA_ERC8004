# 🍃 LEVE IA - QUICK REFERENCE CARD

**Tudo que você precisa em 1 página**

---

## 🔗 **LINKS OFICIAIS**

| Site | URL |
|------|-----|
| **Dashboard Yield** | https://coinmarketleve.com |
| **Comprar (USDT)** | https://levecoin.io |
| **Comprar (PIX)** | https://levenopix.com.br |
| **Roadmap** | https://roadmapdaleve.com.br |
| **Telegram** | https://t.me/comunidadeleve |
| **Twitter** | https://twitter.com/leve_IA |
| **GitHub** | https://github.com/rasrenato/LeveIA_ERC8004 |

---

## 📊 **MÉTRICAS ATUAIS**

| Métrica | Valor |
|---------|-------|
| **Total Sinais** | 3 |
| **Win Rate** | 0.00% (mock) |
| **Yield Médio** | -36.10% (mock) |
| **Sinais Ativos** | 0 |

⚠️ **Nota:** Dados são MOCK. Alpha Engine será implementado em breve!

---

## 🛠️ **COMANDOS ÚTEIS**

### **Ver status dos serviços:**
```bash
pm2 list
```

### **Reiniciar backend:**
```bash
pm2 restart leveclaw-backend
```

### **Reiniciar frontend:**
```bash
pm2 restart leveclaw-frontend
```

### **Ver logs:**
```bash
pm2 logs leveclaw-backend --lines 50
```

### **Rodar yield calculator:**
```bash
cd /root/openclaw
source venv_chainlink/bin/activate
python3 alpha_signals/yield_calculator.py --calculate
```

### **Rodar testes:**
```bash
cd /root/openclaw
source venv_chainlink/bin/activate
bash scripts/run_tests.sh
```

---

## 📁 **ARQUIVOS IMPORTANTES**

| Arquivo | O que é | Onde |
|---------|---------|------|
| `ProofOfYield.sol` | Smart Contract | `/root/openclaw/contracts/` |
| `yield_calculator.py` | Calcula yield | `/root/openclaw/alpha_signals/` |
| `page.tsx` | Frontend sinais | `/opt/leveclaw/frontend/src/app/` |
| `badge.html` | Badge embed | `/root/openclaw/coinmarketleve/` |
| `announcement-telegram.md` | Post pronto | `/root/openclaw/docs/` |

---

## 📱 **REDES SOCIAIS**

### **Telegram:**
- **Comunidade:** t.me/comunidadeleve
- **Post frequency:** 1-2x/dia
- **Conteúdo:** Updates, sinais, provas

### **Twitter:**
- **Handle:** @leve_IA
- **Post frequency:** 3-5x/dia
- **Conteúdo:** Sinais, yield, threads

### **MoltBook:**
- **Agente:** Leve_AI
- **Post frequency:** Auto (30min)
- **Conteúdo:** Sinais, Web3, IA

---

## 🎯 **PRÓXIMOS PASSOS**

| Data | Tarefa | Responsável |
|------|--------|-------------|
| **08/Mar** | Alpha Engine automático | Cabral |
| **08/Mar** | Checkout/Pagamento | Cabral |
| **09/Mar** | Post Telegram/Twitter | Renato |
| **09/Mar** | Badge nos sites | Renato |

---

## 🆘 **SUPORTE**

| Problema | Solução |
|----------|---------|
| Backend caiu | `pm2 restart leveclaw-backend` |
| Frontend caiu | `pm2 restart leveclaw-frontend` |
| Sinais não atualizam | Rodar yield calculator |
| Badge não carrega | Verificar API `/api/yield-dashboard/stats` |
| Chainlink falhou | Verificar `https://mainnet.base.org` |

---

## 📞 **CONTATOS**

- **Renato (Owner):** @rasrenato
- **Cabral (CEO Agent):** Telegram
- **Suporte:** suporte@levecoin.io

---

**🍃 Leve IA - Verifiable AI is the only AI**

**Última atualização:** 08/Mar/2026 01:50 UTC
