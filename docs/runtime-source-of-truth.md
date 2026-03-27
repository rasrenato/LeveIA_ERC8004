# Runtime Source of Truth — OpenClaw

## Objetivo
Este arquivo existe para matar dúvida operacional básica.
Quando houver conflito entre memória, docs antigas, configs soltas e inferência, este arquivo deve ser a referência rápida.

---

## 1. Config ativa
**Config ativa do runtime:**
- `/root/.openclaw/openclaw.json`

**Evidência real:**
- arquivo lido diretamente no ambiente
- providers validados a partir dele
- estrutura `agents.defaults` confirmada nele

---

## 2. Configs não tratadas como fonte ativa
Esses arquivos existem no workspace/repo, mas **não devem ser tratados automaticamente como fonte da verdade**:
- `/root/openclaw/config.json`
- `/root/openclaw/openclaw_config_new.json`

## Regra
Esses arquivos só podem ser usados como:
- referência histórica
- rascunho
- comparação
- migração manual

Nunca assumir que estão em produção sem validação explícita.

---

## 3. Estrutura de agents confirmada
No arquivo ativo, a estrutura confirmada é:

```json
{
  "agents": {
    "defaults": {
      "model": { ... },
      "models": { ... },
      "workspace": "/root/openclaw",
      "memorySearch": { ... },
      "contextPruning": { ... },
      "compaction": { ... },
      "heartbeat": { ... },
      "maxConcurrent": 4,
      "subagents": {
        "maxConcurrent": 8,
        "model": "nvidia-nim/moonshotai/kimi-k2.5"
      }
    }
  }
}
```

## Chave de perfis/agentes nomeados
**Padrão encontrado no repo:**
- `agents.profiles`

**Origem da evidência:**
- `/root/openclaw/config.json`

## Estado atual do arquivo ativo
- `agents.defaults` → presente
- `agents.profiles` → **não presente no arquivo ativo no momento da auditoria**

---

## 4. Providers com validação real
### Operacionais confirmados
- `deepseek`
- `openrouter`
- `custom-api-deepseek-com`
- `nvidia-nim`
- `ollama`

### Configurado mas não utilizável no momento da validação
- `google` → respondeu, mas retornou `HTTP 429`

### Configurado mas não validado como operacional
- `bailian`
- `custom-api-groq-com`
- `qwen-portal`

## Regra
Só considerar "operacional" quando houver teste real bem-sucedido no ambiente atual.

---

## 5. Workspaces criados para novos agentes
Criados fisicamente em:
- `/root/.openclaw/workspaces/research-fast`
- `/root/.openclaw/workspaces/reasoning-audit`
- `/root/.openclaw/workspaces/coding-executor`
- `/root/.openclaw/workspaces/local-cheap`

## Regra
Workspace criado no disco **não significa** agente configurado no runtime.

---

## 6. Regra operacional obrigatória
Antes de afirmar qualquer coisa sobre runtime OpenClaw:
1. verificar `/root/.openclaw/openclaw.json`
2. distinguir fato de inferência
3. não usar `/root/openclaw/docs/` como prova de config de runtime sem leitura do arquivo certo
4. não assumir que arquivo do repo = config ativa
5. não assumir que diretório existente = agente funcional

---

## 7. Perguntas que devem sempre ser respondidas com evidência
- Qual é a config ativa?
- Quais providers estão realmente válidos?
- Quais perfis existem no arquivo ativo?
- Quais workspaces existem no disco?
- O que é legado, proposta ou produção?

---

## 8. Git / GitHub — status real desta auditoria
### Git local confirmado
O workspace `/root/openclaw` é um repositório git com remoto configurado.

**Remote encontrado:**
- `origin -> github.com/rasrenato/LeveIA_ERC8004.git`

### Acesso GitHub API
**Não validado com sucesso nesta auditoria.**
Tentativa de consultar API para `rasrenato/openclaw` sem token disponível no ambiente retornou `HTTP 404`.
Isso não prova ausência de acesso ao GitHub do remoto real; apenas prova que essa consulta específica não confirmou acesso.

### Risco crítico observado
O `git remote -v` exibiu credencial/token embutido na URL do remote.
Isso é péssima prática operacional e deve ser removido da URL do remoto.

---

## 9. Status desta auditoria
**Confirmado:**
- config ativa
- providers validados
- existência de workspaces novos
- padrão `agents.profiles` no repo
- git local com remote apontando para `rasrenato/LeveIA_ERC8004.git`

**Não confirmado aqui:**
- semântica final de todos os campos por profile no runtime ativo
- necessidade de restart para toda e qualquer mudança
- CLI exata para criação automática de agents
- acesso GitHub API validado para inspeção remota autenticada
