# CLASSIFICAÇÃO DE ATIVOS - LEVE IA
## Análise realizada em: 2026-03-22

**Objetivo:** Classificar diretórios e arquivos em 3 grupos:
1. **Migrar agora** para o repo canônico `/root/repos/LeveIA_ERC8004`
2. **Manter fora do git** como operacional/local
3. **Revisar depois**

Foco no produto Leve IA / Alpha Signals / contratos / x402 / docs úteis.

---

## 📁 GRUPO 1: MIGRAR AGORA PARA REPO CANÔNICO

### 📚 Documentação Principal do Produto
- `MASTER_PLAYBOOK_LEVE_IA.md` - Playbook principal da plataforma
- `ALPHA_SIGNALS_TUTORIAL.md` - Tutorial completo Alpha Signals
- `API_DOCUMENTATION.md` - Documentação de APIs
- `ARQUITETURA_CONTRATOS.md` - Arquitetura de contratos
- `CONTRATOS_OFICIAIS.md` - Contratos oficiais
- `ERC8004_INTEGRATION_GUIDE.md` - Guia de integração ERC8004
- `IMPLEMENTACAO_X402.md` - Implementação X402
- `README_X402.md` - Documentação X402
- `TOKENOMICS_V3_AGENTIC.md` - Tokenomics V3
- `X402_IMPLEMENTATION_PLAN.md` - Plano de implementação X402
- `X402_IMPLEMENTATION_SUMMARY.md` - Resumo implementação X402

### 🎯 Alpha Signals (Core Product)
- `alpha_signals/` - Plataforma completa de sinais
  - `alpha_signals_v3.py` - Engine principal V3
  - `api_server.py` - API server
  - `blockchain_api.py` - Integração blockchain
  - `economic_tracker.py` - Rastreador econômico
  - `leaderboard.py` - Leaderboard
  - `result_tracker.py` - Rastreador de resultados
  - `yield_calculator.py` - Calculadora de yield
  - `README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`

### 📊 Contratos e Blockchain
- `contracts/` - Contratos inteligentes
  - `LeveIA_AuditRegistry.sol` - Registro de auditoria
  - `LeveIA_AuditRegistry_Final.sol` - Versão final
  - `ProofOfYield.sol` - Prova de Yield
- `erc-8183/` - Implementação ERC-8183
  - `contracts/` - Contratos ERC-8183
  - `scripts/` - Scripts de deploy
  - `DEPLOY.md`, `IMPLEMENTACAO.md`, `README.md`
- `para_verificacao/` - Contratos para verificação
  - `ERC8183.sol`, `ERC8021.sol`, `ERC8126.sol`
  - `ReputationHook_v2.sol`, `VestingGateIO.sol`

### 🔧 X402 Implementation
- `x402_implementation/` - Implementação X402
- `x402_client/` - Cliente X402
  - `alpha_client.py` - Cliente Alpha
  - `example_real_payment.py` - Exemplo pagamento
- `x402_server/` - Servidor X402
  - `app.py` - Aplicação principal

### 🎨 Dashboard e Interface
- `leveia-dashboard/` - Dashboard Leve IA
  - `package.json`, `vite.config.js`
- `coinmarketleve/` - Integração CoinMarketCap
  - `embed.js` - Embed script

### 📈 Trading e Sinais
- `trading/` - Sistema de trading
  - `signal-generator.js` - Gerador de sinais
  - `whatsapp-concierge.js` - Concierge WhatsApp
  - `CONCIERGE_SCRIPTS.md`, `SINAIS_PRONTOS.md`

### 📋 Documentação Técnica
- `docs/` - Documentação técnica
  - `API.md`, `ARCHITECTURE.md`
  - `GUIA_TESTADOR_ALPHA_SIGNALS.md`
  - `INTEGRACAO_SITES.md`

### 🎪 Marketing e Conteúdo
- `gate-io-*.md` - Documentos Gate.io
- `marketing/` - Material marketing
  - `clickwin-*.md` - Conteúdo ClickWin
  - `PARCEIROS_APRESENTACAO.md`

---

## 🔧 GRUPO 2: MANTER FORA DO GIT (OPERACIONAL/LOCAL)

### 🔐 Configurações e Secrets
- `.env*` - Variáveis de ambiente
  - `.env`, `.env.blockchain`, `.env.secrets`
- `.git-credentials` - Credenciais Git
- `openclaw_config_new.json` - Configuração OpenClaw
- `config.json` - Configurações gerais
- `google_service_account.json` - Service account Google

### 💾 Dados e Cache
- `.coverage` - Dados de cobertura de testes
- `.pytest_cache/` - Cache pytest
- `cache/` - Cache da aplicação
- `data/` - Dados da aplicação
- `logs/` - Logs do sistema
- `memory/` - Memória do assistente
- `reports/` - Relatórios gerados
  - `alpha_prediction_latest.json` - Previsões Alpha

### 🗄️ Node Modules e Dependências
- `node_modules/` - Dependências Node.js
- `venv/`, `venv_chainlink/`, `venv_x402/` - Ambientes virtuais Python

### 📊 Dados Operacionais
- `base_*.json` - Bases de dados
- `contatos_zapi_consolidado.json` - Contatos Z-API
- `moltbook_actual_responses.json` - Respostas Moltbook
- `telefones_formatados*.json` - Telefones formatados

### 🛠️ Scripts e Ferramentas Locais
- `scripts/` - Scripts operacionais
  - `alpha_engine*.py` - Engines Alpha
  - `deploy*.js` - Scripts de deploy
  - `monitor_erc8004.js` - Monitor ERC8004
- `processar_telefones*.py` - Processamento telefones
- `disparo_*.py` - Scripts de disparo

