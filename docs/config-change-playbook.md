# Config Change Playbook — OpenClaw

## Objetivo
Padronizar qualquer mudança de configuração para não repetir erro básico, confusão de fonte e improviso.

---

## 1. Regra principal
Toda mudança em config precisa deixar artefato.
Sem artefato, não existe mudança.

Artefato mínimo aceitável:
- backup
- diff
- arquivo validado
- evidência de aplicação

---

## 2. Arquivo alvo padrão
**Arquivo ativo padrão:**
- `/root/.openclaw/openclaw.json`

Antes de mexer:
1. confirmar que esse é o alvo da mudança
2. confirmar se a alteração é no runtime ativo ou em arquivo legado do repo

---

## 3. Fluxo obrigatório de mudança
### Etapa 1 — Backup
Criar backup com timestamp.
Exemplo:
```bash
cp /root/.openclaw/openclaw.json /root/.openclaw/openclaw.json.bak.$(date -u +%Y%m%dT%H%M%SZ)
```

### Etapa 2 — Patch
Aplicar mudança apenas no arquivo ativo.
Nunca editar múltiplas configs “por garantia”.

### Etapa 3 — Validação
Validar JSON antes de qualquer restart.
Exemplo:
```bash
python3 -m json.tool /root/.openclaw/openclaw.json >/dev/null
```

### Etapa 4 — Diff
Registrar diff entre antes e depois.
Exemplo:
```bash
diff -u arquivo-antigo arquivo-novo
```

### Etapa 5 — Restart / reload
Só reiniciar quando houver evidência de que a alteração exige isso.
Se não houver certeza, registrar explicitamente que a necessidade de restart ainda não foi validada.

### Etapa 6 — Pós-validação
Depois da mudança:
- verificar se a config continua legível
- verificar se o runtime subiu
- verificar se a feature alterada ficou operacional

---

## 4. O que nunca fazer
- não editar `config.json` do repo achando que é produção
- não editar `openclaw_config_new.json` achando que é produção
- não aplicar patch sem backup
- não declarar mudança concluída sem diff/validação
- não chamar de "ativo" algo que só foi proposto

---

## 5. Mudanças em agentes
Toda mudança de agente deve responder:
1. qual profile foi alterado?
2. qual model primary?
3. qual fallback?
4. qual workspace?
5. o profile já está no arquivo ativo?
6. houve restart? foi necessário ou só presumido?

---

## 6. Mudanças em providers
Toda mudança de provider deve responder:
1. provider foi só configurado ou testado?
2. houve resposta HTTP real?
3. o teste foi 200/429/403/404?
4. o status final é operacional, bloqueado ou não validado?

---

## 7. Convenção de status
### Use apenas estes rótulos
- **confirmado**
- **não confirmado**
- **proposto**
- **legado**
- **operacional**
- **não validado**

Evitar:
- "deve estar"
- "parece que"
- "provavelmente"
sem marcar como inferência

---

## 8. Checklists rápidos
### Antes de responder sobre config
- [ ] Li o arquivo ativo real?
- [ ] Diferenciei ativo vs legado?
- [ ] Tenho artefato?

### Antes de responder sobre agents
- [ ] Existe no arquivo ativo?
- [ ] Existe no filesystem?
- [ ] Existe sessão/evidência real?
- [ ] Está como ativo, existente ou proposto?

### Antes de responder sobre providers
- [ ] Foi testado?
- [ ] Tenho código HTTP ou erro real?
- [ ] Marquei operacional vs não validado?

---

## 9. Resultado esperado
Se este playbook for seguido, não deve mais acontecer:
- confundir config ativa com arquivo do repo
- tratar doc de produto como doc de runtime
- propor estrutura JSON sem validar padrão real
- vender progresso sem artefato
