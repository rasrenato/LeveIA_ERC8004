// Script para verificar apenas VestingGateIO
const { run } = require("hardhat");

async function main() {
  console.log("🔍 Verificando VestingGateIO...\n");

  const tokenAddress = "0x67e463AcC3B35406B0f35C8Ed531da89f9670861"; // Token LEVE
  
  await run("verify:verify", {
    address: "0x5798bbECAF20E013718bd89Ef7339b5Ae3643Ff1",
    constructorArguments: [tokenAddress],
  });
  
  console.log("\n✅ VestingGateIO verificado com sucesso!");
  console.log("🔗 BSCScan: https://bscscan.com/address/0x5798bbECAF20E013718bd89Ef7339b5Ae3643Ff1#code\n");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
