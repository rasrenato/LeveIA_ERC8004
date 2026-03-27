# README Alignment Notes

## Objetivo
Registrar os pontos em que o `README.md` principal precisa refletir o estado institucional e operacional com mais precisão.

---

## Pontos de atenção identificados
### 1. Estrutura do projeto
O README atual apresenta uma estrutura de projeto mais limpa/idealizada do que o estado real do repositório.
A leitura institucional correta deve evitar tratar como árvore oficial algo que ainda está em saneamento.

### 2. `leveclaw/`
No README atual, `leveclaw/` aparece como frontend principal com `src/app/dashboard/`.
Na auditoria real recente, o diretório estava contaminado por runtime/build/logs e não foi validado como fonte limpa no repo principal.

### 3. `docs/`
O README aponta docs como se a camada central fosse apenas técnica de produto. Agora existe também a camada institucional em `docs/official/`, que deve ser tratada como referência primária para leitura externa séria.

### 4. Tom institucional
O README pode continuar comercial e explicativo, mas precisa evitar parecer mais organizado do que o repositório realmente está em todos os blocos.

---

## Direção correta
### Manter
- pitch do produto
- links oficiais
- contratos
- narrativa de transparência

### Ajustar
- project structure
- wording sobre componentes que ainda estão em saneamento
- ponte explícita entre README principal e camada institucional oficial

---

## Conclusão
O README principal já melhorou com a seção institucional no topo, mas ainda deve ser alinhado para reduzir risco de inconsistência entre vitrine e realidade auditada.
