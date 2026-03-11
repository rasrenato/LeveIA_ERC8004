# 🎯 CEO AGENT PLAYBOOK - Leve IA Trading Strategy

**Versão:** 1.0  
**Data:** 2026-03-11  
**CEO:** Cabral (AI)  
**Aprovação:** Renato Abreu  

---

## 📜 MISSÃO

Maximizar retorno ajustado ao risco através de operações estratégicas com BTC e ativos crypto, mantendo integridade, transparência e sustentabilidade de longo prazo.

---

## 🛡️ PRINCÍPIOS NÃO NEGOCIÁVEIS

1. **Preservação de Capital > Lucro**
   - Nunca arriscar mais do que podemos perder
   - Drawdown máximo diário: 2%
   - Drawdown máximo mensal: 10%

2. **Validação Antes de Execução**
   - Paper trading mínimo: 7 dias
   - Backtest em dados históricos
   - Only live after consistent profitability

3. **Transparência Total**
   - Todas as decisões logadas
   - Todas as operações auditáveis
   - Renato pode revisar a qualquer momento

4. **Sem Alavancagem Excessiva**
   - Máximo 1x alavancagem (spot primeiro)
   - Nunca "all-in" em uma operação
   - Position sizing baseado em confiança do sinal

---

## 🏗️ ESTRUTURA ORGANIZACIONAL

```
┌─────────────────────────────────────────┐
│           CEO AGENT (Cabral)            │
│  - Estratégia geral                     │
│  - Aprovação final de operações         │
│  - Revisão de performance               │
└─────────────────┬───────────────────────┘
                  │
    ┌─────────────┼─────────────┐
    │             │             │
    ▼             ▼             ▼
┌─────────┐ ┌──────────┐ ┌──────────┐
│ Alpha   │ │ Finance  │ │Compliance│
│Signals  │ │   Ops    │ │   & IR   │
│         │ │          │ │          │
│ - Dados │ │ - Exec   │ │ - Logs   │
│ - Fib   │ │ - Risk   │ │ - Audit  │
│ - Téc   │ │ - Size   │ │ - Report │
└─────────┘ └──────────┘ └──────────┘
```

---

## 📊 DECISION BUS - Fluxo de Decisão

### **Passo 1: Coleta de Sinais (4 Fontes)**

| Fonte | Peso | Dados |
|-------|------|-------|
| Real-time + Whales | 35% | Preço, volume, ETF flow, on-chain |
| Sentimento | 25% | X/Twitter, notícias, Fear & Greed |
| Técnico + Fib | 25% | RSI, MACD, MA, Fibonacci levels |
| Macro | 15% | Fed, geopolítica, tech stocks |

### **Passo 2: Scoring Agregado**

```
Sinal = (Fonte1 × 0.35) + (Fonte2 × 0.25) + (Fonte3 × 0.25) + (Fonte4 × 0.15)

Resultado:
- Score > 70: STRONG BUY
- Score 55-70: BUY
- Score 45-54: HOLD
- Score 30-44: SELL
- Score < 30: STRONG SELL
```

### **Passo 3: Validação de Risco**

```
Checklist obrigatório antes de qualquer operação:
□ Drawdown diário < 2%?
□ Drawdown mensal < 10%?
□ Tamanho da posição dentro do limite?
□ Stop-loss definido?
□ Take-profit definido?
□ Confiança do sinal > 60%?

Se TODOS = SIM → Prosseguir
Se ALGUM = NÃO → Rejeitar operação
```

### **Passo 4: Execução**

```
Paper Trading Mode (Dias 1-7):
- Simular todas as operações
- Registrar resultado
- Ajustar parâmetros se necessário

Live Mode (Após validação):
- Começar com 10% do capital alocado
- Aumentar gradualmente com performance
- Manter stop-loss rigoroso
```

---

## 📈 PARÂMETROS DE OPERAÇÃO

### **Position Sizing**

| Confiança do Sinal | % do Capital |
|-------------------|--------------|
| 60-70% | 5% |
| 70-80% | 10% |
| 80-90% | 15% |
| > 90% | 20% (máximo) |

### **Stop-Loss / Take-Profit**

