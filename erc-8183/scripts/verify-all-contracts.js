// Script para verificar TODOS os contratos no BSCScan via Hardhat
// Uso: npx hardhat run scripts/verify-all-contracts.js --network bsc

const { ethers, run } = require("hardhat");

// Lista de contratos com endereços e argumentos de constructor
const CONTRACTS = [
  {
    name: "ERC-8183 (Alpha Signals)",
    address: "0xcf0520e60ad602454f06Cd80f588634A332d169d",
    file: "contracts/ERC8183.sol",
    contractName: "ERC8183",
    args: ["0x077e8d29e11ff1c0ccb236e0380d0053dcba2b1c", 10], // treasury, feeBps
    status: "✅ JÁ VERIFICADO"
  },
  {
    name: "ERC-8004 (Reputation)",
    address: "0x2A0Af7fA4e8A39bF7B34201CdDba8faed88C27c2",
    file: "contracts/ReputationHook_v2.sol",
    contractName: "ReputationHook_v2",
    args: ["0x0000000000000000000000000000000000000000"], // _erc8004Registry (zero address no deploy)
    status: "⏳ Pendente"
  },
  {
    name: "ERC-8126 (Risk Scoring)",
    address: "0x1d693286CE314fE7dEB26AeDcA3DF7f45F386133",
    file: "contracts/ERC8126.sol",
    contractName: "ERC8126",
    args: [], // Sem constructor args
    status: "⏳ Pendente"
  },
  {
    name: "ERC-8021 (Attribution)",
    address: "0x9e5100EF4Dd701d59aeaF95C89403308cc6dF368",
    file: "contracts/ERC8021.sol",
    contractName: "ERC8021",
    args: [10], // _platformFeeBps
    status: "⏳ Pendente"
  },
  {
    name: "VestingGateIO",
    address: "0x5798bbECAF20E013718bd89Ef7339b5Ae3643Ff1",
    file: "contracts/VestingGateIO.sol",
    contractName: "VestingGateIO",
    args: [], // Sem constructor args
    status: "⏳ Pendente"
  }
];

async function verifyContract(contract) {
  console.log(`\n${"=".repeat(60)}`);
  console.log(`📋 Contrato: ${contract.name}`);
  console.log(`📍 Endereço: ${contract.address}`);
  console.log(`📄 Arquivo: ${contract.file}`);
  console.log(`🔧 Args: ${contract.args.length > 0 ? JSON.stringify(contract.args) : "Nenhum"}`);
  console.log(`${"=".repeat(60)}\n`);

  try {
    await run("verify:verify", {
      address: contract.address,
      constructorArguments: contract.args,
    });
    
    console.log(`\n✅ ${contract.name} verificado com sucesso!`);
    console.log(`🔗 BSCScan: https://bscscan.com/address/${contract.address}#code`);
    contract.status = "✅ VERIFICADO";
    return true;
    
  } catch (error) {
    console.log(`\n❌ Erro na verificação de ${contract.name}:`);
    console.log(error.message);
    
    if (error.message.includes("Already Verified")) {
      console.log("\nℹ️  Contrato já está verificado!");
      contract.status = "✅ JÁ VERIFICADO";
      return true;
    } else if (error.message.includes("Invalid API Key")) {
      console.log("\n❌ API Key inválida!");
      contract.status = "❌ ERRO - API Key";
      return false;
    } else {
      contract.status = `❌ ERRO - ${error.message.substring(0, 50)}`;
      return false;
    }
  }
}

async function main() {
  console.log("🔍 BSCScan Contract Verification Script - ALL CONTRACTS");
  console.log("=======================================================\n");

  // Verificar se tem API key
  const apiKey = process.env.BSCSCAN_API_KEY;
  if (!apiKey || apiKey === "") {
    console.log("❌ ERRO: BSCSCAN_API_KEY não configurada!");
    process.exit(1);
  }

  console.log("✅ BSCSCAN_API_KEY configurada");
  console.log("📊 Total de contratos: 5\n");

  // Verificar cada contrato
  let successCount = 0;
  for (const contract of CONTRACTS) {
    if (contract.status === "✅ JÁ VERIFICADO") {
      console.log(`\n⏭️  Pulando ${contract.name} (já verificado)`);
      successCount++;
      continue;
    }

    const result = await verifyContract(contract);
    if (result) {
      successCount++;
    }
    
    // Aguardar entre verificações (rate limit)
    if (CONTRACTS.indexOf(contract) < CONTRACTS.length - 1) {
      console.log("\n⏱️  Aguardando 5 segundos (rate limit)...");
      await new Promise(resolve => setTimeout(resolve, 5000));
    }
  }

  // Relatório final
  console.log(`\n${"=".repeat(60)}`);
  console.log("📊 RELATÓRIO FINAL");
  console.log(`${"=".repeat(60)}\n`);
  
  console.log("Status de cada contrato:\n");
  for (const contract of CONTRACTS) {
    console.log(`${contract.status.padEnd(20)} | ${contract.name}`);
    console.log(`                     | https://bscscan.com/address/${contract.address}#code`);
  }
  
  console.log(`\n${"=".repeat(60)}`);
  console.log(`✅ Sucesso: ${successCount}/${CONTRACTS.length} contratos`);
  console.log(`${"=".repeat(60)}\n`);
  
  if (successCount === CONTRACTS.length) {
    console.log("🎉 TODOS OS CONTRATOS VERIFICADOS COM SUCESSO!");
  } else {
    console.log("⚠️  Alguns contratos falharam. Verifique os erros acima.");
  }
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
