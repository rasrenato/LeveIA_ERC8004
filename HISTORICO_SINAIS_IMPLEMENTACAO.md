# 📊 HISTÓRICO DE SINAIS - IMPLEMENTAÇÃO COMPLETA

**Data:** 07 Mar 2026 00:10 UTC  
**Status:** ✅ **FASE 1 CONCLUÍDA (BANCO + API)**  
**Próxima Fase:** Dashboard Frontend (Fase 2)

---

## 🏗️ ARQUITETURA

```
┌─────────────────────────────────────────────────────────┐
│                    USUÁRIO                              │
│  (Dashboard /dashboard/my-signals)                     │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼ HTTP Requests
┌─────────────────────────────────────────────────────────┐
│                    API BACKEND                          │
│  /api/alpha-signals/history (GET)                      │
│  /api/alpha-signals/save (POST)                        │
│  /api/alpha-signals/stats (GET)                        │
│  /api/alpha-signals/:id/status (PUT)                   │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼ PostgreSQL Queries
┌─────────────────────────────────────────────────────────┐
│                 BANCO DE DADOS                          │
│  Tabela: alpha_signals                                  │
│  - user_id, symbol, direction, entry, targets...       │
│  - status, pnl, created_at, updated_at                 │
└─────────────────────────────────────────────────────────┘
```

---

## 📁 ARQUIVOS CRIADOS

| Arquivo | Função | Status |
|---------|--------|--------|
| `/opt/leveclaw/backend/routes/alpha-signals.js` | API routes | ✅ Criado |
| `/opt/leveclaw/backend/server.js` | Registro da rota | ✅ Atualizado |
| PostgreSQL `alpha_signals` | Tabela de sinais | ✅ Criada |

---

## 🗄️ ESTRUTURA DO BANCO

```sql
CREATE TABLE alpha_signals (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL,              -- ID do usuário
  symbol VARCHAR(20) NOT NULL,        -- Par (BTC/USDT)
  direction VARCHAR(10) NOT NULL,     -- LONG ou SHORT
  timeframe VARCHAR(50),              -- Swing Trade, Day Trade
  entry_min DECIMAL,                  -- Faixa de entrada (min)
  entry_max DECIMAL,                  -- Faixa de entrada (max)
  targets JSONB,                      -- Alvos múltiplos [{tp: 95000, percentage: 50}]
  stop_loss DECIMAL,                  -- Stop-loss
  risk_reward VARCHAR(20),            -- Risco/Retorno (1:2.5)
  confidence INTEGER,                 -- Confiança (0-100)
  validity VARCHAR(20),               -- Validade (7 dias)
  analysis TEXT,                      -- Análise técnica
  status VARCHAR(20) DEFAULT 'active',-- active, completed, cancelled
  pnl DECIMAL DEFAULT 0,              -- Lucro/Prejuízo (USDC)
  created_at TIMESTAMP DEFAULT NOW(), -- Data de criação
  updated_at TIMESTAMP DEFAULT NOW()  -- Última atualização
);

-- Índices para performance
CREATE INDEX idx_signals_user ON alpha_signals(user_id);
CREATE INDEX idx_signals_created ON alpha_signals(created_at);
CREATE INDEX idx_signals_status ON alpha_signals(status);
```

---

## 🔧 ENDPOINTS DA API

### **1. POST /api/alpha-signals/save**

Salva sinal desbloqueado pelo usuário.

**Payload:**
```json
{
  "symbol": "BTC/USDT",
  "direction": "LONG",
  "timeframe": "Swing Trade (5-15 dias)",
  "entry": { "min": 88000, "max": 90000 },
  "targets": [
    { "tp": 95000, "percentage": 50 },
    { "tp": 100000, "percentage": 50 }
  ],
  "stopLoss": 85000,
  "riskReward": "1:2.5",
  "confidence": 85,
  "validity": "7 dias",
  "analysis": "BTC rompendo resistência..."
}
```

**Resposta:**
```json
{
  "success": true,
  "message": "Sinal salvo com sucesso",
  "data": {
    "id": "uuid-do-sinal",
    "user_id": "uuid-usuario",
    "symbol": "BTC/USDT",
    ...
  }
}
```

---

### **2. GET /api/alpha-signals/history**

Lista histórico de sinais do usuário.

**Query Params:**
- `period` (opcional): Dias (default: 30)
- `status` (opcional): active, completed, cancelled
- `symbol` (opcional): BTC/USDT, ETH/USDT
- `direction` (opcional): LONG, SHORT

**Resposta:**
```json
{
  "success": true,
  "count": 12,
  "signals": [
    {
      "id": "uuid",
      "symbol": "BTC/USDT",
      "direction": "LONG",
      "entry_min": 88000,
      "status": "active",
      "pnl": 0,
      "created_at": "2026-03-06T22:00:00Z"
    },
    ...
  ]
}
```

---

### **3. GET /api/alpha-signals/stats**

Estatísticas de performance do usuário.

