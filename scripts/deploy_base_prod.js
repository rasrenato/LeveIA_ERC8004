const hre = require("hardhat");

async function main() {
  console.log("=== DEPLOY NA BASE MAINNET ===");
  console.log("");
  console.log("Iniciando o deploy do LeveIA_AuditRegistry na rede Base...");
  console.log("Rede: Base Mainnet (Chain ID 8453)");
  console.log("");

  const LeveIA_AuditRegistry = await hre.ethers.getContractFactory("contracts/LeveIA_AuditRegistry_Final.sol:LeveIA_AuditRegistry");
  const contract = await LeveIA_AuditRegistry.deploy();

  console.log("📤 Enviando transação de deploy...");
  await contract.waitForDeployment();

  const address = await contract.getAddress();
  const deploymentTx = contract.deploymentTransaction();

  console.log("");
  console.log("✅ LeveIA_AuditRegistry implantado com sucesso!");
  console.log("");
  console.log("📋 DADOS DO DEPLOY:");
  console.log("Endereço do Contrato:", address);
  console.log("Transação:", deploymentTx.hash);
  console.log("Block:", deploymentTx.blockNumber);
  console.log("");
  console.log("🔗 BASESCAN:");
  console.log(`https://basescan.org/address/${address}`);
  console.log(`https://basescan.org/tx/${deploymentTx.hash}`);
  console.log("");
  console.log("⏳ Aguardando 30 segundos para verificação...");
  await new Promise(resolve => setTimeout(resolve, 30000));

  try {
    await hre.run("verify:verify", {
      address: address,
      constructorArguments: [],
    });
    console.log("✅ Contrato verificado com sucesso no BaseScan!");
  } catch (error) {
    console.log("⚠️  Erro na verificação automática:", error.message);
    console.log("Você pode verificar manualmente no BaseScan.");
  }
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
