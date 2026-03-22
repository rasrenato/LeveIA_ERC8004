const hre = require("hardhat");

async function main() {
  console.log("🚀 Deploying ReputationHook v2 na BSC...");
  
  // Endereços existentes
  const AUDIT_REGISTRY = "0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512"; // LeveIA_AuditRegistry
  const ERC8183 = "0x5FbDB2315678afecb367f032d93F642f64180aa3"; // ERC-8183 Commercial Layer
  
  console.log(`📋 Audit Registry: ${AUDIT_REGISTRY}`);
  console.log(`📋 ERC-8183: ${ERC8183}`);
  
  // Deploy
  const ReputationHook = await hre.ethers.getContractFactory("ReputationHook_v2");
  const reputationHook = await ReputationHook.deploy(AUDIT_REGISTRY, ERC8183);
  
  await reputationHook.waitForDeployment();
  
  const address = await reputationHook.getAddress();
  
  console.log("✅ ReputationHook v2 deployado com sucesso!");
  console.log(`📍 Endereço: ${address}`);
  console.log(`🔗 BSCScan: https://bscscan.com/address/${address}`);
  
  // Salvar endereços
  const fs = require("fs");
  const addressesPath = "./addresses-bsc.json";
  let addresses = {};
  
  if (fs.existsSync(addressesPath)) {
    addresses = JSON.parse(fs.readFileSync(addressesPath, "utf8"));
  }
  
  addresses.ReputationHook_v2 = address;
  addresses.ReputationHook_v1 = addresses.ReputationHook;
  addresses.ReputationHook = address; // Atualizar para v2
  
  fs.writeFileSync(addressesPath, JSON.stringify(addresses, null, 2));
  
  console.log("📝 Endereços salvos em addresses-bsc.json");
  
  // Esperar algumas confirmações
  console.log("⏳ Aguardando confirmações...");
  await reputationHook.deploymentTransaction().wait(5);
  
  console.log("✅ Deploy confirmado!");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
