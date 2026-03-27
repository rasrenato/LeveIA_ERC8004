const hre = require("hardhat");

async function main() {
  console.log("Iniciando o deploy do LeveIA_AuditRegistry na rede Base...");

  const LeveIA_AuditRegistry = await hre.ethers.getContractFactory("contracts/LeveIA_AuditRegistry_Final.sol:LeveIA_AuditRegistry");
  const contract = await LeveIA_AuditRegistry.deploy();

  await contract.waitForDeployment();

  const address = await contract.getAddress();

  console.log("LeveIA_AuditRegistry implantado com sucesso!");
  console.log("Endereço do Contrato:", address);

  console.log("Aguardando confirmações da rede para verificação...");
  // Aguarda 30 segundos antes de verificar
  await new Promise(resolve => setTimeout(resolve, 30000));

  try {
    await hre.run("verify:verify", {
      address: address,
      constructorArguments: [],
    });
    console.log("Contrato verificado com sucesso no BaseScan!");
  } catch (error) {
    console.log("Erro na verificação automática:", error.message);
    console.log("Você pode verificar manualmente no BaseScan usando o endereço acima.");
  }
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
