# HEARTBEAT.md

## ⏸️ AUTOMAÇÃO MOLTBOOK + TWITTER - PAUSADA

**Status:** Desativada em 2026-03-06 por decisão do Renato
**Motivo:** Foco em budget tracking e controle de custos primeiro

### Quando reativar:
- Após implementar budget tracking
- Quando tiver controle de custos por agente
- Quando Renato aprovar

---

## 📋 CHECKLIST DE HEARTBEAT (Ativo)

Verificações periódicas (2-4x ao dia):

- [ ] **Emails** - Urgentes não lidos?
- [ ] **Calendar** - Eventos próximas 24-48h?
- [ ] **Projetos** - Git status, pendências?
- [ ] **Memory** - Revisar/atualizar MEMORY.md?

### Rastreamento
Use `memory/heartbeat-state.json` para timestamps:
```json
{
  "lastChecks": {
    "email": null,
    "calendar": null,
    "moltbook": "2026-03-06T11:38:00Z"
  }
}
```

---

## 📜 HISTÓRICO DA AUTOMAÇÃO (Arquivado)

**Período de operação:** ~1025 posts processados, 205 tweets postados
**Última execução:** 2026-03-06T11:34:07Z
**Estado salvo em:** `/root/openclaw/skills/twitter-api/moltbook_automation_state.json`

### Para reativar no futuro:
1. Implementar budget tracking (prioridade)
2. Adicionar hard limits de custo por agente
3. Reverter esta edição do HEARTBEAT.md
