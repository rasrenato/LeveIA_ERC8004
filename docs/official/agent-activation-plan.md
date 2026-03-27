# Agent Activation Plan

## Objetivo
Transformar a stack de agentes proposta em plano operacional real, baseado na config ativa do OpenClaw.

---

## 1. Estado atual confirmado
### Config ativa auditada
Arquivo:
- `/root/.openclaw/openclaw.json`

### Estrutura `agents` confirmada hoje
No momento da auditoria, a config ativa contém apenas:
- `agents.defaults`

Não há, no arquivo ativo auditado agora:
- `agents.profiles`

### Conclusão factual
Os agentes especializados ainda **não estão ativados** na config ativa.
Hoje existe somente:
- padrão global (`defaults`)
- subagents com `model = nvidia-nim/moonshotai/kimi-k2.5`

---

## 2. O que já existe
### Ativo
- `main` como agente/orquestrador real

### Proposto, mas ainda não ativado
- `research-fast`
- `reasoning-audit`
- `coding-executor`
- `local-cheap`

---

## 3. Stack mínima recomendada
### `main`
- papel: orquestração e decisão
- primary: `openai-codex/gpt-5.4`
- fallback: `nvidia-nim/moonshotai/kimi-k2.5`
- status: ativo

### `research-fast`
- papel: pesquisa e síntese rápida
- primary: `nvidia-nim/moonshotai/kimi-k2.5`
- fallback: `openrouter/auto`
- status: recomendado para ativação fase 1

### `reasoning-audit`
- papel: auditoria lógica / segunda opinião
- primary: `custom-api-deepseek-com/deepseek-reasoner`
- fallback: `deepseek/deepseek-chat`
- status: recomendado para ativação fase 1

### `coding-executor`
- papel: implementação técnica
- primary: `openai-codex/gpt-5.4`
- fallback: `nvidia-nim/moonshotai/kimi-k2.5`
- status: recomendado para ativação fase 2

### `local-cheap`
- papel: tarefas locais / baixo custo
- primary: `ollama-qwen35/qwen3.5-opus-distilled`
- fallback: `ollama/kwangsuklee/qwen3.5-opus-distilled:latest`
- status: recomendado para ativação fase 2

---

## 4. Fases recomendadas
### Fase 1 — ativação mínima séria
Ativar primeiro:
- `research-fast`
- `reasoning-audit`

Motivo:
- entregam mais valor imediato
- reduzem risco de alucinação
- melhoram pesquisa e checagem sem multiplicar demais a operação

### Fase 2 — ampliação operacional
Ativar depois:
- `coding-executor`
- `local-cheap`

Motivo:
- úteis, mas entram melhor depois que o fluxo de perfis estiver comprovadamente estável

---

## 5. Recomendação institucional
Não ativar 10 agentes de uma vez.
A ordem correta é:
1. validar a mecânica de perfis na config ativa
2. ativar 2 perfis úteis
3. testar uso real
4. ampliar depois

---

## 6. Próximo passo técnico real
Para sair do plano e ir para a execução, falta:
1. aplicar `agents.profiles` na config ativa
2. validar JSON final
3. confirmar se o runtime passa a reconhecer os perfis
4. testar uma primeira delegação/uso real

---

## 7. Conclusão
Hoje a stack especializada ainda é desenho.
O plano correto não é explosão de agentes, e sim ativação mínima, validada e progressiva.
