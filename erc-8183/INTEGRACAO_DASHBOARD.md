# 🔗 INTEGRAÇÃO DOS CONTRATOS NO DASHBOARD

**Data:** 2026-03-11  
**Status:** ✅ Pronto para integrar após deploy

---

## 📋 ENDEREÇOS PARA ATUALIZAR

### **Após o deploy, atualizar:**

**Arquivo:** `/root/openclaw/leveia-dashboard/src/App.jsx`

```javascript
const CONTRACTS = {
  ERC8183: "0x...",           // Substituir após deploy
  ERC8126: "0x...",            // Substituir após deploy
  ERC8021: "0x...",            // Substituir após deploy
  ReputationHook_v2: "0x...",  // Substituir após deploy
  VestingGateIO: "0x...",      // Substituir após deploy
  Token_LEVE: "0x67e463AcC3B35406B0f35C8Ed531da89f9670861" // Já existe
};
```

---

## 🎯 COMPONENTES PARA CRIAR

### **1. ContractList.jsx** (JÁ EXISTE)

**Local:** `/root/openclaw/leveia-dashboard/src/components/ContractList.jsx`

**O que faz:**
- Lista todos os 5 contratos
- Mostra endereço de cada um
- Link para BSCScan
- Botão de copiar

**Status:** ✅ Já criado

---

### **2. ContractDetails.jsx** (NOVO)

**Local:** `/root/openclaw/leveia-dashboard/src/components/ContractDetails.jsx`

**O que faz:**
- Mostra detalhes de cada contrato
- Funções públicas disponíveis
- Eventos emitidos
- Histórico de transações

**Status:** ⏳ Pendente (criar após deploy)

---

### **3. ContractInteraction.jsx** (NOVO)

**Local:** `/root/openclaw/leveia-dashboard/src/components/ContractInteraction.jsx`

**O que faz:**
- Permite interagir com contratos
- Chamar funções públicas
- Ver resultados em tempo real

**Status:** ⏳ Pendente (criar após deploy)

---

## 📊 FLUXO DE INTEGRAÇÃO

### **Após Deploy:**

```
1. Deploy dos contratos
   ↓
2. Pegar endereços do deploy
   ↓
3. Atualizar App.jsx com endereços
   ↓
4. Atualizar ContractList.jsx
   ↓
5. Testar no dashboard
   ↓
6. Build e deploy do dashboard
```

---

## 🔧 COMANDO PARA ATUALIZAR

**Após receber endereços do deploy:**

```bash
# 1. Editar App.jsx
nano /root/openclaw/leveia-dashboard/src/App.jsx

# 2. Atualizar CONTRACTS com endereços reais

# 3. Build
cd /root/openclaw/leveia-dashboard
npm run build

# 4. Deploy
cp -r dist/* /var/www/leveia-dashboard/
```

---

## 📝 EXEMPLO DE ATUALIZAÇÃO

**Antes:**
```javascript
const CONTRACTS = {
  ERC8183: "0x0000000000000000000000000000000000000000",
  // ...
};
```

**Depois:**
```javascript
const CONTRACTS = {
  ERC8183: "0x5FbDB2315678afecb367f032d93F642f64180aa3",
  // ...
};
```

---

## ✅ CHECKLIST DE INTEGRAÇÃO

- [ ] Receber endereços do deploy
- [ ] Atualizar App.jsx
- [ ] Atualizar ContractList.jsx
- [ ] Testar localmente
- [ ] Build do dashboard
- [ ] Deploy do dashboard
- [ ] Verificar no ar

---

## 🚀 PRÓXIMOS PASSOS

1. **Aguardar deploy dos contratos**
2. **Receber endereços**
3. **Atualizar dashboard**
4. **Testar integração**
5. **Fazer deploy do dashboard atualizado**

---

**Status:** ✅ PRONTO PARA INTEGRAR  
**Aguardando:** Endereços dos contratos após deploy
