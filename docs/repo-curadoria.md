# Repo Curadoria — Classificação Atual do Git Status

## Objetivo
Separar o que deve entrar no crescimento do repositório do que deve ser revisto e do que não deve subir.
Classificação feita a partir de `git status --porcelain` real.

---

## 1. Classes
### `core-versionar`
Arquivos/pastas que parecem parte do núcleo técnico e da base estrutural.

### `avaliar`
Arquivos que podem ter valor, mas precisam de curadoria antes de versionar.
Aqui mora o risco de subir ruído, duplicação, debug, dumps ou material ainda sem padrão.

### `nao-versionar`
Arquivos sensíveis, pessoais, operacionais ou claramente inadequados para o GitHub.

---

## 2. core-versionar
### Infra/estrutura
- `.gitignore`
- `docs/agents-catalog.md`
- `docs/config-change-playbook.md`
- `docs/github-repo-saneamento.md`
- `docs/repo-growth-base.md`
- `docs/runtime-source-of-truth.md`

### Produto / engenharia
- `alpha_signals/` (quase todo o bloco técnico detectado)
- `aster-mcp/`
- `client/`
- `contracts/`
- `erc-8183/`
- `leveclaw/`
- `leveclaw-github/`
- `leveclaw-python-sdk/`
- `scripts/`
- `server/`
- `skills/`
- `tools/`
- `x402_client/`
- `x402_implementation/`
- `x402_server/`

### Arquivos soltos considerados núcleo técnico
- `deploy.sh`
- `fix_prompt.py`
- `orchestrate.py`
- `package.json`
- `package-lock.json`
- `requirements.txt`
- `requirements_x402.txt`
- `setup_x402.sh`
- `start_x402_server.sh`
- `test_payment_splitter.js`
- `test_twitter.py`
- `test_user_sync.js`
- `verify_contracts_api.py`

### Observação
Mesmo dentro do `core-versionar`, ainda vale revisão fina por diretório antes de commit.
Especialmente:
- backups de código
- arquivos temporários internos
- docs duplicadas dentro de diretórios técnicos

---

## 3. avaliar
### Motivo desta classe
Esses itens não são automaticamente lixo, mas também não deveriam subir no automático.
Precisam de revisão por utilidade, duplicidade e sensibilidade.

### Exemplos fortes desta classe
- muitos `.md` soltos na raiz
- imagens de debug / evidência
- dumps `.json`
- relatórios pontuais
- scripts comerciais / outreach
- materiais de marketing
- diretórios paralelos como `coinmarketleve/`, `leveia-dashboard/`, `n8n/`, `ceo_agent/`, `projects/`, `projetos/`
- `config.json` e `openclaw_config_new.json` (referência, não produção)
- `trading/` quase inteiro precisa triagem separada

### Regra para esta classe
Nada daqui sobe sem decisão consciente.

---

## 4. nao-versionar
### Classificados agora
- `SOUL.md`
- `.env.example`
- `alpha_signals/.env.example`
- `erc-8183/.env.example`
- `trading/test-zapi-token.js`

### Observação importante
Os `.env.example` podem até ser versionáveis em muitos projetos, mas aqui foram classificados com cautela porque o repositório já tem histórico de mistura ruim entre config pública e config sensível.
Devem ser revisados antes de qualquer decisão.

---

## 5. Decisão operacional recomendada
### Commit em ondas
#### Onda 1 — Base organizacional
- `.gitignore`
- docs novas de governança/runtime/curadoria

#### Onda 2 — Núcleo técnico priorizado
- `alpha_signals/`
- `contracts/`
- `erc-8183/`
- `scripts/`
- `server/`
- `client/`
- `tools/`
- `skills/`

#### Onda 3 — Avaliação dirigida
- `trading/`
- docs soltas na raiz
- imagens
- dumps
- projetos paralelos

---

## 6. O que isso resolve
Essa curadoria impede 3 erros clássicos:
1. subir segredo junto com código
2. subir entulho junto com produto
3. transformar o GitHub em backup caótico do VPS

---

## 7. Próximo passo recomendado
Executar a primeira onda:
- preparar commit apenas da base organizacional
- sem tocar ainda no bloco massivo de código
- sem empurrar material duvidoso da classe `avaliar`
