require("@nomicfoundation/hardhat-toolbox");
require("dotenv").config();

/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
  solidity: {
    version: "0.8.20",
    settings: {
      optimizer: {
        enabled: true,
        runs: 200,
      },
    },
  },
  networks: {
    hardhat: {
      chainId: 31337,
    },
    // Binance Smart Chain (BSC)
    bsc: {
      url: process.env.BSC_RPC_URL || "https://bsc-dataseed.binance.org/",
      chainId: 56,
      accounts: process.env.PRIVATE_KEY && process.env.PRIVATE_KEY.length > 10 ? [process.env.PRIVATE_KEY] : [],
      gasPrice: "auto",
    },
    bscTestnet: {
      url: process.env.BSC_TESTNET_RPC_URL || "https://data-seed-prebsc-1-s1.binance.org:8545/",
      chainId: 97,
      accounts: process.env.PRIVATE_KEY && process.env.PRIVATE_KEY.length > 10 ? [process.env.PRIVATE_KEY] : [],
      gasPrice: 10000000000,
    },
    "base-sepolia": {
      url: process.env.BASE_SEPOLIA_RPC_URL || "https://sepolia.base.org",
      chainId: 84532,
      accounts: process.env.PRIVATE_KEY && process.env.PRIVATE_KEY.length > 10 ? [process.env.PRIVATE_KEY] : [],
    },
    base: {
      url: process.env.BASE_RPC_URL || "https://mainnet.base.org",
      chainId: 8453,
      accounts: process.env.PRIVATE_KEY && process.env.PRIVATE_KEY.length > 10 ? [process.env.PRIVATE_KEY] : [],
    },
  },
  // API V2 do Etherscan (Multichain)
  etherscan: {
    apiKey: process.env.BSCSCAN_API_KEY || "",
  },
};
