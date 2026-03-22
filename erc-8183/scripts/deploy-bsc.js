require("dotenv").config();
const { ethers } = require("hardhat");

async function main() {
  console.log("🚀 Deploying ERC-8183 Agentic Commerce Protocol (BSC)...");
  console.log("   Network: Binance Smart Chain");
  console.log("   Chain ID: 56");
  console.log("   Gas Token: BNB");
  console.log("");

  // Check balance
  const [deployer] = await ethers.getSigners();
  const balance = await ethers.provider.getBalance(deployer.address);
  console.log("📊 Deployer:", deployer.address);
  console.log("💰 Balance:", ethers.formatEther(balance), "BNB");
  console.log("");

  // ⚠️ VERIFICAÇÃO DE SEGURANÇA - GAS PRICE
  const feeData = await ethers.provider.getFeeData();
  const gasPrice = feeData.gasPrice || ethers.parseUnits("3", "gwei");
  console.log("⛽ Gas Price:", ethers.formatUnits(gasPrice, "gwei"), "Gwei");
  
  if (gasPrice > maxGasPrice) {
    console.log("🛑 GAS PRICE MUITO ALTO! (> 5 gwei)");
    console.log("   Abortando deploy. Aguarde rede menos congestionada.");
    process.exit(1);
  }
  console.log("✅ Gas price OK (< 5 gwei)");
  console.log("");

  if (balance === 0n) {
    console.log("❌ Insufficient BNB balance!");
    console.log("   Please transfer 0.1-0.2 BNB to this address");
    process.exit(1);
  }

  // Configurações
  const treasury = process.env.TREASURY_ADDRESS || "0x077e8d29e11ff1c0ccb236e0380d0053dcba2b1c";
  const platformFeeBps = process.env.PLATFORM_FEE_BPS || 10; // 0.1%
  const leveTokenAddress = process.env.LEVE_TOKEN_ADDRESS || "0x67e463AcC3B35406B0f35C8Ed531da89f9670861";

  // ⚠️ REGRAS DE SEGURANÇA - NÃO REMOVER
  const maxGasPrice = ethers.parseUnits("5", "gwei"); // Máximo 5 gwei
  const maxCostPerContract = ethers.parseEther("0.01"); // Máximo 0.01 BNB por contrato

  console.log("📋 Configuration:");
  console.log("   Treasury:", treasury);
  console.log("   Platform Fee:", platformFeeBps, "bps (", platformFeeBps / 100, "%)");
  console.log("   LEVE Token:", leveTokenAddress);
  console.log("");

  // Deploy ERC8183
  console.log("📦 Deploying ERC8183...");
  const ERC8183 = await ethers.getContractFactory("ERC8183");
  const acp = await ERC8183.deploy(treasury, platformFeeBps);
  await acp.waitForDeployment();

  const acpAddress = await acp.getAddress();
  const deployTx = await acp.deploymentTransaction();
  console.log("✅ ERC8183 deployed to:", acpAddress);
  console.log("📝 Transaction:", deployTx.hash);
  console.log("");

  // Deploy ReputationHook
  console.log("📦 Deploying ReputationHook...");
  const ReputationHook = await ethers.getContractFactory("ReputationHook");
  const repHook = await ReputationHook.deploy("0x0000000000000000000000000000000000000000");
  await repHook.waitForDeployment();

  const hookAddress = await repHook.getAddress();
  const hookTx = await repHook.deploymentTransaction();
  console.log("✅ ReputationHook deployed to:", hookAddress);
  console.log("📝 Transaction:", hookTx.hash);
  console.log("");

  // Deploy ERC-8126 (Risk Scoring)
  console.log("📦 Deploying ERC-8126 (Risk Scoring)...");
  const ERC8126 = await ethers.getContractFactory("ERC8126");
  const riskScoring = await ERC8126.deploy();
  await riskScoring.waitForDeployment();

  const riskAddress = await riskScoring.getAddress();
  const riskTx = await riskScoring.deploymentTransaction();
  console.log("✅ ERC-8126 deployed to:", riskAddress);
  console.log("📝 Transaction:", riskTx.hash);
  console.log("");

  // Deploy ERC-8021 (Attribution)
  console.log("📦 Deploying ERC-8021 (Attribution)...");
  const ERC8021 = await ethers.getContractFactory("ERC8021");
  const attribution = await ERC8021.deploy(platformFeeBps);
  await attribution.waitForDeployment();

  const attrAddress = await attribution.getAddress();
  const attrTx = await attribution.deploymentTransaction();
  console.log("✅ ERC-8021 deployed to:", attrAddress);
  console.log("📝 Transaction:", attrTx.hash);
  console.log("");

  // Deploy VestingGateIO (Gate.io Vesting)
  console.log("📦 Deploying VestingGateIO (Gate.io Vesting)...");
  const VestingGateIO = await ethers.getContractFactory("VestingGateIO");
  const vesting = await VestingGateIO.deploy(leveTokenAddress);
  await vesting.waitForDeployment();

  const vestingAddress = await vesting.getAddress();
  const vestingTx = await vesting.deploymentTransaction();
  console.log("✅ VestingGateIO deployed to:", vestingAddress);
  console.log("📝 Transaction:", vestingTx.hash);
  console.log("");

  // Salvar endereços
  const fs = require("fs");
  const addresses = {
    network: "bsc-mainnet",
    chainId: 56,
    ERC8183: acpAddress,
    ReputationHook: hookAddress,
    ERC8126_RiskScoring: riskAddress,
    ERC8021_Attribution: attrAddress,
    VestingGateIO: vestingAddress,
    LEVE_Token: leveTokenAddress,
    treasury: treasury,
    platformFeeBps: platformFeeBps,
    deployedAt: new Date().toISOString(),
    deployer: deployer.address,
  };

  fs.writeFileSync("./addresses-bsc.json", JSON.stringify(addresses, null, 2));
  console.log("💾 Addresses saved to addresses-bsc.json");
  console.log("");

  // Resumo
  console.log("📊 Deployment Summary:");
  console.log("   Network: BSC Mainnet (56)");
  console.log("   Treasury:", treasury);
  console.log("   Platform Fee:", platformFeeBps, "bps (", platformFeeBps / 100, "%)");
  console.log("   ERC-8183 (Commercial):", acpAddress);
  console.log("   ReputationHook (ERC-8004):", hookAddress);
  console.log("   ERC-8126 (Risk Scoring):", riskAddress);
  console.log("   ERC-8021 (Attribution):", attrAddress);
  console.log("   VestingGateIO (Gate.io):", vestingAddress);
  console.log("   LEVE Token:", leveTokenAddress);
  console.log("");
  console.log("🔗 View on BSCScan:");
  console.log("   ERC-8183: https://bscscan.com/address/" + acpAddress);
  console.log("   ReputationHook: https://bscscan.com/address/" + hookAddress);
  console.log("   ERC-8126: https://bscscan.com/address/" + riskAddress);
  console.log("   ERC-8021: https://bscscan.com/address/" + attrAddress);
  console.log("   VestingGateIO: https://bscscan.com/address/" + vestingAddress);
  console.log("");
  console.log("🎉 ALL CONTRACTS DEPLOYED SUCCESSFULLY!");
  console.log("🎉 ECOSSISTEMA LEVE IA 100% COMPLETO NA BSC!");
  console.log("🎉 VESTING GATE.IO IMPLEMENTADO!");
  console.log("🎉 53+ HOLDERS PODEM SER ADICIONADOS AO VESTING!");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
