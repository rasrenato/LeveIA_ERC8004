const hre = require("hardhat");

async function main() {
  console.log("🚀 Deploy de Todos os Contratos - Leve IA\n");
  console.log("📋 ORDEM CORRETA DE DEPLOY:\n");
  
  // Configurações
  const treasury = "0x077e8d29e11ff1c0ccb236e0380d0053dcba2b1c";
  const leveToken = "0x67e463AcC3B35406B0f35C8Ed531da89f9670861";
  const platformFeeBps = 10; // 0.1%
  const usdtAddress = "0x55d398326f99059fF775485246999027B3197955"; // USDT na BSC
  const wbnbAddress = "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c"; // WBNB na BSC
  
  const deployedContracts = {};
  
  try {
    // ============================================================
    // ORDEM 1: ERC8183 (Commercial Layer)
    // ============================================================
    // NÃO DEPENDE DE NINGUÉM - PODE SER DEPLOYADO PRIMEIRO
    // Aceita múltiplos tokens: USDT, WBNB, LEVE
    console.log("📦 1/5 - Deploy ERC8183 (Commercial Layer)...");
    console.log("   ├── Tokens aceitos: USDT, WBNB, LEVE");
    console.log("   └── Treasury:", treasury);
    const ERC8183 = await hre.ethers.getContractFactory("ERC8183");
    const erc8183 = await ERC8183.deploy(treasury, platformFeeBps);
    await erc8183.waitForDeployment();
    const erc8183Address = await erc8183.getAddress();
    deployedContracts.ERC8183 = erc8183Address;
    console.log(`   ✅ ERC8183: ${erc8183Address}\n`);
    
    // ============================================================
    // ORDEM 2: ERC8126 (Risk Scoring)
    // ============================================================
    // NÃO DEPENDE DE NINGUÉM - INDEPENDENTE
    console.log("📦 2/5 - Deploy ERC8126 (Risk Scoring)...");
    console.log("   └── Score: 0-1000");
    const ERC8126 = await hre.ethers.getContractFactory("ERC8126");
    const erc8126 = await ERC8126.deploy();
    await erc8126.waitForDeployment();
    const erc8126Address = await erc8126.getAddress();
    deployedContracts.ERC8126 = erc8126Address;
    console.log(`   ✅ ERC8126: ${erc8126Address}\n`);
    
    // ============================================================
    // ORDEM 3: ERC8021 (Attribution)
    // ============================================================
    // NÃO DEPENDE DE NINGUÉM - INDEPENDENTE
    console.log("📦 3/5 - Deploy ERC8021 (Attribution)...");
    console.log("   └── Revenue sharing");
    const ERC8021 = await hre.ethers.getContractFactory("ERC8021");
    const erc8021 = await ERC8021.deploy();
    await erc8021.waitForDeployment();
    const erc8021Address = await erc8021.getAddress();
    deployedContracts.ERC8021 = erc8021Address;
    console.log(`   ✅ ERC8021: ${erc8021Address}\n`);
    
    // ============================================================
    // ORDEM 4: ReputationHook_v2
    // ============================================================
    // DEPENDE DO ERC8183 - PRECISA SABER O ENDEREÇO
    console.log("📦 4/5 - Deploy ReputationHook_v2...");
    console.log("   ├── Depende de: ERC8183");
    console.log("   └── ERC8183:", erc8183Address);
    const ReputationHook = await hre.ethers.getContractFactory("ReputationHook_v2");
    const reputationHook = await ReputationHook.deploy(
      "0x0000000000000000000000000000000000000000", // erc8004Registry (opcional)
      erc8183Address // erc8183 (OBRIGATÓRIO)
    );
    await reputationHook.waitForDeployment();
    const reputationHookAddress = await reputationHook.getAddress();
    deployedContracts.ReputationHook_v2 = reputationHookAddress;
    console.log(`   ✅ ReputationHook_v2: ${reputationHookAddress}\n`);
    
    // ============================================================
    // ORDEM 5: VestingGateIO
    // ============================================================
    // DEPENDE DO TOKEN LEVE - JÁ EXISTE NA BSC
    console.log("📦 5/5 - Deploy VestingGateIO...");
    console.log("   ├── Depende de: Token LEVE");
    console.log("   └── Token LEVE:", leveToken);
    const VestingGateIO = await hre.ethers.getContractFactory("VestingGateIO");
    const vestingGateIO = await VestingGateIO.deploy(leveToken);
    await vestingGateIO.waitForDeployment();
    const vestingGateIOAddress = await vestingGateIO.getAddress();
    deployedContracts.VestingGateIO = vestingGateIOAddress;
    console.log(`   ✅ VestingGateIO: ${vestingGateIOAddress}\n`);
    
    // ============================================================
    // SALVAR ENDEREÇOS
    // ============================================================
    const fs = require("fs");
    const addressesPath = "./addresses-bsc.json";
    let addresses = {};
    
    if (fs.existsSync(addressesPath)) {
      addresses = JSON.parse(fs.readFileSync(addressesPath, "utf8"));
    }
    
    // Atualizar com novos endereços
    addresses.ERC8183 = erc8183Address;
    addresses.ERC8126_RiskScoring = erc8126Address;
    addresses.ERC8021_Attribution = erc8021Address;
    addresses.ReputationHook_v2 = reputationHookAddress;
    addresses.VestingGateIO = vestingGateIOAddress;
    addresses.deployedAt = new Date().toISOString();
    addresses.deployOrder = [
      "ERC8183",
      "ERC8126",
      "ERC8021",
      "ReputationHook_v2",
      "VestingGateIO"
    ];
    addresses.supportedTokens = {
      USDT: usdtAddress,
      WBNB: wbnbAddress,
      LEVE: leveToken
    };
    
    fs.writeFileSync(addressesPath, JSON.stringify(addresses, null, 2));
    
    console.log("✅ Todos os contratos deployados com sucesso!\n");
    console.log("📝 Endereços salvos em addresses-bsc.json\n");
    
    console.log("=== RESUMO FINAL ===");
    console.log("1. ERC8183:           " + erc8183Address);
    console.log("2. ERC8126:           " + erc8126Address);
    console.log("3. ERC8021:           " + erc8021Address);
    console.log("4. ReputationHook_v2: " + reputationHookAddress);
    console.log("5. VestingGateIO:     " + vestingGateIOAddress);
    console.log("");
    console.log("=== TOKENS ACEITOS ===");
    console.log("USDT:  " + usdtAddress);
    console.log("WBNB:  " + wbnbAddress);
    console.log("LEVE:  " + leveToken);
    console.log("");
    console.log("🔗 BSCScan: https://bscscan.com/address/");
    console.log("");
    console.log("⚠️  PRÓXIMOS PASSOS:");
    console.log("1. Verificar contratos no BSCScan");
    console.log("2. Fazer verify dos contratos (opcional)");
    console.log("3. Integrar no dashboard");
    
  } catch (error) {
    console.error("❌ Erro no deploy:", error);
    process.exit(1);
  }
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
