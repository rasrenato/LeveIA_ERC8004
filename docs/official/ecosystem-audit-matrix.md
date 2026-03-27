# Ecosystem Audit Matrix

## Objetivo
Consolidar, em um único lugar, o estado auditado do ecossistema do projeto.
Este documento existe para reduzir fantasia, eliminar nomes soltos e dar visão executiva do que é real, ausente, externo, proposto ou bloqueado para versionamento.

---

## Legenda de status
- **ativo** = existe e tem evidência real de uso/operação
- **presente** = existe no workspace, mas não necessariamente validado como ativo
- **externo** = projeto próprio, não tratado como parte do monorepo
- **bloqueado no monorepo** = continua existindo localmente, mas protegido contra versionamento acidental
- **proposto** = desenho recomendado, ainda não aplicado
- **ausente** = não existe no workspace auditado

---

## 1. Núcleo principal
| Bloco | Status | Leitura correta |
|---|---|---|
| `main` (agent) | ativo | agente principal/orquestrador real |
| `minimax` (agent) | presente | existe estrutura, mas não comprovado como operacional |
| `docs/official/` | ativo | camada institucional oficial do projeto |
| `README.md` | ativo | vitrine principal alinhada à camada institucional |
| `~/.openclaw/openclaw.json` | ativo | config real do runtime OpenClaw |

---

## 2. Produto / engenharia
| Bloco | Status | Leitura correta |
|---|---|---|
| `alpha_signals/` | presente | baseline técnico versionado |
| `contracts/` | presente | contratos/artefatos selecionados versionados |
| `erc-8183/` | presente | material técnico/comercial e deploy versionado |
| `scripts/` | presente | automações e scripts versionados |
| `trading/` | presente | bloco curado e versionado com cautela |

---

## 3. Blocos estruturais auditados
| Bloco | Status | Leitura correta |
|---|---|---|
| `leveclaw/` | bloqueado no monorepo | existe localmente, mas auditado como contaminado por runtime/build/logs/secrets |
| `leveia-dashboard/` | bloqueado no monorepo | contém build + node_modules, sem fonte útil visível na auditoria |
| `aster-mcp/` | externo | repo git próprio, mantido fora do monorepo |
| `leveclaw-python-sdk/` | externo | repo git próprio vazio/inicializado, mantido fora do monorepo |
| `leveclaw-github/` | ausente | não existe no workspace auditado |
| `n8n/` | ausente | não existe no workspace auditado |

---

## 4. Agentes e stack de IA
| Item | Status | Leitura correta |
|---|---|---|
| `main` | ativo | cérebro central da operação |
| `research-fast` | proposto | pesquisa e síntese rápida |
| `reasoning-audit` | proposto | segunda opinião / auditoria lógica |
| `coding-executor` | proposto | implementação técnica |
| `local-cheap` | proposto | tarefas locais/baratas |

### Providers validados
- `deepseek`
- `openrouter`
- `custom-api-deepseek-com`
- `nvidia-nim`
- `ollama`

### Providers configurados mas não plenamente validados
- `google` (429 no momento da validação)
- `bailian`
- `custom-api-groq-com`
- `qwen-portal`

---

## 5. Decisões institucionais já tomadas
1. GitHub principal saneado por ondas
2. token removido da URL do remote git
3. runtime local e blocos contaminados protegidos por `.gitignore`
4. docs institucionais criadas e expostas no topo do repo
5. leitura de blocos ausentes passou a ser factual, não imaginada

---

## 6. Leitura executiva final
### O que já parece empresa
- documentação institucional
- governança de repo
- contratos oficiais documentados
- commits curados e empurrados com disciplina
- redução de improviso estrutural

### O que ainda precisa amadurecer
- ativação real dos perfis de agentes especializados
- saneamento profundo de blocos locais contaminados (`leveclaw/`)
- localização de fontes reais de projetos hoje representados só por build ou nome
- consolidação futura dos satélites válidos em arquitetura mais limpa

---

## 7. Regra daqui pra frente
Qualquer novo bloco deve ser classificado imediatamente nesta matriz.
Se não couber claramente em um status, ainda não está institucionalmente entendido.
