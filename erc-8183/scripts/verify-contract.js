// Script para verificar contrato no BSCScan via Hardhat
// Uso: npx hardhat run scripts/verify-contract.js --network bsc

const { ethers, run } = require("hardhat");

async function main() {
  console.log("🔍 BSCScan Contract Verification Script");
  console.log("========================================\n");

  // Verificar se tem API key
  const apiKey = process.env.BSCSCAN_API_KEY;
  if (!apiKey || apiKey === "") {
    console.log("❌ ERRO: BSCSCAN_API_KEY não configurada!");
    console.log("\n📋 COMO OBTER:");
    console.log("1. Crie conta em: https://bscscan.com/register");
    console.log("2. Pegue API key em: https://bscscan.com/myapikey");
    console.log("3. Adicione no .env: BSCSCAN_API_KEY=sua_key_aqui");
    process.exit(1);
  }

  console.log("✅ BSCSCAN_API_KEY configurada");

  // Contrato ERC-8183 (Alpha Signals)
  const contractAddress = "0xcf0520e60ad602454f06Cd80f588634A332d169d";
  const contractName = "ERC8183";
  const sourceFile = "contracts/ERC8183.sol";
  
  // Argumentos do constructor (do deploy original)
  const treasuryAddress = "0x077e8d29e11ff1c0ccb236e0380d0053dcba2b1c";
  const platformFeeBps = 10; // 0.1%
  
  console.log(`\n📋 Contrato: ${contractName}`);
  console.log(`📍 Endereço: ${contractAddress}`);
  console.log(`📄 Arquivo: ${sourceFile}`);
  console.log(`🔧 Constructor Args: treasury=${treasuryAddress}, fee=${platformFeeBps}bps\n`);

  try {
    console.log("🔄 Iniciando verificação no BSCScan...\n");
    
    await run("verify:verify", {
      address: contractAddress,
      constructorArguments: [treasuryAddress, platformFeeBps],
    });
    
    console.log("\n✅ Contrato verificado com sucesso!");
    console.log(`🔗 BSCScan: https://bscscan.com/address/${contractAddress}#code`);
    
  } catch (error) {
    console.log("\n❌ Erro na verificação:");
    console.log(error.message);
    
    if (error.message.includes("Already Verified")) {
      console.log("\nℹ️  Contrato já está verificado!");
    } else if (error.message.includes("Invalid API Key")) {
      console.log("\n❌ API Key inválida! Verifique em https://bscscan.com/myapikey");
    }
  }
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
