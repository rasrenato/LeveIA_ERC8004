
const { ethers } = require("ethers");

async function main() {
    const provider = new ethers.JsonRpcProvider("https://mainnet.base.org");
    const address = "0x077e8d29e11ff1c0ccb236e0380d0053dcba2b1c";
    
    console.log(`Buscando transações de deploy para: ${address}...`);
    
    const currentBlock = await provider.getBlockNumber();
    // Busca nos últimos 10.000 blocos (aprox. 5 horas na Base)
    for (let i = 0; i < 10000; i += 1000) {
        const logs = await provider.getLogs({
            fromBlock: currentBlock - i - 1000,
            toBlock: currentBlock - i,
            address: null // Queremos transações de criação, não eventos
        });
        // Como logs de criação são complexos, vamos direto no histórico de transações via fetch
    }
}

// Alternativa mais rápida: usar fetch no explorer via proxy ou similar
main();
