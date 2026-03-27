# Agents Catalog — Estado Operacional

## Objetivo
Listar agentes e perfis sem teatro.
Separar o que está ativo, o que está vazio, o que é legado e o que é proposta.

---

## 1. Agentes/diretórios encontrados
### Confirmados no filesystem
- `main`
- `minimax`

Paths:
- `/root/.openclaw/agents/main`
- `/root/.openclaw/agents/minimax`

---

## 2. Agente `main`
### Evidência real lida
Arquivos lidos:
- `/root/.openclaw/agents/main/agent/auth-profiles.json`
- `/root/.openclaw/agents/main/agent/models.json`
- `/root/.openclaw/agents/main/sessions/sessions.json`

### Status
**Ativo / real / operacional**

### Papel atual observado
- orquestrador principal
- executor contextual
- cron worker
- suporte/sales em algumas sessões
- pesquisa em algumas sessões

### Conclusão
O `main` existe e está em uso real.
Não deve ser recriado do zero.
Deve ser tratado como agente principal/orquestrador.

---

## 3. Agente `minimax`
### Evidência real lida
Arquivo lido:
- `/root/.openclaw/agents/minimax/sessions/sessions.json`

### Resultado
- arquivo vazio (`{}`)
- sem sessões registradas
- sem evidência lida de `agent/models.json`
- sem evidência lida de `agent/auth-profiles.json`

### Status
**Existente, mas não comprovado como operacional**

### Conclusão
`minimax` hoje é tratado como estrutura existente, não como agente pronto para uso.
Não deve ser assumido como parte da stack funcional até ser configurado/validado.

---

## 4. Perfis/agentes propostos
Esses perfis ainda **não estavam presentes no arquivo ativo** no momento desta catalogação.
Eles são proposta operacional baseada em providers validados.

### 4.1 `research-fast`
- função: pesquisa rápida e síntese
- primary: `nvidia-nim/moonshotai/kimi-k2.5`
- fallback: `openrouter/auto`
- workspace: `/root/.openclaw/workspaces/research-fast`
- status: **proposto**

### 4.2 `reasoning-audit`
- função: auditoria lógica / segunda opinião
- primary: `custom-api-deepseek-com/deepseek-reasoner`
- fallback: `deepseek/deepseek-chat`
- workspace: `/root/.openclaw/workspaces/reasoning-audit`
- status: **proposto**

### 4.3 `coding-executor`
- função: implementação/código
- primary: `openai-codex/gpt-5.4`
- fallback: `nvidia-nim/moonshotai/kimi-k2.5`
- workspace: `/root/.openclaw/workspaces/coding-executor`
- status: **proposto**

### 4.4 `local-cheap`
- função: tarefas locais/baratas
- primary: `ollama-qwen35/qwen3.5-opus-distilled`
- fallback: `ollama/kwangsuklee/qwen3.5-opus-distilled:latest`
- workspace: `/root/.openclaw/workspaces/local-cheap`
- status: **proposto**

---

## 5. Regra de leitura deste catálogo
### Status possíveis
- **ativo** = há evidência real de uso/operação
- **existente** = diretório/estrutura existe
- **proposto** = desenho recomendado, ainda não aplicado
- **legado** = não usar como base sem revalidação

---

## 6. Recomendação operacional atual
### Manter
- `main` como orquestrador principal

### Não assumir como pronto
- `minimax`

### Criar/configurar se a decisão for seguir com stack especializada
- `research-fast`
- `reasoning-audit`
- `coding-executor`
- `local-cheap`

---

## 7. Regra de governança
Nenhum agente entra como "ativo" só porque:
- o nome existe
- o diretório existe
- a ideia é boa
- apareceu em doc

Só entra como ativo quando houver:
- config aplicada
- workspace associado
- modelo definido
- evidência de uso real ou teste validado
