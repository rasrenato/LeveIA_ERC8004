# Institutional Source of Truth

## Objetivo
Definir a fonte oficial da verdade para leitura institucional.

---

## 1. Configuração ativa do OpenClaw
**Arquivo ativo confirmado:**
- `/root/.openclaw/openclaw.json`

## Regra
Arquivos do workspace/repo como:
- `/root/openclaw/config.json`
- `/root/openclaw/openclaw_config_new.json`

não devem ser tratados como produção sem validação explícita.

---

## 2. Runtime / GitHub
### Repositório principal confirmado
- `https://github.com/rasrenato/LeveIA_ERC8004.git`

### Branch operacional confirmada
- `master`

### Status institucional
O repositório deixou de ser apenas dump de VPS e passou a receber ondas curadas de governança, engenharia e operação.

---

## 3. Providers de IA validados no ambiente
### Operacionais confirmados
- `deepseek`
- `openrouter`
- `custom-api-deepseek-com`
- `nvidia-nim`
- `ollama`

### Configurado mas não utilizável no momento da validação
- `google` (`HTTP 429`)

### Configurado mas não validado como operacional
- `bailian`
- `custom-api-groq-com`
- `qwen-portal`

---

## 4. Regra institucional
Quando houver conflito entre:
- memória
- arquivo legado
- inferência
- docs espalhadas
- estado do VPS

a prioridade deve ser:
1. artefato real
2. config ativa
3. commit/diff
4. documentação oficial desta pasta

---

## 5. Status
Este documento é a referência mínima para evitar contradição institucional sobre runtime, GitHub e operação.
