# 🎯 VESTING GATE.IO - GUIA COMPLETO

**Data:** 2026-03-10  
**Rede:** BSC (BEP-20)  
**Status:** ✅ DEPLOYADO

---

## 📍 **CONTRATO VESTING GATE.IO**

```
Endereço: 0xDc64a140Aa3E981100a9becA4E685f962f0cF6C9
Token: LEVE (0x67e463AcC3B35406B0f35C8Ed531da89f9670861)
BSCScan: https://bscscan.com/address/0xDc64a140Aa3E981100a9becA4E685f962f0cF6C9
TX: 0x66e2a2ee818d22c4edae5eee62ca63ccccd04e4db1ae1be7f0f01d247f60e67f
```

---

## 🎯 **O QUE É ESTE CONTRATO:**

```
Vesting Gate.IO = Contrato para bloquear tokens dos 53+ holders
                  Liberação gradual APÓS listagem na Gate.io
                  Anti-dump protection
```

---

## 💡 **COMO FUNCIONA:**

### **Fluxo:**

```
1. Owner (Renato) adiciona holders ao vesting
   ↓
2. Tokens TRANSFERIDOS para o contrato
   ↓
3. Tokens BLOQUEADOS até Gate.io listing
   ↓
4. Gate.io listing → Owner marca como "listed"
   ↓
5. TGE Release: 20% liberado na listagem
   ↓
6. Pós-TGE: 20% por mês (5 meses total)
   ↓
7. Holders claimam tokens liberados
```

---

## 📊 **CONFIGURAÇÃO PADRÃO:**

| Parâmetro | Valor | Explicação |
|-----------|-------|------------|
| **TGE Release** | 20% | Liberado na listagem |
| **Cliff** | 0 dias | Sem período de espera |
| **Vesting** | 150 dias | 5 meses de liberação |
| **Liberação** | 20%/mês | Linear após TGE |
| **Total** | 100% | 5 meses |

---

## 🔧 **COMO ADICIONAR HOLDERS:**

### **Passo 1: Aprovar Tokens**

```javascript
// Owner precisa aprovar tokens primeiro
const token = await ethers.getContractAt("IERC20", "0x67e463AcC3B35406B0f35C8Ed531da89f9670861");
await token.approve("0xDc64a140Aa3E981100a9becA4E685f962f0cF6C9", amount);
```

### **Passo 2: Criar Vesting Schedule**

```javascript
const vesting = await ethers.getContractAt("VestingGateIO", "0xDc64a140Aa3E981100a9becA4E685f962f0cF6C9");

await vesting.createVestingSchedule(
  beneficiary,    // Endereço do holder
  totalAmount,    // Quantidade de tokens (em wei)
  cliffDuration,  // 0 (sem cliff)
  vestingDuration,// 150 days = 12960000 seconds
  tgePercentage   // 2000 = 20%
);
```

### **Exemplo Prático:**

```javascript
// Adicionar holder com 100,000 LEVE tokens
const holder = "0x..."; // Endereço do holder
const amount = ethers.parseUnits("100000", 18); // 100k LEVE (18 decimals)
const cliff = 0; // Sem cliff
const vesting = 150 * 24 * 60 * 60; // 150 dias em segundos
const tge = 2000; // 20% (2000/10000)

await vesting.createVestingSchedule(holder, amount, cliff, vesting, tge);
```

---

## 📋 **PARA ADICIONAR OS 53+ HOLDERS:**

### **Script de Batch:**

```javascript
const holders = [
  { address: "0x...", amount: "100000" },
  { address: "0x...", amount: "50000" },
  // ... adicionar todos 53+ holders
];

for (const holder of holders) {
  const amount = ethers.parseUnits(holder.amount, 18);
  await vesting.createVestingSchedule(
    holder.address,
    amount,
    0,
    150 * 24 * 60 * 60,
    2000
  );
  console.log("Added:", holder.address);
}
```

---

## 🎯 **QUANDO USAR ESTE CONTRATO:**

