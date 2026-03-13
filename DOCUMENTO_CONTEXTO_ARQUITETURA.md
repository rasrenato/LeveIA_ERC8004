# 📐 DOCUMENTO DE CONTEXTO - ARQUITETURA LEVE IA

**Data:** 2026-03-13 01:50 UTC  
**Autor:** Cabral (Arquiteto de Software)  
**Status:** ⚠️ EM REVISÃO (pós-auditoria)  
**Rede Principal:** BSC (Binance Smart Chain) - Chain ID: 56

---

## 🎯 VISÃO GERAL DO SISTEMA

**Leve IA** é uma plataforma SaaS de sinais de trading com IA + transparência blockchain.

**Stack:**
- Frontend: Next.js 14 + React + TypeScript
- Backend: Node.js (Express) + Python (Flask)
- Blockchain: BSC (5 smart contracts)
- Database: PostgreSQL

---

## 1. 🗺️ MAPA DE DEPENDÊNCIAS

### **1.1 FRONTEND (Next.js)**

```
/opt/leveclaw/frontend/src/
├── app/
│   ├── dashboard/
│   │   ├── page.tsx ──────────────────┐
│   │   ├── alpha-signals/             │
│   │   │   └── page.tsx               │
│   │   └── leveia/                    │
│   │       └── page.tsx               │
│   └── login/                         │
│       └── page.tsx                   │
├── components/                        │
│   ├── leveia/                        │
│   │   ├── BTCPrediction.tsx ─────────┤
│   │   ├── ContractList.tsx ──────────┤
│   │   └── SignalGuide.tsx ───────────┤
│   └── ui/                            │
└── contexts/                          │
    └── AuthContext.tsx ───────────────┘
```

**Dependências:**
```
dashboard/page.tsx
  ├── Importa: BTCPrediction.tsx
  ├── Importa: ContractList.tsx
  ├── Importa: SignalGuide.tsx
  └── Usa: AuthContext.tsx (autenticação)

BTCPrediction.tsx
  └── Chama: GET /api/alpha-signals/btc-price

ContractList.tsx
  └── Chama: GET /api/alpha-signals/contracts

SignalGuide.tsx
  └── Estático (sem chamadas API)
```

---

### **1.2 BACKEND (Node.js + Express)**

```
/opt/leveclaw/backend/
├── server.js ─────────────────────────┐
├── routes/                            │
│   ├── alpha-signals.js ──────────────┤
│   ├── auth.js ───────────────────────┤
│   └── analytics.js ──────────────────┤
├── middleware/                        │
│   └── auth.js ───────────────────────┤
└── config/                            │
    └── database.js ───────────────────┘
```

**Dependências:**
```
server.js
  ├── Importa: routes/alpha-signals.js
  ├── Importa: routes/auth.js
  ├── Importa: middleware/auth.js
  └── Conecta: config/database.js

alpha-signals.js
  ├── GET /btc-price ──────> Binance API (externo)
  ├── GET /contracts ──────> Hardcoded (dados estáticos)
  ├── GET /signals ────────> PostgreSQL
  └── POST /save ──────────> PostgreSQL
```

---

### **1.3 AI ENGINE (Python + Flask)**

```
/root/openclaw/alpha_signals/
├── api_server.py ─────────────────────┐
├── alpha_signals_v3.py ───────────────┤
├── alpha_tools.py ────────────────────┤
└── data/                              │
    └── alpha_predictions.json ────────┘
```

**Dependências:**
```
api_server.py
  ├── Importa: alpha_signals_v3.py
  ├── Importa: alpha_tools.py
  ├── Chama: Binance API (externo)
  └── Salva: data/alpha_predictions.json

alpha_signals_v3.py
  ├── Analisa: BTC, ETH, BNB
  ├── Gera: Sinais (entrada, alvo, stop)
  └── Salva: PostgreSQL (via api_server)
```

---

### **1.4 SMART CONTRACTS (Solidity)**

```
/root/openclaw/erc-8183/contracts/
├── IACPHook.sol ──────────────────────┐
├── IERC8183.sol ──────────────────────┤
├── ERC8183.sol ───────────────────────┤
├── ReputationHook_v2.sol ─────────────┤
├── ERC8126.sol ───────────────────────┤
├── ERC8021.sol ───────────────────────┤
└── VestingGateIO.sol ─────────────────┘
```

