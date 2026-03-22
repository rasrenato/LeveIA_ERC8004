const hre = require("hardhat");

async function main() {
  console.log("🚀 Deploying ERC-8183 Agentic Commerce Protocol...");

  // Configurações
  const treasury = "0x077e8d29e11ff1c0ccb236e0380d0053dcba2b1c"; // Renato wallet
  const platformFeeBps = 10; // 0.1% (10 basis points)

  // Deploy ERC8183
  const ERC8183 = await hre.ethers.getContractFactory("ERC8183");
  console.log("📦 Deploying ERC8183...");
  const acp = await ERC8183.deploy(treasury, platformFeeBps);
  await acp.waitForDeployment();

  const acpAddress = await acp.getAddress();
  console.log("✅ ERC8183 deployed to:", acpAddress);

  // Deploy ReputationHook
  const ReputationHook = await hre.ethers.getContractFactory("ReputationHook");
  console.log("📦 Deploying ReputationHook...");
  const repHook = await ReputationHook.deploy("0x0000000000000000000000000000000000000000");
  await repHook.waitForDeployment();

  const hookAddress = await repHook.getAddress();
  console.log("✅ ReputationHook deployed to:", hookAddress);

  // Verificar no BaseScan
  console.log("\n📝 Verify on BaseScan:");
  console.log(`npx hardhat verify --network ${hre.network.name} ${acpAddress} ${treasury} ${platformFeeBps}`);
  console.log(`npx hardhat verify --network ${hre.network.name} ${hookAddress} 0x0000000000000000000000000000000000000000`);

  // Salvar endereços
  const fs = require("fs");
  const addresses = {
    network: hre.network.name,
    ERC8183: acpAddress,
    ReputationHook: hookAddress,
    treasury: treasury,
    platformFeeBps: platformFeeBps,
    deployedAt: new Date().toISOString(),
  };

  fs.writeFileSync(
    "./addresses.json",
    JSON.stringify(addresses, null, 2)
  );
  console.log("\n💾 Addresses saved to addresses.json");

  // Resumo
  console.log("\n📊 Deployment Summary:");
  console.log("  Network:", hre.network.name);
  console.log("  Treasury:", treasury);
  console.log("  Platform Fee:", platformFeeBps, "bps (", platformFeeBps / 100, "%)");
  console.log("  ERC8183:", acpAddress);
  console.log("  ReputationHook:", hookAddress);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
