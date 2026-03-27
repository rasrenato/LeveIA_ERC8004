# Official Repo Governance — Leve IA

## Objetivo
Estabelecer o padrão institucional do repositório.

---

## 1. O que o repositório deve ser
- base de engenharia
- base de documentação útil
- trilha auditável de decisões técnicas
- vitrine séria para parceiros, exchanges e due diligence

## 2. O que o repositório não deve ser
- dump do servidor
- backup de runtime local
- depósito de segredo
- mistura caótica de código, build, log, memória e experimento

---

## 3. Regra de crescimento
Todo novo bloco deve cair em uma destas classes:
1. produto / engenharia
2. documentação estrutural
3. runtime / segredo / lixo operacional

Classe 3 não sobe.

---

## 4. Ondas aplicadas até agora
### Onda 1
- governança e base operacional

### Onda 2
- baseline técnico de Alpha Signals + contratos + scripts

### Onda 3
- curadoria comercial e `trading/`

### Onda 4
- proteção contra contaminação do `leveclaw/`

### Onda 5
- proteção contra build sem source do `leveia-dashboard/`

### Onda 6
- manutenção de `aster-mcp/` como projeto externo ao monorepo

---

## 5. Regra institucional final
O GitHub deve evoluir por curadoria, não por despejo.
Cada commit relevante deve melhorar:
- clareza
- segurança
- auditabilidade
- legibilidade institucional
