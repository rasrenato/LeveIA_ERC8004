# GitHub / Repo Saneamento — Diagnóstico Inicial

## Objetivo
Separar o que pode ir para o GitHub do que não deve sequer encostar em commit.
Este documento foi gerado a partir de inspeção real do git local em `/root/openclaw`.

---

## 1. Estado atual do repo local
### Remote confirmado
- `origin -> github.com/rasrenato/LeveIA_ERC8004.git`

### Problemas confirmados
- token embutido na URL do remote
- repositório altamente poluído
- mistura de runtime, memória, docs operacionais, código, mídia, credenciais e experimentos
- `.gitignore` atual insuficiente para o estado do workspace

---

## 2. Categorias encontradas no git status
### Secrets / sensíveis
Exemplos reais detectados:
- `.git-credentials`
- `.openclaw/`
- `google_service_account.json`
- `memory/`
- `MEMORY.md`
- `SOUL.md`
- `HEARTBEAT.md`
- `circle_grant_data.env`
- `trading/test-zapi-token.js`

### Runtime / estado transitório
- `.coverage`
- `__pycache__/`
- `artifacts/`
- `cache/`
- `reports/alpha_prediction_latest.json`

### Docs / notas
- dezenas de `.md` soltos na raiz
- docs novas de operação em `docs/`
- material de marketing, pitch, classificações e relatórios

### Código / produto
- `alpha_signals/`
- `erc-8183/`
- `leveclaw/`
- `skills/`
- `tools/`
- `server/`
- `client/`
- `scripts/`
- `contracts/`

### Mídia / artefatos de evidência
- muitos `.png`
- muitos `.json` operacionais
- dumps e saídas intermediárias

### Dependências / ambientes
- `venv/`
- `venv_chainlink/`
- `venv_x402/`
- `.claude/`
- `.clawhub/`

---

## 3. O que NÃO deve ir para o GitHub
### Bloquear imediatamente
- `.git-credentials`
- `.openclaw/`
- `memory/`
- `MEMORY.md`
- `SOUL.md`
- `USER.md`
- `HEARTBEAT.md`
- `google_service_account.json`
- qualquer `.env` real
- qualquer arquivo com token/credencial operacional
- caches, runtime state e venvs

---

## 4. O que pode ir para o GitHub depois de triagem
### Provável sim
- código fonte real de produto
- contratos
- scripts úteis
- docs de produto que façam sentido como documentação pública/interna de engenharia
- README e documentação consolidada

### Provável não / precisa triagem
- prints de fluxo
- relatórios operacionais temporários
- dumps JSON
- material de memória pessoal/operacional
- docs duplicadas e rascunhos

---

## 5. Problema do `.gitignore` atual
O `.gitignore` atual cobre pouco.
Ele não está barrando adequadamente:
- `.openclaw/` inteiro
- `memory/`
- venvs diversos
- caches Python
- artefatos de build e imagens operacionais
- dumps JSON temporários
- arquivos sensíveis fora do padrão `.env`

---

## 6. Recomendação operacional
### Fase 1 — Segurança
1. remover token da URL do remote
2. expandir `.gitignore`
3. revisar arquivos sensíveis já visíveis no status

### Fase 2 — Higiene
1. separar código versionável de runtime local
2. decidir o que é repositório de produto vs repositório de operação
3. reduzir arquivos soltos na raiz

### Fase 3 — GitHub
1. só depois da triagem comparar com remoto
2. preparar commit limpo por blocos
3. evitar push massivo de sujeira local

---

## 7. Regra prática
Antes de qualquer push:
- se contém segredo → não sobe
- se é runtime local → não sobe
- se é memória operacional/pessoal → não sobe
- se é código ou doc de engenharia útil → triagem e sobe

---

## 8. Próximo passo recomendado
Aplicar saneamento mínimo agora:
1. endurecer `.gitignore`
2. remover credencial do remote
3. gerar diff do `.gitignore`
4. só então revisar o que continua aparecendo no `git status`
