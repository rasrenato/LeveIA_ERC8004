const { ethers } = require("hardhat");

async function main() {
    console.log("⛽ Gas Estimation for Leve IA Agent Registration");
    console.log("================================================\n");

    const [deployer] = await ethers.getSigners();
    
    // Get gas price
    const feeData = await ethers.provider.getFeeData();
    const gasPrice = feeData.gasPrice;
    
    console.log("📊 Current Network Data:");
    console.log(`   Gas Price: ${ethers.formatUnits(gasPrice, "gwei")} Gwei`);
    console.log(`   Base Fee: ${ethers.formatUnits(feeData.maxFeePerGas || 0, "gwei")} Gwei (max)`);
    console.log(`   Priority Fee: ${ethers.formatUnits(feeData.maxPriorityFeePerGas || 0, "gwei")} Gwei`);
    console.log("");

    // Estimate contract deployment
    console.log("📦 Contract Deployment Estimation:");
    const LeveIA_AuditRegistry = await ethers.getContractFactory("LeveIA_AuditRegistry");
    const deploymentGas = await ethers.provider.estimateGas(
        LeveIA_AuditRegistry.getDeployTransaction()
    );
    
    const deploymentCost = deploymentGas * gasPrice;
    console.log(`   Deployment Gas: ${deploymentGas.toString()}`);
    console.log(`   Deployment Cost: ${ethers.formatEther(deploymentCost)} ETH`);
    console.log("");

    // Estimate agent registration
    console.log("🤖 Agent Registration Estimation:");
    const registry = await LeveIA_AuditRegistry.deploy();
    await registry.waitForDeployment();
    
    const AGENT_ID = "leve-ia-market-predictor-v1";
    const CAPABILITIES = JSON.stringify({
        name: "Leve IA Market Predictor",
        version: "1.0.0"
    });
    const initialAttestationRoot = ethers.keccak256(ethers.toUtf8Bytes("initial-root"));
    
    const registerGas = await registry.registerAgent.estimateGas(
        AGENT_ID,
        CAPABILITIES,
        initialAttestationRoot
    );
    
    const registerCost = registerGas * gasPrice;
    console.log(`   Registration Gas: ${registerGas.toString()}`);
    console.log(`   Registration Cost: ${ethers.formatEther(registerCost)} ETH`);
    console.log("");

    // Estimate attestation batch creation
    console.log("📊 Attestation Batch Creation Estimation:");
    const attestationRoot = ethers.keccak256(ethers.toUtf8Bytes("batch-root"));
    
    const batchGas = await registry.createAttestationBatch.estimateGas(
        attestationRoot,
        10 // 10TB
    );
    
    const batchCost = batchGas * gasPrice;
    console.log(`   Batch Creation Gas: ${batchGas.toString()}`);
    console.log(`   Batch Creation Cost: ${ethers.formatEther(batchCost)} ETH`);
    console.log("");

    // Estimate prediction logging
    console.log("📈 Prediction Logging Estimation:");
    const inputHash = ethers.keccak256(ethers.toUtf8Bytes("input-data"));
    const proof = ethers.keccak256(ethers.toUtf8Bytes("proof"));
    const circleAttestation = ethers.keccak256(ethers.toUtf8Bytes("circle-attestation"));
    
    const predictionGas = await registry.logPrediction.estimateGas(
        "Gemini-3-LeveV2",
        inputHash,
        "BTC_LONG_78000",
        proof,
        circleAttestation
    );
    
    const predictionCost = predictionGas * gasPrice;
    console.log(`   Prediction Logging Gas: ${predictionGas.toString()}`);
    console.log(`   Prediction Logging Cost: ${ethers.formatEther(predictionCost)} ETH`);
    console.log("");

    // Total estimation
    console.log("💰 Total Estimated Costs:");
    const totalGas = deploymentGas + registerGas + batchGas + predictionGas;
    const totalCost = deploymentCost + registerCost + batchCost + predictionCost;
    
    console.log(`   Total Gas: ${totalGas.toString()}`);
    console.log(`   Total Cost: ${ethers.formatEther(totalCost)} ETH`);
    
    // Convert to USD (approximate)
    const ethPrice = 3500; // Approximate ETH price in USD
    const totalCostUSD = parseFloat(ethers.formatEther(totalCost)) * ethPrice;
    console.log(`   Total Cost (USD): $${totalCostUSD.toFixed(2)}`);
    console.log("");

    console.log("📝 Note: Actual costs may vary based on:");
    console.log("   - Network congestion");
    console.log("   - Gas price fluctuations");
    console.log("   - Contract size optimization");
    console.log("   - ETH/USD exchange rate");
    
    return {
        deploymentGas: deploymentGas.toString(),
        deploymentCost: ethers.formatEther(deploymentCost),
        registerGas: registerGas.toString(),
        registerCost: ethers.formatEther(registerCost),
        batchGas: batchGas.toString(),
        batchCost: ethers.formatEther(batchCost),
        predictionGas: predictionGas.toString(),
        predictionCost: ethers.formatEther(predictionCost),
        totalGas: totalGas.toString(),
        totalCost: ethers.formatEther(totalCost),
        totalCostUSD: totalCostUSD.toFixed(2)
    };
}

if (require.main === module) {
    main()
        .then(() => process.exit(0))
        .catch((error) => {
            console.error(error);
            process.exit(1);
        });
}

module.exports = main;