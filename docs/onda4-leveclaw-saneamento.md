# Onda 4 — LeveClaw Saneamento e Solução

## Objetivo
Dar uma solução correta para o bloco `leveclaw/`, que hoje não está pronto para entrar no repositório principal sem risco operacional.

---

## 1. Diagnóstico factual
### Estrutura encontrada em `leveclaw/`
No estado atual inspecionado, o diretório contém basicamente runtime e build local:

- `leveclaw/.env.production`
- `leveclaw/backend/.env`
- `leveclaw/backend/logs/`
- `leveclaw/backend/node_modules/`
- `leveclaw/e2e.log`
- `leveclaw/frontend/.next/`
- `leveclaw/frontend/frontend.log`
- `leveclaw/frontend/node_modules/`

### Conclusão factual
No estado atual visível pelo filesystem, `leveclaw/` **não está apresentando fonte útil pronta para versionamento**.
O que aparece é essencialmente:
- segredo
- logs
- build artefact
- dependências instaladas
- estado de execução local

---

## 2. Problema real
Se esse bloco fosse commitado agora, o efeito seria ruim:
- subir `.env`
- subir `.env.production`
- subir logs
- subir `node_modules`
- subir `.next`
- subir ruído de execução

Isso não melhora o projeto. Só polui o GitHub.

---

## 3. Solução recomendada
### Decisão
**Não versionar `leveclaw/` agora.**

### Motivo
Ainda não há evidência suficiente de uma árvore-fonte limpa dentro dele.
O diretório precisa primeiro ser saneado internamente.

---

## 4. Plano correto para `leveclaw/`
### Fase A — Extração da fonte real
Precisamos localizar onde está o código-fonte de verdade:
- backend source
- frontend source
- manifests (`package.json`, etc.)
- configs públicas
- docs técnicas úteis

### Fase B — Separação
Separar explicitamente:
- `source/`
- `runtime/`
- `build/`
- `logs/`
- `secrets/`

### Fase C — Só depois versionar
Apenas quando essa separação existir, o bloco pode entrar em uma nova onda.

---

## 5. Recomendação operacional agora
### Para o repositório principal
Adicionar regras de ignore específicas para evitar entrada acidental de lixo do `leveclaw/`:
- `leveclaw/**/.env`
- `leveclaw/**/.env.*`
- `leveclaw/**/node_modules/`
- `leveclaw/**/.next/`
- `leveclaw/**/logs/`
- `leveclaw/**/*.log`

---

## 6. Decisão estratégica
### Melhor escolha agora
Em vez de insistir em `leveclaw/`, o projeto deve seguir por dois caminhos em paralelo:

1. **proteger o repo principal** contra o lixo do `leveclaw/`
2. **deixar o saneamento interno do `leveclaw/` como tarefa dedicada**

Isso mantém o crescimento do repo saudável sem travar o projeto inteiro por causa de um diretório contaminado.

---

## 7. Conclusão
A solução correta não é “dar push no `leveclaw/`”.
A solução correta é:
- bloquear a sujeira
- documentar o problema
- voltar depois com extração cirúrgica da fonte