### **Cenário 1: Gate.io Exige Vesting**

```
Gate.io diz: "Todos holders precisam estar em vesting"
✅ Você usa este contrato
✅ Adiciona 53+ holders
✅ Gate.io lista
```

### **Cenário 2: Anti-Dump Protection**

```
Você quer: "Evitar dump de 53+ holders na listagem"
✅ Você usa este contrato
✅ Tokens bloqueados
✅ Apenas 20% liberado no TGE
✅ Preço estável
```

### **Cenário 3: Opcional**

```
Gate.io NÃO exige vesting para holders existentes
✅ Você NÃO usa este contrato
✅ Deixa holders como estão
✅ Só usa para NOVA pré-venda
```

---

## 🔍 **FUNÇÕES DO CONTRATO:**

### **Owner Functions:**

```solidity
// Criar vesting schedule
createVestingSchedule(beneficiary, amount, cliff, duration, tge%)

// Marcar Gate.io como listado
setGateIOListed()

// Bloquear schedule (não modificável)
lockForGateIO(beneficiary)

// Emergency withdrawal
emergencyWithdraw(tokenAddress, amount)
```

### **Holder Functions:**

```solidity
// Claim tokens liberados
release()

// Verificar detalhes
getVestingDetails(beneficiary)
```

### **View Functions:**

```solidity
// Calcular tokens liberáveis
calculateReleasable(beneficiary)

// Obter todos beneficiários
getAllBeneficiaries()

// Número de beneficiários
getBeneficiaryCount()

// Saldo de tokens do contrato
getTokenBalance()
```

---

## 📊 **EXEMPLO DE VESTING:**

### **Holder: 100,000 LEVE**

| Mês | Liberação | Acumulado | Saldo Bloqueado |
|-----|-----------|-----------|-----------------|
| **TGE (Listagem)** | 20,000 (20%) | 20,000 | 80,000 |
| **Mês 1** | 20,000 (20%) | 40,000 | 60,000 |
| **Mês 2** | 20,000 (20%) | 60,000 | 40,000 |
| **Mês 3** | 20,000 (20%) | 80,000 | 20,000 |
| **Mês 4** | 20,000 (20%) | 100,000 | 0 |

**Total:** 5 meses de vesting

---

## 💬 **DECISÃO: USAR OU NÃO USAR?**

### **✅ USAR ESTE CONTRATO SE:**

- [ ] Gate.io EXIGIR vesting para holders existentes
- [ ] Você quer anti-dump protection
- [ ] 53+ holders concordam com vesting
- [ ] Quer alinhar interesses de longo prazo

### **❌ NÃO USAR SE:**

- [ ] Gate.io NÃO exige vesting
- [ ] 53+ holders NÃO aceitam vesting
- [ ] Tokens já foram vendidos/liberados
- [ ] São early supporters com tokens já liberados

---

## 🎯 **MINHA RECOMENDAÇÃO:**

> **"Renato, este contrato está PRONTO mas é OPCIONAL.**
>
> *Use se:*
> - *Gate.io exigir vesting para 53+ holders*
> - *Você quiser anti-dump protection extra*
>
> *Não use se:*
> - *Gate.io não exigir*
> - *Holders já têm tokens liberados*
>
> *O contrato já está deployado:*
> - *0xDc64a140Aa3E981100a9becA4E685f962f0cF6C9*
>
> *Só usar se precisar!"*

---

## 🔗 **LINKS:**

| Recurso | Link |
|---------|------|
| **Contrato Vesting** | https://bscscan.com/address/0xDc64a140Aa3E981100a9becA4E685f962f0cF6C9 |
| **Token LEVE** | https://bscscan.com/token/0x67e463AcC3B35406B0f35C8Ed531da89f9670861 |
| **Vesting Existente** | https://bscscan.com/address/0xD8E4226eD752fCc7488410C6d34f73007FD66059 |

---

**Contrato Vesting Gate.IO deployado e pronto para uso!** 🎉
