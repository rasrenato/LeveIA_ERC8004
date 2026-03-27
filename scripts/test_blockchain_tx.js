// Script de teste para Alpha Signals x402
// Registra uma previsão de BTC no contrato ERC-8004

const { ethers } = require("hardhat");

// Configuração
const CONTRACT_ADDRESS = "0x2333cBC71805b47D64C2867Ef66682c7257B5D4f";
const RPC_URL = "https://mainnet.base.org"; // Base Mainnet
// const RPC_URL = "https://mainnet.infura.io/v3/YOUR_KEY"; // Ethereum Mainnet

// ABI mínima do contrato (função registerSignal)
const ABI = [
  "function registerSignal(string _asset, string _signalType, bytes32 _dataHash, string _metadataURI) public returns (uint256)",
  "function auditTrail(uint256) public view returns (uint256 timestamp, string asset, string signalType, bytes32 dataHash, string metadataURI)",
  "function nextAttestationId() public view returns (uint256)",
  "event SignalRegistered(uint256 indexed id, string asset, string signalType, bytes32 dataHash)"
];

async function main() {
  console.log("🧪 Teste Alpha Signals x402");
  console.log("============================\n");

  // Verificar PRIVATE_KEY
  const privateKey = process.env.PRIVATE_KEY;
  if (!privateKey) {
    console.log("❌ ERRO: PRIVATE_KEY não configurada");
    console.log("   Configure: export PRIVATE_KEY=0x...");
    console.log("   Ou adicione no arquivo .env\n");
    return;
  }

  // Conectar na rede
  console.log("📡 Conectando na rede...");
  const provider = new ethers.JsonRpcProvider(RPC_URL);
  const wallet = new ethers.Wallet(privateKey, provider);
  
  console.log(`   Rede: ${RPC_URL}`);
  console.log(`   Carteira: ${wallet.address}`);
  
  // Verificar saldo
  const balance = await provider.getBalance(wallet.address);
  console.log(`   Saldo: ${ethers.formatEther(balance)} ETH\n`);

  if (balance === 0n) {
    console.log("⚠️  Saldo zero! Adicione ETH na carteira antes de continuar.\n");
    return;
  }

  // Conectar ao contrato
  console.log("📄 Conectando ao contrato...");
  const contract = new ethers.Contract(CONTRACT_ADDRESS, ABI, wallet);
  console.log(`   Contrato: ${CONTRACT_ADDRESS}\n`);

  // Dados da previsão de teste
  const asset = "BTC";
  const signalType = "BUY"; // ou "SELL", "ACCUMULATE"
  const dataHash = ethers.keccak256(ethers.toUtf8Bytes("teste-qa-cabral-2026-03-04"));
  const metadataURI = "https://api.coinmarketleve.com/signals/test-001";

  console.log("📊 Dados da transação:");
  console.log(`   Asset: ${asset}`);
  console.log(`   Signal: ${signalType}`);
  console.log(`   DataHash: ${dataHash}`);
  console.log(`   Metadata: ${metadataURI}\n`);

  // Estimar gas
  console.log("⛽ Estimando gas...");
  try {
    const gasEstimate = await contract.registerSignal.estimateGas(
      asset,
      signalType,
      dataHash,
      metadataURI
    );
    console.log(`   Gas estimado: ${gasEstimate.toString()}\n`);
  } catch (err) {
    console.log("⚠️  Erro na estimativa (pode ser falta de permissão):");
    console.log(`   ${err.message}\n`);
  }

  // Enviar transação
  console.log("🚀 Enviando transação...");
  const tx = await contract.registerSignal(
    asset,
    signalType,
    dataHash,
    metadataURI
  );

  console.log(`   Hash: ${tx.hash}`);
  console.log("   Aguardando confirmação...");

  const receipt = await tx.wait();
  console.log(`\n✅ Transação confirmada!`);
  console.log(`   Block: ${receipt.blockNumber}`);
  console.log(`   Gas usado: ${receipt.gasUsed.toString()}`);
  console.log(`   Status: ${receipt.status === 1 ? 'Sucesso' : 'Falha'}\n`);

  // Ler evento
  const event = receipt.logs.find(log => {
    try {
      const parsed = contract.interface.parseLog(log);
      return parsed && parsed.name === 'SignalRegistered';
    } catch {
      return false;
    }
  });

  if (event) {
    const parsed = contract.interface.parseLog(event);
    console.log("📋 Evento SignalRegistered:");
    console.log(`   ID: ${parsed.args[0].toString()}`);
    console.log(`   Asset: ${parsed.args[1]}`);
    console.log(`   Signal: ${parsed.args[2]}`);
    console.log(`   Hash: ${parsed.args[3]}\n`);
  }

  // Verificar no contrato
  console.log("🔍 Verificando dados no contrato...");
  const nextId = await contract.nextAttestationId();
  const attestationId = nextId - 1n;
  
  const attestation = await contract.auditTrail(attestationId);
  console.log(`   Attestation ID: ${attestationId.toString()}`);
  console.log(`   Timestamp: ${new Date(Number(attestation.timestamp) * 1000).toISOString()}`);
  console.log(`   Asset: ${attestation.asset}`);
  console.log(`   Signal: ${attestation.signalType}`);
  console.log(`   DataHash: ${attestation.dataHash}\n`);

  console.log("✅ Teste concluído com sucesso!");
  console.log("\n📋 Resumo:");
  console.log(`   - Transação: ${tx.hash}`);
  console.log(`   - Explorador: https://basescan.org/tx/${tx.hash}`);
  console.log(`   - Contrato: https://basescan.org/address/${CONTRACT_ADDRESS}`);
}

main().catch((error) => {
  console.error("❌ Erro:", error.message);
  process.exitCode = 1;
});