**Dependências:**
```
ReputationHook_v2.sol
  ├── Importa: IACPHook.sol
  ├── Importa: ERC8183.sol
  └── Chama: ERC-8004 Registry (externo)

ERC8183.sol
  ├── Importa: IERC8183.sol
  └── Interface principal (x402)

ERC8126.sol, ERC8021.sol, VestingGateIO.sol
  └── Independentes (sem imports internos)
```

---

## 2. 🔄 FLUXO DE DADOS PRINCIPAL

### **2.1 FLUXO: GERAÇÃO DE SINAL**

```
┌─────────────────┐
│  Binance API    │ (Preço BTC em tempo real)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ alpha_signals   │ (Python - Gera sinal)
│ _v3.py          │  - Entrada: $88,000
│                 │  - Alvos: $95k, $100k
│                 │  - Stop: $85k
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ api_server.py   │ (Flask API)
│                 │  - Salva no PostgreSQL
│                 │  - Expõe via REST
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Backend Node.js │ (Express)
│ alpha-signals.js│  - GET /signals
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Frontend        │ (Next.js)
│ BTCPrediction   │  - Exibe pro usuário
└─────────────────┘
```

---

### **2.2 FLUXO: VERIFICAÇÃO DE CONTRATO**

```
┌─────────────────┐
│ Contrato BSC    │ (Bytecode na blockchain)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ BSCScan         │ (Verificação manual)
│                 │  - Upload código fonte
│                 │  - Validação compiler
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Selo Verde ✓    │ (Código público)
└─────────────────┘
```

**STATUS ATUAL:** ⚠️ 5/5 contratos NÃO verificados

---

### **2.3 FLUXO: AUTENTICAÇÃO**

```
┌─────────────────┐
│ Usuário         │ (Login/Senha)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ AuthContext.tsx │ (Frontend)
│                 │  - Armazena token JWT
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ auth.js         │ (Backend)
│                 │  - Valida credenciais
│                 │  - Gera JWT
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ PostgreSQL      │ (Tabela users)
└─────────────────┘
```

---

## 3. 📋 CONTRATOS BÁSICOS (NÃO PODEM QUEBRAR)

### **3.1 INTERFACES FRONTEND**

```typescript
// Componentes LeveIA
interface BTCPredictionProps {
  // Sem props (busca dados internos)
}

interface ContractListProps {
  // Sem props (busca dados internos)
}

interface SignalGuideProps {
  // Sem props (estático)
}

// API Responses
interface BTCPriceResponse {
  success: boolean;
  data: {
    price: number;
    change_24h: number;
    high_24h: number;
    low_24h: number;
    volume_24h: number;
    timestamp: string;
  };
}

interface ContractResponse {
  name: string;
  address: string;
  network: string;
  function: string;
  color: string;
  bscscan: string;
}
```

---

### **3.2 ESTRUTURAS DE DADOS (BACKEND)**

```javascript
// Sinal Alpha
{
  symbol: "BTC/USDT",
  direction: "LONG" | "SHORT",
  entry_min: number,
  entry_max: number,
  targets: number[],
  stop_loss: number,
  confidence: number,
  status: "active" | "expired" | "win" | "loss",
  pnl: number,
  created_at: timestamp
}

// Usuário
{
  id: UUID,
  email: string,
  password_hash: string,
  created_at: timestamp
}
```

---

### **3.3 INTERFACES SMART CONTRACTS**

```solidity
// ERC-8183 (Principal)
interface IERC8183 {
  function setProvider(uint256 jobId, address provider, bytes calldata optParams) external;
  function setBudget(uint256 jobId, uint256 amount, bytes calldata optParams) external;
  function submit(uint256 jobId, bytes32 deliverable, bytes calldata optParams) external;
  function complete(uint256 jobId, bytes32 reason, bytes calldata optParams) external;
  function reject(uint256 jobId, bytes32 reason, bytes calldata optParams) external;
}

// ReputationHook_v2
interface IERC8004 {
  function emitAttestation(
    address agent,
    string memory signalType,
    bytes memory data
  ) external returns (uint256);
}
```

