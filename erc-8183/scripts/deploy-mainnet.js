require("dotenv").config();
const { ethers } = require("hardhat");

async function main() {
  console.log("🚀 Deploying ERC-8183 Agentic Commerce Protocol (Base Mainnet)...");

  // Check balance
  const [deployer] = await ethers.getSigners();
  const balance = await ethers.provider.getBalance(deployer.address);
  console.log("📊 Deployer:", deployer.address);
  console.log("💰 Balance:", ethers.formatEther(balance), "ETH");

  if (balance === 0n) {
    console.log("❌ Insufficient funds!");
    process.exit(1);
  }

  // Configurações
  const treasury = "0x077e8d29e11ff1c0ccb236e0380d0053dcba2b1c"; // Renato wallet
  const platformFeeBps = 10; // 0.1% (10 basis points)

  // Deploy ERC8183
  console.log("\n📦 Deploying ERC8183...");
  const ERC8183 = await ethers.getContractFactory("ERC8183");
  const acp = await ERC8183.deploy(treasury, platformFeeBps);
  await acp.waitForDeployment();

  const acpAddress = await acp.getAddress();
  const deployTx = await acp.deploymentTransaction();
  console.log("✅ ERC8183 deployed to:", acpAddress);
  console.log("📝 Transaction:", deployTx.hash);

  // Deploy ReputationHook
  console.log("\n📦 Deploying ReputationHook...");
  const ReputationHook = await ethers.getContractFactory("ReputationHook");
  const repHook = await ReputationHook.deploy("0x0000000000000000000000000000000000000000");
  await repHook.waitForDeployment();

  const hookAddress = await repHook.getAddress();
  const hookTx = await repHook.deploymentTransaction();
  console.log("✅ ReputationHook deployed to:", hookAddress);
  console.log("📝 Transaction:", hookTx.hash);

  // Salvar endereços
  const fs = require("fs");
  const addresses = {
    network: "base-mainnet",
    chainId: 8453,
    ERC8183: acpAddress,
    ReputationHook: hookAddress,
    treasury: treasury,
    platformFeeBps: platformFeeBps,
    deployedAt: new Date().toISOString(),
    deployer: deployer.address,
  };

  fs.writeFileSync("./addresses.json", JSON.stringify(addresses, null, 2));
  console.log("\n💾 Addresses saved to addresses.json");

  // Resumo
  console.log("\n📊 Deployment Summary:");
  console.log("  Network: Base Mainnet (8453)");
  console.log("  Treasury:", treasury);
  console.log("  Platform Fee:", platformFeeBps, "bps (", platformFeeBps / 100, "%)");
  console.log("  ERC8183:", acpAddress);
  console.log("  ReputationHook:", hookAddress);
  console.log("\n🔗 View on BaseScan:");
  console.log("  https://basescan.org/address/" + acpAddress);
  console.log("  https://basescan.org/address/" + hookAddress);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
