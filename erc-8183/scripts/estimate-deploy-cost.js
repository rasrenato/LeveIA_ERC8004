/**
 * Script de Estimativa de Custo de Deploy
 * USO OBRIGATÓRIO ANTES DE QUALQUER DEPLOY
 * 
 * Como usar:
 *   npx hardhat run scripts/estimate-deploy-cost.js --network bsc
 */

require("dotenv").config();
const { ethers } = require("hardhat");

async function main() {
  console.log("=".repeat(60));
  console.log("📊 ESTIMATIVA DE CUSTO DE DEPLOY - BSC");
  console.log("=".repeat(60));
  console.log("");

  // 1. Obter gas price atual da rede
  const feeData = await ethers.provider.getFeeData();
  const gasPrice = feeData.gasPrice;
  const gasPriceGwei = ethers.formatUnits(gasPrice, "gwei");
  
  console.log("⛽ GAS PRICE ATUAL:");
  console.log(`   ${gasPriceGwei} Gwei`);
  console.log(`   ${ethers.formatUnits(gasPrice, "ether")} BNB`);
  console.log("");

  // 2. Preço do BNB em USD (Binance API)
  try {
    const response = await fetch('https://api.binance.com/api/v3/ticker/price?symbol=BNBUSDT');
    const data = await response.json();
    const bnbPrice = parseFloat(data.price);
    
    console.log("💰 PREÇO DO BNB:");
    console.log(`   $${bnbPrice.toFixed(2)} USD`);
    console.log("");
  } catch (e) {
    console.log("💰 PREÇO DO BNB: Não foi possível obter");
    console.log("");
  }

  // 3. Estimar gas para cada contrato
  const contracts = [
    { name: "ERC8183", file: "ERC8183", args: ["0x077e8d29e11ff1c0ccb236e0380d0053dcba2b1c", 10] },
    { name: "ReputationHook", file: "ReputationHook", args: ["0x0000000000000000000000000000000000000000"] },
    { name: "ERC-8126 (Risk Scoring)", file: "ERC8126", args: [] },
    { name: "ERC-8021 (Attribution)", file: "ERC8021", args: [10] }
  ];

  console.log("📦 ESTIMATIVA POR CONTRATO:");
  console.log("-".repeat(60));

  let totalGas = 0n;

  for (const contract of contracts) {
    try {
      const Factory = await ethers.getContractFactory(contract.file);
      
      // Simular deploy (sem executar)
      const deployTx = await Factory.getDeployTransaction(...contract.args);
      
      // Estimar gas
      const estimatedGas = await ethers.provider.estimateGas({
        to: deployTx.to,
        data: deployTx.data,
        from: (await ethers.getSigners())[0].address
      });

      totalGas += estimatedGas;

      const costBNB = ethers.formatEther(estimatedGas * gasPrice);
      const costUSD = parseFloat(costBNB) * 650; // Preço aproximado

      console.log("");
      console.log(`   ${contract.name}:`);
      console.log(`      Gas: ${estimatedGas.toLocaleString()}`);
      console.log(`      Custo: ${costBNB} BNB (~$${costUSD.toFixed(2)} USD)`);
    } catch (error) {
      console.log("");
      console.log(`   ${contract.name}: ⚠️ Erro ao estimar`);
      console.log(`      ${error.message}`);
    }
  }

  console.log("");
  console.log("-".repeat(60));
  console.log("📊 TOTAL GERAL:");
  console.log("-".repeat(60));
  
  const totalBNB = ethers.formatEther(totalGas * gasPrice);
  const totalUSD = parseFloat(totalBNB) * 650;

  console.log(`   Gas Total: ${totalGas.toLocaleString()}`);
  console.log(`   Custo Total: ${totalBNB} BNB`);
  console.log(`   Custo Total: ~$${totalUSD.toFixed(2)} USD`);
  console.log("");

  // 4. Verificar saldo da wallet
  const [deployer] = await ethers.getSigners();
  const balance = await ethers.provider.getBalance(deployer.address);
  const balanceBNB = ethers.formatEther(balance);
  const balanceUSD = parseFloat(balanceBNB) * 650;

  console.log("💳 SALDO DA WALLET:");
  console.log(`   Endereço: ${deployer.address}`);
  console.log(`   Saldo: ${balanceBNB} BNB (~$${balanceUSD.toFixed(2)} USD)`);
  console.log("");

  // 5. Verificação de segurança
  console.log("🛡️ VERIFICAÇÃO DE SEGURANÇA:");
  console.log("-".repeat(60));

  const minBalance = totalGas * gasPrice * 110n / 100n; // 10% de margem
  const hasEnough = balance >= minBalance;

  if (hasEnough) {
    console.log("   ✅ SALDO SUFICIENTE");
    console.log(`   ✅ Sobra estimada: ${ethers.formatEther(balance - minBalance)} BNB`);
  } else {
    console.log("   ❌ SALDO INSUFICIENTE");
    const needed = minBalance - balance;
    console.log(`   ❌ Faltam: ${ethers.formatEther(needed)} BNB (~$${(parseFloat(ethers.formatEther(needed)) * 650).toFixed(2)} USD)`);
  }

  console.log("");
  console.log("⚠️ REGRAS DE SEGURANÇA:");
  console.log("-".repeat(60));
  
  const gasPriceLimit = ethers.parseUnits("5", "gwei");
  const costLimit = ethers.parseEther("0.01"); // 0.01 BNB por contrato

  if (gasPrice > gasPriceLimit) {
    console.log("   🛑 GAS PRICE MUITO ALTO (> 5 gwei)");
    console.log("   🛑 RECOMENDAÇÃO: Aguardar rede menos congestionada");
  } else {
    console.log("   ✅ Gas price dentro do limite (< 5 gwei)");
  }

  console.log("");
  console.log("=".repeat(60));
  console.log("📋 PRÓXIMOS PASSOS:");
  console.log("=".repeat(60));
  console.log("");
  console.log("1. Verifique se o saldo está correto");
  console.log("2. Confirme que os valores fazem sentido");
  console.log("3. SÓ ENTÃO execute o deploy com:");
  console.log("   npx hardhat run scripts/deploy-bsc.js --network bsc");
  console.log("");
  console.log("⚠️ NUNCA execute deploy sem rodar este script antes!");
  console.log("");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
