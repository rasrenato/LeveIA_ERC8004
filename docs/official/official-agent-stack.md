# Official Agent Stack — Leve IA / OpenClaw

## Objetivo
Definir a leitura institucional da stack de agentes.

---

## 1. Agente principal
### `main`
Status:
- ativo
- orquestrador principal
- concentra contexto, operação e tomada de decisão

Regra:
- não recriar outro “main” sem necessidade real

---

## 2. Perfis especializados propostos
### `research-fast`
- função: pesquisa e síntese rápida
- primary: `nvidia-nim/moonshotai/kimi-k2.5`
- fallback: `openrouter/auto`
- status: proposto

### `reasoning-audit`
- função: auditoria lógica / segunda opinião
- primary: `custom-api-deepseek-com/deepseek-reasoner`
- fallback: `deepseek/deepseek-chat`
- status: proposto

### `coding-executor`
- função: implementação técnica
- primary: `openai-codex/gpt-5.4`
- fallback: `nvidia-nim/moonshotai/kimi-k2.5`
- status: proposto

### `local-cheap`
- função: tarefas locais e baratas
- primary: `ollama-qwen35/qwen3.5-opus-distilled`
- fallback: `ollama/kwangsuklee/qwen3.5-opus-distilled:latest`
- status: proposto

---

## 3. Regra institucional
Agente só vira “ativo” quando houver:
- config aplicada
- modelo definido
- workspace associado
- validação de uso real

Sem isso, continua como proposta.

---

## 4. Princípio de governança
A stack deve ampliar execução real, não criar zoológico de agentes.