| Tipo | Distância |
|------|-----------|
| Stop-loss | 3-5% abaixo da entrada |
| Take-profit 1 | 5% acima (vender 50%) |
| Take-profit 2 | 10% acima (vender 25%) |
| Take-profit 3 | 15%+ acima (trail restante) |

### **Limites Diários**

| Métrica | Limite |
|---------|--------|
| Operações máximas/dia | 3 |
| Perda máxima/dia | 2% do capital |
| Ganho mínimo para parar | 5% (opcional) |

---

## 🔧 INFRAESTRUTURA TÉCNICA

### **Fontes de Dados**

```
1. Brave Search API → Sentimento geral, notícias
2. Web Fetch → Dados em tempo real de sites parceiros
3. Glassnode (quando disponível) → On-chain data
4. Whale Alert (quando disponível) → Fluxo de baleias
5. Binance API → Preço, volume, RSI, MACD
```

### **Componentes**

```
/root/openclaw/trading/
├── decision_bus.py        # Agregador de sinais
├── risk_manager.py        # Validação de risco
├── paper_trading.py       # Simulação
├── execution_engine.py    # Execução real (futuro)
├── logger.py              # Logs e auditoria
└── config.json            # Parâmetros configuráveis
```

---

## 📋 LOGS E AUDITORIA

### **Toda Operação Deve Registrar:**

```json
{
  "timestamp": "2026-03-11T02:30:00Z",
  "decision_id": "BTC-20260311-001",
  "signal_score": 68,
  "signal_sources": {
    "realtime": 65,
    "sentiment": 55,
    "technical": 72,
    "macro": 70
  },
  "action": "BUY",
  "position_size": "10%",
  "entry_price": 69500,
  "stop_loss": 67000,
  "take_profit": [73000, 76500, 80000],
  "risk_checks_passed": true,
  "mode": "paper",
  "ceo_approval": "Cabral",
  "notes": "Fib 61.8% target $58k, RSI oversold"
}
```

---

## 🎯 KPIs DE PERFORMANCE

| Métrica | Meta |
|---------|------|
| Win Rate | > 55% |
| Profit Factor | > 1.5 |
| Max Drawdown | < 10% |
| Sharpe Ratio | > 1.0 |
| Avg Win/Loss Ratio | > 1.3 |

---

## 🔄 REVISÃO E AJUSTES

### **Diário (Automático)**
- Revisar operações do dia
- Atualizar logs
- Ajustar parâmetros se necessário

### **Semanal (CEO)**
- Performance da semana
- Ajustes de estratégia
- Report para Renato

### **Mensal (Renato + CEO)**
- Review completo
- Decisões de alocação
- Mudanças de estratégia se necessário

---

## ⚠️ GATILHOS DE EMERGÊNCIA

**Parar todas as operações imediatamente se:**

- Drawdown diário atingir 2%
- Drawdown mensal atingir 10%
- 3 operações perdedoras consecutivas
- Evento macro extremo (guerra, colapso exchange, etc.)
- Falha técnica crítica

**Retomar apenas após:**
- Review completo do CEO
- Aprovação de Renato (se > 5% loss)
- Ajustes implementados

---

## 📞 ESCALONAMENTO

| Situação | Ação |
|----------|------|
| Operação padrão | CEO decide |
| Loss > 5% em dia | Notificar Renato |
| Loss > 10% no mês | Parar, revisar com Renato |
| Mudança de estratégia | Aprovação Renato necessária |
| Live trading após paper | Aprovação Renato necessária |

---

## ✅ CHECKLIST DE ATIVAÇÃO

- [ ] Playbook aprovado por Renato
- [ ] Decision Bus implementado
- [ ] Risk Manager configurado
- [ ] Paper Trading Mode ativo
- [ ] Logs e auditoria funcionando
- [ ] 7 dias de paper trading completados
- [ ] Performance consistente validada
- [ ] Aprovação final para live trading

---

**Documento Vivo:** Este playbook será atualizado conforme aprendizados e performance.

**Última Atualização:** 2026-03-11 02:15 UTC  
**Próxima Revisão:** 2026-03-18 (7 dias)
