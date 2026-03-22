const hre = require("hardhat");

async function main() {
  const TREASURY_ADDRESS = "0x4474Ad931757466B401ABE0B93445E8cB21ddCc6";
  
  console.log("🚀 Deploying PaymentSplitter na BSC Mainnet...");
  console.log(`📦 Treasury: ${TREASURY_ADDRESS}`);
  
  // Verificar saldo da wallet
  const [deployer] = await hre.ethers.getSigners();
  const balance = await hre.ethers.provider.getBalance(deployer.address);
  console.log(`💰 Deployer: ${deployer.address}`);
  console.log(`💰 Saldo: ${hre.ethers.formatEther(balance)} BNB`);
  
  if (balance === 0n) {
    console.error("❌ ERRO: Wallet sem BNB para gas!");
    console.error("⚠️  Transfira BNB para:", deployer.address);
    process.exit(1);
  }
  
  const PaymentSplitter = await hre.ethers.getContractFactory("PaymentSplitter");
  console.log("\n📝 Compilando e deployando...");
  
  const splitter = await PaymentSplitter.deploy(TREASURY_ADDRESS);
  
  console.log("⏳ Aguardando confirmação do deploy...");
  await splitter.waitForDeployment();
  
  const address = await splitter.getAddress();
  const deploymentTx = splitter.deploymentTransaction();
  
  console.log("\n" + "=".repeat(60));
  console.log("✅ PaymentSplitter DEPLOYADO COM SUCESSO!");
  console.log("=".repeat(60));
  console.log(`📍 Endereço: ${address}`);
  console.log(`🔗 BscScan: https://bscscan.com/address/${address}`);
  console.log(`📄 TX: https://bscscan.com/tx/${deploymentTx.hash}`);
  console.log(`👤 Owner: ${deployer.address}`);
  console.log(`🏦 Treasury: ${TREASURY_ADDRESS}`);
  console.log("=".repeat(60));
  
  // Salvar endereço
  const fs = require("fs");
  const path = require("path");
  
  const addressesPath = path.join(__dirname, "..", "addresses-bsc.json");
  let addresses = {};
  
  if (fs.existsSync(addressesPath)) {
    addresses = JSON.parse(fs.readFileSync(addressesPath, "utf8"));
  }
  
  addresses.PaymentSplitter = address;
  addresses.treasury = TREASURY_ADDRESS;
  addresses.deployedAt = new Date().toISOString();
  
  fs.writeFileSync(addressesPath, JSON.stringify(addresses, null, 2));
  
  console.log("\n📝 Endereço salvo em addresses-bsc.json");
  
  // Instruções de verificação
  console.log("\n" + "=".repeat(60));
  console.log("📋 PARA VERIFICAR NO BSCSCAN:");
  console.log("=".repeat(60));
  console.log(`npx hardhat verify --network bsc ${address} ${TREASURY_ADDRESS}`);
  console.log("\nOu acesse: https://bscscan.com/address/");
  console.log("e clique em 'Verify and Publish'");
  console.log("=".repeat(60));
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
