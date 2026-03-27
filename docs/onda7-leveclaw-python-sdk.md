# Onda 7 — LeveClaw Python SDK

## Objetivo
Resolver a situação estrutural de `leveclaw-python-sdk/` no workspace.

---

## 1. Diagnóstico factual
### O que foi encontrado
`leveclaw-python-sdk/` é um diretório com repositório git próprio (`.git/`), porém:
- **sem commits iniciais**
- sem árvore-fonte visível no nível auditado
- sem arquivos de projeto identificados além da estrutura do git

### Conclusão factual
No estado atual, `leveclaw-python-sdk/` não é:
- fonte validada
- projeto pronto
- dependência clara
- parte saudável do monorepo

É, hoje, uma **casca de repositório vazio/inicializado**.

---

## 2. Decisão correta
**Não internalizar e não versionar no repo principal agora.**

Motivo:
- não há conteúdo útil auditado para subir
- manter isso visível como candidato a commit só cria ruído estrutural
- repo vazio dentro de repo principal é sinal de desorganização, não de maturidade

---

## 3. Solução aplicada
### Estratégia
Tratar `leveclaw-python-sdk/` como projeto externo/incompleto até haver uma das duas coisas:
1. fonte real colocada ali com intenção clara
2. remoção/abandono consciente

---

## 4. Regra prática
Enquanto estiver nesse estado, o repo principal deve ignorar `leveclaw-python-sdk/`.

---

## 5. Conclusão
`leveclaw-python-sdk/` não entra como onda de engenharia.
Entra como caso de governança: repositório vazio/inicializado, mantido fora do monorepo até decisão explícita.
