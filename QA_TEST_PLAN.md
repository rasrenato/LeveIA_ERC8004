# 🧪 Plano de QA - LeveClaw Alpha

**Responsável:** Cabral (Qwen3.5-Plus)
**Período:** 04-06 Março 2026
**Objetivo:** Validar fluxo completo antes de liberar para 6 beta testers

---

## 📊 STATUS GERAL

| Módulo | Status | Progresso | Observações |
|--------|--------|-----------|-------------|
| Frontend | ✅ Online | 100% | https://app.leve.app.br |
| Backend | ✅ Online | 100% | Porta 3002 |
| PostgreSQL | ✅ Online | 100% | Schema leveclaw criado |
| Nginx/HTTPS | ✅ Online | 100% | Proxy configurado |
| Blockchain (Ethereum) | ✅ Encontrado | 100% | Contrato: `0x2333cBC71805b47D64C2867Ef66682c7257B5D4f` (Ethereum Mainnet) |
| Alpha Signals x402 | 🔄 Testar | 0% | $0.10 USDC por sinal |
| Agentes IA | 🔄 Testar | 0% | Integração OpenClaw |

---

## 🗓️ CRONOGRAMA

### **Dia 1 (04/Mar) — Fluxo do Usuário**
- [ ] Registro de nova conta
- [ ] Login/Logout
- [ ] Criação de perfil
- [ ] Dashboard inicial
- [ ] Recuperação de senha

### **Dia 2 (05/Mar) — Alpha Signals x402 & Blockchain**
- [ ] Conexão com carteira (Base Chain)
- [ ] Compra de sinal ($0.10 USDC)
- [ ] Verificação de tx hash no explorador
- [ ] Evento no contrato inteligente
- [ ] Entrega do sinal após pagamento
- [ ] Validação de previsão BTC (direção)

### **Dia 3 (06/Mar) — Agentes IA**
- [ ] Criação de agente
- [ ] Execução de agente
- [ ] Logs e métricas
- [ ] Integração com OpenClaw
- [ ] Webhooks/Notificações

---

## 🔍 CHECKLIST BLOCKCHAIN

### **Contrato LeveIA (Ethereum Mainnet)**
- Endereço: `0x2333cBC71805b47D64C2867Ef66682c7257B5D4f`
- Rede: **Ethereum Mainnet** (Chain ID: 1)
- Status: ✅ Contrato deployado (bytecode presente)
- Verificado: ❌ Não verificado no Etherscan
- Transações: 0 (nenhuma transação registrada)

### **Validações:**
- [x] Contrato existe na blockchain
- [ ] Transação de $0.10 USDC é registrada?
- [ ] Evento `PredictionCreated` é emitido?
- [ ] Direção (UP/DOWN) está correta no log?
- [ ] Timestamp da previsão está sincronizado?
- [ ] Hash da transação é retrievable?

### **Exploradores para validar:**
- https://etherscan.io/address/0x2333cBC71805b47D64C2867Ef66682c7257B5D4f ✅

---

## 🐛 BUGS ENCONTRADOS

| Data | Severidade | Descrição | Status |
|------|------------|-----------|--------|
| 04/Mar | 🔧 Baixa | Bug `/usr/bin/bash.10` → `$0.10` | ✅ Corrigido |
| 04/Mar | ⚠️ Média | Backend em loop (EADDRINUSE) | ✅ Corrigido |
| 04/Mar | ⚠️ Média | PostgreSQL sem schema | ✅ Corrigido |
| 04/Mar | ⚠️ Média | Tabela users não existia | ✅ Corrigido |

---

## ✅ CRITÉRIOS DE GO/NO-GO

### **Go (Liberar para beta testers):**
- [ ] Registro e login funcionais
- [ ] Dashboard carrega sem erros
- [ ] Alpha Signals registra no blockchain
- [ ] Tx hashes são válidos no explorador
- [ ] Nenhum erro crítico no console

### **No-Go (Adiar liberação):**
- [ ] Bloqueio no registro/login
- [ ] Blockchain não registra transações
- [ ] Erros 500 no backend
- [ ] Dados de usuários vazando

---

## 📝 LOG DE TESTES

### **04/Mar — Dia 1**
| Hora | Teste | Resultado | Observações |
|------|-------|-----------|-------------|
| 19:20 | Site no ar | ✅ Pass | https://app.leve.app.br |
| 19:20 | Bug $0.10 | ✅ Corrigido | Substituído em 10 arquivos |
| 19:30 | Backend online | ✅ Pass | Porta 3002, health OK |
| 19:30 | PostgreSQL | ✅ Pass | Schema + tabela users criados |
| 19:22 | Registro de usuário | ✅ Pass | User ID + JWT token gerado |
| 19:22 | Trial 7 dias | ✅ Pass | `2026-03-11T19:22:25Z` |
| 19:22 | Login | ✅ Pass | JWT + settings (pt-BR, SP) |
| 19:44 | Blockchain | ✅ Encontrado | Ethereum Mainnet |
| 19:48 | Script de teste | ✅ Criado | `scripts/test_blockchain_tx.js` |

### **05/Mar — Dia 2 (Fase 1-3 ClawWork)**
| Hora | Teste | Resultado | Observações |
|------|-------|-----------|-------------|
| 00:40 | ClawWork Analysis | ✅ Completo | `/root/openclaw/CLAWWORK_ANALYSIS.md` |
| 00:55 | EconomicTracker | ✅ Criado | `/root/openclaw/alpha_signals/economic_tracker.py` |
| 00:56 | Alpha Tools | ✅ Criado | `decide_activity`, `get_status`, `submit_signal` |
| 00:57 | Testes Fase 1 | ✅ Pass | Todas tools funcionais |
| 01:25 | WorkEvaluator | ✅ Criado | `/root/openclaw/alpha_signals/work_evaluator.py` |
| 01:26 | Testes Fase 2 | ✅ Pass | Scoring 0.0-1.0 funcional |
| 01:36 | Dashboard Setup | ✅ Criado | Vite + React + Tailwind |
| 01:40 | Components | ✅ Criado | StatusCard, Leaderboard, App |
| 01:42 | Build | ✅ Pass | Dashboard compilado com sucesso |

*(Atualizações em tempo real)*

---

## 🎯 PRÓXIMOS PASSOS

1. Testar fluxo completo de registro
2. Validar transações blockchain
3. Testar previsões de BTC (UP/DOWN)
4. Liberar para 6 beta testers (após Go)

---

**Última atualização:** 2026-03-04 19:20 UTC
**Próximo check:** 2026-03-05 09:00 UTC
