# Repo Growth Base — Próximo Nível de Organização

## Objetivo
Estabelecer a base de crescimento do repositório sem levar lixo, segredo e runtime local para o GitHub.

---

## 1. O que foi feito agora
### `.gitignore` reforçado
O `.gitignore` foi expandido para bloquear:
- segredos e credenciais
- memória operacional/pessoal
- runtime OpenClaw local
- caches Python
- venvs
- estado local de ferramentas
- artefatos temporários

### Resultado prático
Depois do endurecimento do `.gitignore`, várias classes de sujeira deixaram de aparecer no `git status`, especialmente:
- `.openclaw/`
- `memory/`
- venvs
- caches locais
- `.claude/`
- `.clawhub/`

---

## 2. O que ainda sobra no status
O que ainda aparece agora é, em grande parte:
- código potencialmente versionável
- documentação espalhada
- imagens e evidências operacionais
- JSONs e dumps misturados
- scripts e projetos paralelos

Isso é bom: a camada mais tóxica foi parcialmente contida.
Agora começa a triagem de verdade.

---

## 3. Base de crescimento recomendada
### Camada A — Runtime local (não sobe)
- `.openclaw/`
- `memory/`
- credenciais
- tokens
- venvs
- caches
- estado transitório

### Camada B — Operação/documentação interna (sobe só se fizer sentido)
- docs operacionais consolidadas
- playbooks
- catálogos
- relatórios úteis e permanentes

### Camada C — Produto/engenharia (prioridade de versionamento)
- código
- contratos
- scripts
- SDKs
- integrações
- documentação técnica de produto

---

## 4. Nova regra de crescimento
Antes de adicionar qualquer arquivo ao GitHub, ele deve cair em uma destas 3 classes:
1. **produto**
2. **documentação estrutural**
3. **lixo operacional / segredo / runtime**

Se cair na classe 3, não sobe.

---

## 5. Próxima sequência correta
### Fase 1 — Segurança
- remover token do remote git

### Fase 2 — Curadoria
Separar em grupos:
- `core-versionar`
- `avaliar`
- `não-versionar`

### Fase 3 — Estrutura
Consolidar documentação útil em poucos arquivos centrais, em vez de dezenas de `.md` soltos.

### Fase 4 — Push limpo
Só depois da triagem por blocos.

---

## 6. Meta
O objetivo não é "subir tudo".
É transformar o repositório em:
- base de engenharia confiável
- base de documentação útil
- base escalável para novos agentes e novos produtos

Sem isso, crescimento vira acúmulo.