---

## 4. 🚨 PONTO DE FALHA ATUAL

### **4.1 PROBLEMA CRÍTICO #1: DOCUMENTAÇÃO DE CONTRATOS**

**Sintoma:**
```
❌ 77% dos arquivos de documentação têm endereços ERRADOS
❌ 3 redes diferentes mencionadas (BSC, Base, Ethereum)
❌ 2 conjuntos de endereços circulando (antigos vs. novos)
❌ 1 endereço fantasma (0x2333cBC...) que não existe
```

**Arquivos Afetados:**
```
❌ API_DOCUMENTATION.md (diz Base, endereço errado)
❌ ERC8004_INTEGRATION_GUIDE.md (diz Base, endereço errado)
❌ IMPLEMENTACAO_STATUS.md (diz Base, endereço errado)
❌ ARQUITETURA_CONTRATOS.md (endereços antigos)
❌ ANALISE_ARQUITETURA_COMPLETA.md (endereços antigos)
❌ CONTRATOS_OFICIAIS.md (faltando VestingGateIO)
```

**Arquivos Corretos:**
```
✅ DEPLOY_COMPLETO_BSC_MAR2026.md (endereços reais)
✅ MEMORY.md (atualizado)
✅ README.md (GitHub, endereços corretos)
```

**Impacto:**
- Testers tentando verificar contratos errados no BSCScan
- Investidores confusos sobre qual rede é a correta
- Perda de confiança na documentação

**Solução:**
```
1. Atualizar CONTRATOS_OFICIAIS.md com TODOS os 6 contratos
2. Marcar TODOS os arquivos errados como "OBSOLETO"
3. Buscar/substituir endereços antigos em TODO o código
4. Criar regra: "Só atualiza endereços em CONTRATOS_OFICIAIS.md"
```

---

### **4.2 PROBLEMA CRÍTICO #2: CONTRASTES NÃO VERIFICADOS**

**Sintoma:**
```
❌ 5/5 contratos deployados na BSC estão NÃO VERIFICADOS
❌ Código fonte NÃO público no BSCScan
❌ Zero transações em todos os contratos
❌ Sem website/social linkado
```

**Contratos Afetados:**
```
❌ ERC-8183: 0xcf0520e60ad602454f06Cd80f588634A332d169d
❌ ERC-8004: 0x2A0Af7fA4e8A39bF7B34201CdDba8faed88C27c2
❌ ERC-8126: 0x1d693286CE314fE7dEB26AeDcA3DF7f45F386133
❌ ERC-8021: 0x9e5100EF4Dd701d59aeaF95C89403308cc6dF368
❌ VestingGateIO: 0x5798bbECAF20E013718bd89Ef7339b5Ae3643Ff1

✅ Token LEVE: 0x67e463AcC3B35406B0f35C8Ed531da89f9670861 (verificado)
```

**Impacto:**
- Ninguém consegue auditar o código
- Perda de confiança de investidores/testers
- Risco de segurança (bytecode sem fonte)

**Solução:**
```
1. Usar arquivos em: /root/openclaw/para_verificacao/
2. Verificar cada contrato no BSCScan (manual, 25 min)
3. Adicionar website: https://levecoin.io
4. Adicionar email: rasrenato@gmail.com
```

---

### **4.3 PROBLEMA CRÍTICO #3: INCONSISTÊNCIA DE REDE**

**Sintoma:**
```
❌ Dashboard menciona "Base Chain" em alguns lugares
❌ Documentação fala "Ethereum Mainnet" em outros
❌ Contratos reais estão na BSC
```

**Arquivos Confusos:**
```
❌ /opt/leveclaw/frontend/src/app/home/page.tsx (diz Base)
❌ API_DOCUMENTATION.md (diz Base)
❌ ERC8004_INTEGRATION_GUIDE.md (diz Base)
❌ QA_BLOCKCHAIN_FINAL.md (diz Ethereum)
```

**Realidade:**
```
✅ TODOS os contratos estão na BSC (Chain ID: 56)
✅ Token LEVE: BSC (53 holders)
✅ Deploy: 2026-03-12
```

