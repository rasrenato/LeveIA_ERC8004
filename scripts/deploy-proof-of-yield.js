const hre = require("hardhat");

/**
 * Deploy ProofOfYield na Base Network
 * Wallet: Renato (0x077e8d29e11ff1c0ccb236e0380d0053dcba2b1c)
 */

async function main() {
  console.log("🚀 Deploy ProofOfYield - Leve IA");
  console.log("================================\n");

  // Wallet do Renato
  const privateKey = "0xf091abca2de925b91546b09e0fe6e8f970322a1ffd34d159c2851c5c77901dfa";
  
  console.log("📡 Conectando na Base Network...");
  const [deployer] = await hre.ethers.getSigners();
  
  console.log(`   Deployer: ${deployer.address}`);
  
  // Verificar saldo
  const balance = await hre.ethers.provider.getBalance(deployer.address);
  console.log(`   Saldo: ${hre.ethers.formatEther(balance)} ETH`);
  
  if (balance === 0n) {
    console.log("❌ ERRO: Saldo zero!");
    return;
  }

  // Deploy do contrato
  console.log("\n📄 Deploy ProofOfYield...");
  
  const ProofOfYield = await hre.ethers.getContractFactory("ProofOfYield");
  const proofOfYield = await ProofOfYield.deploy();
  
  await proofOfYield.waitForDeployment();
  
  const contractAddress = await proofOfYield.getAddress();
  const deployTx = proofOfYield.deploymentTransaction();
  
  console.log("\n✅ DEPLOY CONCLUÍDO!");
  console.log("==================");
  console.log(`Contract: ${contractAddress}`);
  console.log(`Deployer: ${deployer.address}`);
  console.log(`Tx Hash: ${deployTx.hash}`);
  console.log(`Explorer: https://basescan.org/address/${contractAddress}`);
  console.log(`Tx: https://basescan.org/tx/${deployTx.hash}`);
  
  // Salvar endereço no .env
  console.log("\n💾 Salvando endereço...");
  const fs = require("fs");
  const envPath = "/root/openclaw/.env.blockchain";
  let envContent = fs.existsSync(envPath) ? fs.readFileSync(envPath, "utf8") : "";
  
  if (envContent.includes("PROOF_OF_YIELD_ADDRESS")) {
    envContent = envContent.replace(/PROOF_OF_YIELD_ADDRESS=.*/, `PROOF_OF_YIELD_ADDRESS=${contractAddress}`);
  } else {
    envContent += `\nPROOF_OF_YIELD_ADDRESS=${contractAddress}\n`;
  }
  
  fs.writeFileSync(envPath, envContent);
  console.log("   Endereço salvo em .env.blockchain");
  
  console.log("\n🎉 Próximo: Integrar com alpha_signals_v3.py");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
