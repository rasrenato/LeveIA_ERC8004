# Onda 6 — Aster MCP

## Objetivo
Resolver corretamente a situação do diretório `aster-mcp/` dentro do repositório principal.

---

## 1. Diagnóstico factual
### O que foi encontrado
`aster-mcp/` é um **repositório git próprio**, com:
- `.git/` interno
- remote próprio: `https://github.com/asterdex/aster-mcp.git`
- branch: `main`
- status limpo (`main...origin/main`)

Também contém:
- código Python real (`aster_mcp/`)
- `pyproject.toml`
- `requirements.txt`
- `tests/`
- docs próprias
- `venv/`
- `__pycache__/`
- `aster_mcp.egg-info/`

---

## 2. Conclusão factual
`aster-mcp/` não é sujeira de runtime como `leveclaw/`.
Mas também **não deve ser commitado diretamente dentro do repo principal** como pasta comum.

Motivo:
- é um repo git embutido
- isso gera ambiguidade estrutural
- outer repo não vai carregar o conteúdo como um diretório comum de forma saudável
- pode virar pseudo-submódulo acidental ou referência quebrada

---

## 3. Decisão correta
### Não internalizar agora no repo principal
A decisão segura é:
- **não adicionar `aster-mcp/` como pasta comum do repo principal**
- **não transformar em submódulo sem decisão explícita**

---

## 4. Solução aplicada
### Proteção no repo principal
Bloquear o caminho `aster-mcp/` no repositório principal até decisão formal.

### Manter como projeto externo
Por enquanto, `aster-mcp/` deve ser tratado como:
- dependência local de desenvolvimento
- projeto externo acoplado ao workspace
- não como parte nativa do monorepo atual

---

## 5. Próximas opções válidas
### Opção A — manter externo (recomendado agora)
- ignorar no repo principal
- documentar como dependência/projeto paralelo

### Opção B — submódulo formal
Só faz sentido se houver decisão deliberada de manter vínculo explícito com o repo original.

### Opção C — internalização real
Só faria sentido se o projeto fosse forkado ou absorvido, com remoção do `.git/` interno e curadoria completa.

---

## 6. Recomendação
**Recomendação atual: Opção A.**

Motivo:
- resolve a ambiguidade
- não quebra o repo principal
- preserva o `aster-mcp` como unidade própria
- evita criar dependência estrutural mal resolvida

---

## 7. Conclusão
`aster-mcp/` não entra como onda de código agora.
Entra como caso de governança estrutural: projeto externo mantido fora do monorepo até decisão explícita.
