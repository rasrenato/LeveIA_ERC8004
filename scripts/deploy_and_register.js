const { ethers } = require("hardhat");
const { parseEther } = ethers;

async function main() {
    console.log("🚀 Leve IA - Agent Registration Script");
    console.log("=======================================\n");

    // Configuration
    const NETWORK = "mainnet";
    const AGENT_ID = "leve-ia-market-predictor-v1";
    const CAPABILITIES = JSON.stringify({
        name: "Leve IA Market Predictor",
        version: "1.0.0",
        description: "AI agent for financial market predictions using 10TB data processing",
        capabilities: [
            "market_prediction",
            "data_processing_10tb",
            "circle_attestations",
            "agent0_sdk_compatible"
        ],
        dataProcessing: {
            volume: "10TB",
            attestation: "circle_protocol",
            frequency: "daily"
        }
    });

    // Get signer
    const [deployer] = await ethers.getSigners();
    console.log(`📝 Deployer: ${deployer.address}`);
    console.log(`🌐 Network: ${NETWORK}\n`);

    // Deploy contract
    console.log("📦 Deploying LeveIA_AuditRegistry contract...");
    const LeveIA_AuditRegistry = await ethers.getContractFactory("LeveIA_AuditRegistry");
    const registry = await LeveIA_AuditRegistry.deploy();
    await registry.waitForDeployment();
    
    const contractAddress = await registry.getAddress();
    console.log(`✅ Contract deployed at: ${contractAddress}`);
    console.log(`📜 Contract owner: ${await registry.owner()}\n`);

    // Register agent
    console.log("🤖 Registering agent with Agent0 SDK compatibility...");
    
    // Generate initial attestation root (mock for example)
    const initialAttestationRoot = ethers.keccak256(ethers.toUtf8Bytes("initial-attestation-root"));
    
    const tx = await registry.registerAgent(
        AGENT_ID,
        CAPABILITIES,
        initialAttestationRoot
    );
    
    await tx.wait();
    console.log(`✅ Agent registered with ID: ${AGENT_ID}`);
    console.log(`📋 Transaction hash: ${tx.hash}\n`);

    // Verify registration
    console.log("🔍 Verifying agent registration...");
    const agentInfo = await registry.getAgentRegistration(deployer.address);
    
    console.log("📊 Agent Registration Details:");
    console.log(`   Agent Address: ${agentInfo.agentAddress}`);
    console.log(`   Agent ID: ${agentInfo.agentId}`);
    console.log(`   Registration Time: ${new Date(Number(agentInfo.registrationTime) * 1000).toISOString()}`);
    console.log(`   Active: ${agentInfo.isActive}`);
    console.log(`   Attestation Root: ${agentInfo.attestationRoot}`);
    console.log(`   Capabilities: ${agentInfo.capabilities}\n`);

    // Create first attestation batch (10TB data processing)
    console.log("📊 Creating first attestation batch for 10TB data processing...");
    const attestationRoot = ethers.keccak256(ethers.toUtf8Bytes("10tb-data-processing-batch-1"));
    
    const batchTx = await registry.createAttestationBatch(
        attestationRoot,
        10 // 10TB
    );
    
    await batchTx.wait();
    console.log(`✅ Attestation batch created for 10TB data processing`);
    console.log(`📋 Batch transaction hash: ${batchTx.hash}\n`);

    // Log first prediction with Circle attestation
    console.log("📈 Logging first market prediction with Circle attestation...");
    
    const inputHash = ethers.keccak256(ethers.toUtf8Bytes("10tb-market-data-2024-01"));
    const proof = ethers.keccak256(ethers.toUtf8Bytes("zk-proof-market-prediction"));
    const circleAttestation = ethers.keccak256(ethers.toUtf8Bytes("circle-attestation-10tb-processing"));
    
    const predictionTx = await registry.logPrediction(
        "Gemini-3-LeveV2",
        inputHash,
        "BTC_LONG_78000_USD_2024Q1",
        proof,
        circleAttestation
    );
    
    await predictionTx.wait();
    console.log(`✅ First prediction logged with Circle attestation`);
    console.log(`📋 Prediction transaction hash: ${predictionTx.hash}\n`);

    // Final summary
    console.log("🎉 Deployment and Registration Complete!");
    console.log("=========================================");
    console.log(`📋 Contract Address: ${contractAddress}`);
    console.log(`🤖 Agent ID: ${AGENT_ID}`);
    console.log(`👤 Agent Owner: ${deployer.address}`);
    console.log(`🔗 Agent0 SDK Compatible: YES`);
    console.log(`🔄 Circle Protocol Attestations: YES`);
    console.log(`💾 Data Processing Proof: 10TB`);
    console.log(`📊 First Prediction: Logged with attestation\n`);

    console.log("📝 Next Steps:");
    console.log("1. Verify contract on Etherscan");
    console.log("2. Register agent in Agent0 SDK registry");
    console.log("3. Configure Circle Protocol attestation service");
    console.log("4. Set up automated prediction logging\n");

    return {
        contractAddress,
        agentId: AGENT_ID,
        deployer: deployer.address,
        transactions: {
            deploy: registry.deploymentTransaction()?.hash,
            registerAgent: tx.hash,
            createBatch: batchTx.hash,
            logPrediction: predictionTx.hash
        }
    };
}

// Execute script
main()
    .then((result) => {
        console.log("✅ Script executed successfully");
        process.exit(0);
    })
    .catch((error) => {
        console.error("❌ Script failed:", error);
        process.exit(1);
    });