**Query Params:**
- `period` (opcional): Dias (default: 30)

**Resposta:**
```json
{
  "success": true,
  "stats": {
    "totalSignals": 12,
    "completed": 8,
    "active": 4,
    "wins": 6,
    "losses": 2,
    "winRate": 75.00,
    "totalPnl": 245.50,
    "avgPnl": 30.69
  }
}
```

---

### **4. PUT /api/alpha-signals/:id/status**

Atualiza status de um sinal (ex: quando alvo é atingido).

**Payload:**
```json
{
  "status": "completed",
  "pnl": 50.00
}
```

**Resposta:**
```json
{
  "success": true,
  "message": "Status atualizado com sucesso",
  "data": {
    "id": "uuid",
    "status": "completed",
    "pnl": 50.00,
    ...
  }
}
```

---

## 📊 O QUE O USUÁRIO VAI VER (FASE 2)

```
┌─────────────────────────────────────────────────────────┐
│  📊 MEUS SINAIS                                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  📈 Win Rate: 75%  │  💰 PnL: +$245  │  📊 Total: 12  │
│                                                         │
│  FILTROS: [Período: 30d ▼] [Par: Todos ▼] [Status: Todos ▼]│
│                                                         │
│  ┌──────────────────────────────────────────────────────┐│
│  │ Data       │ Par       │ Dir  │ Entry  │ Status │ PnL││
│  ├──────────────────────────────────────────────────────┤│
│  │ 06/03 22h  │ BTC/USDT  │ LONG │ $89k   │ 🟢 TP1 │ +$50││
│  │ 05/03 14h  │ ETH/USDT  │ SHT  │ $3.4k  │ 🔴 Stop│ -$30││
│  │ 04/03 09h  │ SOL/USDT  │ LONG │ $142   │ ⏳ Ativo│  -  ││
│  └──────────────────────────────────────────────────────┘│
│                                                         │
│  [Exportar CSV] [Exportar PDF]                          │
└─────────────────────────────────────────────────────────┘
```

---

## 🗓️ CRONOGRAMA

| Fase | O que | Quando | Status |
|------|-------|--------|--------|
| **1** | Banco + API | 07 Mar 00:10 | ✅ **CONCLUÍDO** |
| **2** | Dashboard Frontend | 07-09 Mar | ⏳ A FAZER |
| **3** | Performance + Gráficos | 10-13 Mar | ⏳ A FAZER |
| **4** | Exportar (CSV/PDF) | 14-17 Mar | ⏳ A FAZER |

---

## 💰 CUSTO

| Item | Custo |
|------|-------|
| **Desenvolvimento (Fase 1)** | $0-50 (2h) |
| **Banco de dados** | $0 (já temos) |
| **Armazenamento** | $0 (baixo volume) |
| **Total Fase 1** | ~$0 |

**Total estimado (todas fases):** $100-300

---

## 🎯 PRÓXIMOS PASSOS (FASE 2)

**Frontend Dashboard:**

1. [ ] Criar página `/dashboard/my-signals`
2. [ ] Tabela com lista de sinais
3. [ ] Filtros (período, par, direção, status)
4. [ ] Cards de estatísticas (Win Rate, PnL)
5. [ ] Status visual (🟢 Green, 🔴 Red, ⏳ Ativo)
6. [ ] Integração com API (`/api/alpha-signals/history`, `/stats`)

**Timeline:** 48-72h

---

## 📝 NOTAS TÉCNICAS

- **Autenticação:** Todas as rotas requerem JWT token (middleware `authenticateToken`)
- **Isolamento:** Cada usuário vê só seus próprios sinais (`WHERE user_id = $1`)
- **Performance:** Índices criados em `user_id`, `created_at`, `status`
- **Segurança:** Prepared statements (previne SQL injection)
- **Escalabilidade:** JSONB pra targets (flexível pra múltiplos alvos)

---

## ✅ TESTES

**Testar API:**

```bash
# 1. Salvar sinal
curl -X POST http://localhost:3002/api/alpha-signals/save \
  -H "Authorization: Bearer SEU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "BTC/USDT",
    "direction": "LONG",
    "entry": {"min": 88000, "max": 90000},
    "targets": [{"tp": 95000, "percentage": 50}],
    "stopLoss": 85000,
    "confidence": 85
  }'

# 2. Listar histórico
curl -X GET "http://localhost:3002/api/alpha-signals/history?period=30" \
  -H "Authorization: Bearer SEU_TOKEN"

# 3. Ver estatísticas
curl -X GET "http://localhost:3002/api/alpha-signals/stats?period=30" \
  -H "Authorization: Bearer SEU_TOKEN"
```

---

**Criado por:** Cabral (Qwen3.5-Plus)  
**Data:** 07 Mar 2026 00:10 UTC  
**Status:** ✅ **FASE 1 CONCLUÍDA**

---

*"Histórico de sinais = Transparência + Confiança + Retenção"* 🍃
