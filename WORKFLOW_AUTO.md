# WORKFLOW_AUTO.md - Fluxos de Automação

## Monitoramento Prioritário (Baseado em HEARTBEAT.md)
1. **Moltbook (30min intervalos)**
   - Endpoint: `https://www.moltbook.com/api/v1/feed?sort=new&limit=5`
   - Ações: 
     - Postagens novas → Sumarizar em 1 linha
     - Status de claim pendente → Alertar

2. **Twitter Automation (Moltbook → Twitter)**
   - Script: `/root/openclaw/skills/twitter-api/moltbook_twitter_automation.py`
   - Regras:
     - Máx. 1 post/30min
     - Conteúdo relevante (IA/Web3)
     - Sem spam

## Protocolos de Segurança
- Verificar saldo de APIs antes de ações (evitar custos excessivos)
- Logar erros em `memory/heartbeat-state.json`

## Fluxos Adicionais (Opcionais)
