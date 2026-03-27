# Onda 5 — LeveIA Dashboard

## Objetivo
Determinar se `leveia-dashboard/` pode entrar no repositório principal agora.

---

## 1. Diagnóstico factual
### Estrutura encontrada
O diretório `leveia-dashboard/` contém apenas:
- `dist/`
- `node_modules/`

Não foram encontrados, no nível inspecionado:
- `src/`
- `public/`
- `package.json`
- `vite.config.*`
- `index.html` na raiz do projeto-fonte
- qualquer árvore-fonte clara

### Conclusão factual
No estado atual, `leveia-dashboard/` não contém a fonte útil do projeto.
Ele contém apenas:
- artefato de build (`dist/`)
- dependências instaladas (`node_modules/`)

---

## 2. Decisão correta
**Não versionar `leveia-dashboard/` agora.**

Motivo:
Subir esse bloco agora seria subir build + dependências, sem o código-fonte correspondente.
Isso não ajuda engenharia, só polui o repositório.

---

## 3. Solução aplicada
### Proteção recomendada
Adicionar guardas ao `.gitignore` para bloquear esse bloco enquanto a fonte não for localizada:
- `leveia-dashboard/node_modules/`
- `leveia-dashboard/dist/`

---

## 4. Próximo passo correto
Precisamos localizar onde está o source real do dashboard.
Possibilidades:
1. foi gerado em outro diretório e só copiaram o build para cá
2. o source existe em outro repo/projeto paralelo
3. houve limpeza parcial e sobrou só o build

---

## 5. Regra estratégica
Sem `src/` ou equivalente, `leveia-dashboard/` não entra em onda de produto.
Só entra depois que a fonte existir e estiver separada do build.

---

## 6. Conclusão
O bloco foi auditado e descartado corretamente por enquanto.
A ação certa não é commit. É contenção e rastreamento da fonte real.