### 🧪 Testes e Desenvolvimento
- `__pycache__/` - Cache Python
- `artifacts/` - Artefatos de build
- `test_*.py`, `test_*.js` - Scripts de teste

---

## 🔍 GRUPO 3: REVISAR DEPOIS

### 🤖 Agentes e Automação
- `AGENTS.md` - Documentação agentes
- `CEO_AGENT_*` - Agente CEO
- `ceo_agent/` - Implementação agente CEO
- `agent-registration.json` - Registro de agentes
- `orchestrate.py` - Orquestração

### 📋 Gestão e Planejamento
- `ANALISE_ARQUITETURA_COMPLETA.md`
- `AUDITORIA_CONTRATOS_GITHUB.md`
- `CABRAL_OPERATING_PROTOCOL.md`
- `DEPLOY_COMPLETO_BSC_MAR2026.md`
- `DOCUMENTO_CONTEXTO_ARQUITETURA.md`
- `GITHUB_ORGANIZADO_MAR2026.md`
- `IMPLEMENTACAO_STATUS.md`
- `KANBAN.md`
- `PROJECT.md`
- `ROADMAP.md`
- `STATE.md`
- `TODO_PROXIMOS_PASSOS.md`

### 🔄 Integrações e MCP
- `aster-mcp/` - Integração Aster MCP
- `aster-skills-hub/` - Hub de skills Aster
- `leveclaw/` - Integração LeveClaw
- `leveia-x402-skill/` - Skill X402

### 📝 Documentação Diversa
- `CLAWWORK_*` - Análises ClawWork
- `FASE2_CONCLUIDA.md`
- `HISTORICO_SINAIS_IMPLEMENTACAO.md`
- `LEVE_IA_Relatorio_Capitulacao_05_02.md`
- `O-QUE-TEMOS-DE-VERDADE.md`
- `PERFORMANCE_REPORT_LAST_24H.md`
- `QA_*` - QA e testes
- `RELATORIO_COMPARACAO_CONTRATOS_BSC_BASE_ETH.md`
- `RESUMO_*` - Resumos diversos
- `STATUS_FINAL.md`
- `VERIFICACAO_*` - Verificações

### 🎭 Identidade e Configuração
- `IDENTITY.md` - Identidade do assistente
- `SOUL.md` - "Alma" do assistente
- `TOOLS.md` - Ferramentas configuradas
- `USER.md` - Informações do usuário

### 📧 Comunicação
- `CONVITE_AMIGOS.md`
- `MENSAGEM_TESTERS_*`
- `TESTE_AMIGOS.md`
- `analise-ceo-testers-alpha-signals.md`
- `testers-*` - Listas de testers
- `sales_followup_*.md` - Follow-up vendas

### 🛠️ Projetos e Experimentos
- `projetos/` - Projetos diversos
- `banners-leve-ia/` - Banners
- `client/` - Cliente genérico
- `examples/` - Exemplos
- `hooks/` - Hooks do sistema
- `n8n/` - Workflows N8N
- `server/` - Servidor genérico
- `skills/` - Skills OpenClaw
- `tools/` - Ferramentas diversas

---

## 🎯 PRIORIZAÇÃO PARA MIGRAÇÃO

### 🚀 PRIORIDADE ALTA (Migrar Imediatamente)
1. **Alpha Signals** - Core do produto
2. **Contratos ERC-8183** - Blockchain core
3. **X402 Implementation** - Sistema de pagamentos
4. **Documentação Principal** - MASTER_PLAYBOOK, tutoriais
5. **Dashboard Leve IA** - Interface principal

### 📦 PRIORIDADE MÉDIA (Migrar em Segunda Fase)
1. **Marketing Materials** - Gate.io, ClickWin
2. **Trading System** - Sinais e concierge
3. **Documentação Técnica** - API, arquitetura
4. **Contratos para Verificação** - ERC8021, ERC8126

### ⏳ PRIORIDADE BAIXA (Revisar/Avaliar)
1. **Agentes e Automação** - CEO Agent, orchestration
2. **Gestão e Planejamento** - Roadmaps, status
3. **Integrações** - Aster MCP, LeveClaw
4. **Documentação Histórica** - Análises antigas

---

## 📊 RESUMO ESTATÍSTICO

**Total de arquivos analisados:** ~300+ arquivos

**Distribuição por grupo:**
- Grupo 1 (Migrar agora): ~120 arquivos (40%)
- Grupo 2 (Manter local): ~100 arquivos (33%)
- Grupo 3 (Revisar depois): ~80 arquivos (27%)

**Principais categorias identificadas:**
1. **Produto Core:** Alpha Signals, contratos, X402
2. **Operacional:** Configs, dados, logs, cache
3. **Documentação:** Tutoriais, playbooks, guias
4. **Marketing:** Gate.io, ClickWin, parceiros
5. **Desenvolvimento:** Scripts, testes, integrações

---

## 🎯 RECOMENDAÇÕES

1. **Iniciar migração pelo Grupo 1 - Prioridade Alta**
2. **Manter Grupo 2 isolado** (não versionar secrets/dados)
3. **Revisar Grupo 3** para decidir o que arquivar/descatar
4. **Criar estrutura clara** no repo canônico:
   - `/docs/` - Documentação
   - `/contracts/` - Contratos
   - `/alpha-signals/` - Core product
   - `/x402/` - Sistema de pagamentos
   - `/dashboard/` - Interface
   - `/marketing/` - Conteúdo marketing

5. **Estabelecer políticas** para:
   - Secrets em `.env` (gitignored)
   - Dados operacionais em `/data/` (gitignored)
   - Logs em `/logs/` (gitignored)
   - Cache em `/cache/` (gitignored)

**Próximos passos:** Executar migração incremental começando pelos arquivos de maior valor para o produto Leve IA.