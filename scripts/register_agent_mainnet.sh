#!/bin/bash

# Leve IA - Agent Registration on Ethereum Mainnet
# This script deploys and registers the Leve IA agent on Ethereum Mainnet

set -e

echo "🚀 Leve IA - Ethereum Mainnet Agent Registration"
echo "================================================="
echo ""

# Configuration
CONTRACT_NAME="LeveIA_AuditRegistry"
AGENT_ID="leve-ia-market-predictor-v1"
NETWORK="mainnet"

# Check for required environment variables
if [ -z "$PRIVATE_KEY" ]; then
    echo "❌ ERROR: PRIVATE_KEY environment variable is not set"
    echo "   Export your Ethereum private key:"
    echo "   export PRIVATE_KEY=your_private_key_here"
    exit 1
fi

if [ -z "$INFURA_API_KEY" ]; then
    echo "❌ ERROR: INFURA_API_KEY environment variable is not set"
    echo "   Get an API key from https://infura.io"
    echo "   export INFURA_API_KEY=your_infura_api_key"
    exit 1
fi

# Check for required tools
command -v node >/dev/null 2>&1 || { echo "❌ Node.js is required but not installed"; exit 1; }
command -v npm >/dev/null 2>&1 || { echo "❌ npm is required but not installed"; exit 1; }
command -v npx >/dev/null 2>&1 || { echo "❌ npx is required but not installed"; exit 1; }

echo "✅ Environment check passed"
echo "📋 Configuration:"
echo "   Network: $NETWORK"
echo "   Contract: $CONTRACT_NAME"
echo "   Agent ID: $AGENT_ID"
echo ""

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install --silent
fi

# Create capabilities JSON
echo "📝 Creating agent capabilities configuration..."
CAPABILITIES_JSON=$(cat <<EOF
{
    "name": "Leve IA Market Predictor",
    "version": "1.0.0",
    "description": "AI agent for financial market predictions using 10TB data processing with Circle Protocol attestations",
    "capabilities": [
        "market_prediction",
        "data_processing_10tb",
        "circle_attestations",
        "agent0_sdk_compatible",
        "erc8004_compliant"
    ],
    "dataProcessing": {
        "volume": "10TB",
        "attestation": "circle_protocol",
        "frequency": "daily",
        "proofType": "merkle_root_batch"
    },
    "integration": {
        "agent0Sdk": true,
        "circleProtocol": true,
        "ethereumMainnet": true
    }
}
EOF
)

echo "$CAPABILITIES_JSON" > config/agent_capabilities.json
echo "✅ Capabilities configuration saved to config/agent_capabilities.json"
echo ""

# Compile contract
echo "🔧 Compiling smart contract..."
npx hardhat compile --quiet
echo "✅ Contract compiled successfully"
echo ""

# Estimate gas costs
echo "⛽ Estimating gas costs..."
GAS_ESTIMATE=$(npx hardhat run scripts/estimate_gas.js --network $NETWORK 2>/dev/null || echo "Gas estimation failed")
echo "   Estimated gas: $GAS_ESTIMATE"
echo ""

# Deploy and register
echo "🚀 Starting deployment and registration process..."
echo "   This may take a few minutes..."
echo ""

# Run deployment script
npx hardhat run scripts/deploy_and_register.js --network $NETWORK

echo ""
echo "================================================="
echo "🎉 Agent Registration Complete!"
echo ""
echo "📋 Next Steps:"
echo "   1. Verify contract on Etherscan"
echo "   2. Register agent in Agent0 SDK registry"
echo "   3. Configure Circle Protocol attestation service"
echo "   4. Set up automated prediction logging"
echo ""
echo "🔗 Useful Links:"
echo "   - Agent0 SDK: https://sdk.ag0.xyz"
echo "   - Circle Protocol: https://developers.circle.com"
echo "   - Etherscan: https://etherscan.io"
echo ""
echo "💡 Tips:"
echo "   - Keep your private key secure"
echo "   - Monitor contract events for predictions"
echo "   - Use the verifyAuditLog function to validate proofs"
echo ""