**Solução:**
```
1. Buscar "Base" em TODO o código frontend
2. Substituir por "BSC" ou "Binance Smart Chain"
3. Atualizar TODOS os arquivos .md
4. Criar regra: "Sempre usar 'BSC', nunca 'Base'"
```

---

## 5. 📊 STATUS ATUAL (RESUMO)

| Componente | Status | Problemas |
|------------|--------|-----------|
| **Frontend** | ✅ Online | ⚠️ Menção a "Base" (deveria ser BSC) |
| **Backend** | ✅ Online | ✅ OK |
| **AI Engine** | ✅ Online | ✅ OK |
| **PostgreSQL** | ✅ Online | ✅ OK |
| **Smart Contracts** | ✅ Deployados | ❌ Não verificados no BSCScan |
| **Documentação** | ❌ Bagunçada | ❌ 77% com informações erradas |

---

## 6. 🎯 PRIORIDADES (PRÓXIMOS 7 DIAS)

### **Dia 1 (HOJE - 13/Mar):**
```
□ Verificar 5 contratos no BSCScan (25 min, manual)
□ Atualizar CONTRATOS_OFICIAIS.md com endereços corretos
□ Marcar arquivos obsoletos
```

### **Dia 2-3 (14-15/Mar):**
```
□ Buscar/substituir "Base" → "BSC" no frontend
□ Buscar/substituir endereços antigos → novos
□ Atualizar API_DOCUMENTATION.md
□ Atualizar ERC8004_INTEGRATION_GUIDE.md
```

### **Dia 4-5 (16-17/Mar):**
```
□ Coletar feedback dos testers (até 18h 13/Mar)
□ Testar integrações com contratos verificados
□ Adicionar website/social nos contratos
```

### **Dia 6-7 (18-19/Mar):**
```
□ Revisão geral da documentação
□ Testes de ponta a ponta
□ Preparar pitch Gate.io
```

---

## 7. 🔗 LINKS IMPORTANTES

### **Repositório:**
```
GitHub: https://github.com/rasrenato/LeveIA_ERC8004
```

### **Dashboard:**
```
https://app.leve.app.br
```

### **Contratos (BSCScan):**
```
ERC-8183: https://bscscan.com/address/0xcf0520e60ad602454f06Cd80f588634A332d169d
ERC-8004: https://bscscan.com/address/0x2A0Af7fA4e8A39bF7B34201CdDba8faed88C27c2
ERC-8126: https://bscscan.com/address/0x1d693286CE314fE7dEB26AeDcA3DF7f45F386133
ERC-8021: https://bscscan.com/address/0x9e5100EF4Dd701d59aeaF95C89403308cc6dF368
VestingGateIO: https://bscscan.com/address/0x5798bbECAF20E013718bd89Ef7339b5Ae3643Ff1
Token LEVE: https://bscscan.com/token/0x67e463AcC3B35406B0f35C8Ed531da89f9670861
```

### **Documentação Correta:**
```
✅ DEPLOY_COMPLETO_BSC_MAR2026.md
✅ MEMORY.md
✅ README.md (GitHub)
❌ CONTRATOS_OFICIAIS.md (precisa atualizar)
❌ API_DOCUMENTATION.md (precisa corrigir)
```

---

## 8. ⚠️ ALERTAS DE SEGURANÇA

### **NUNCA FAZER:**
```
❌ Commitar .env com chaves privadas
❌ Usar endereços de teste em produção
❌ Documentar sem verificar no BSCScan
❌ Falar de "Base" ou "Ethereum" (é BSC!)
```

### **SEMPRE FAZER:**
```
✅ Verificar endereços em CONTRATOS_OFICIAIS.md
✅ Testar em testnet antes de mainnet
✅ Verificar contratos no BSCScan após deploy
✅ Atualizar documentação ANTES de mergar
```

---

**Última Atualização:** 2026-03-13 01:50 UTC  
**Próxima Revisão:** 2026-03-20 (7 dias)  
**Responsável:** Renato Abreu (CEO)  
**Arquiteto:** Cabral (AI Assistant)

---

**ESTE DOCUMENTO É A VERDADE. NADA DE INVENÇÃO.**  
**SE NÃO TÁ AQUI, NÃO EXISTE.**
