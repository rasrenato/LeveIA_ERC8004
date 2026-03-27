# 🍃 Leve IA - AI Trading Signals on Blockchain

**AI-powered trading signals with full transparency on BSC | Sinais de trading com IA e transparência total na BSC**

[![Status](https://img.shields.io/badge/status-production-green)](https://app.leve.app.br)
[![Blockchain](https://img.shields.io/badge/blockchain-BSC-yellow)](https://bscscan.com)
[![Testers](https://img.shields.io/badge/testers-9%20active-blue)](https://app.leve.app.br/dashboard)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

---

## 🏛️ Institutional Reference

For the official institutional layer of this project, start here:

- [`docs/official/README.md`](docs/official/README.md)
- [`docs/official/institutional-source-of-truth.md`](docs/official/institutional-source-of-truth.md)
- [`docs/official/official-architecture.md`](docs/official/official-architecture.md)
- [`docs/official/official-contracts.md`](docs/official/official-contracts.md)
- [`docs/official/official-agent-stack.md`](docs/official/official-agent-stack.md)
- [`docs/official/official-repo-governance.md`](docs/official/official-repo-governance.md)

This is the institutional spine for partners, exchanges, diligence and technical review.

---

## 🎯 What is Leve IA?

**Leve IA** is a SaaS platform that generates AI-powered trading signals with full transparency on blockchain.

**Leve IA** é uma plataforma SaaS que gera sinais de trading com IA e transparência total na blockchain.

### Key Features | Principais Funcionalidades

- 🤖 **AI-Generated Signals** - 24/7 analysis of BTC, ETH, BNB
- 🔍 **Full Transparency** - All signals recorded on BSC (ERC-8004)
- 📊 **Real-Time Data** - Live prices from Binance API
- 💰 **Pay-Per-Signal** - $0.10 in LEVE tokens (coming soon)
- 📱 **Mobile-First** - Works on any device

---

## 🚀 Live Links | Links Oficiais

| Service | URL | Status |
|---------|-----|--------|
| **Dashboard** | https://app.leve.app.br | ✅ Online |
| **Token LEVE** | [BSCScan](https://bscscan.com/token/0x67e463AcC3B35406B0f35C8Ed531da89f9670861) | ✅ 53+ Holders |
| **Contracts** | See [Contracts](#smart-contracts--contratos-inteligentes) | ✅ 5 Deployed |

---

## 📊 Smart Contracts | Contratos Inteligentes

All contracts deployed on **Binance Smart Chain (BSC)** | Todos os contratos na **Binance Smart Chain (BSC)**

| Contract | Address | Function | BSCScan |
|----------|---------|----------|---------|
| **ERC-8183** (Alpha Signals) | `0xcf0520e60ad602454f06Cd80f588634A332d169d` | Paid Signals (x402) | [View](https://bscscan.com/address/0xcf0520e60ad602454f06Cd80f588634A332d169d) |
| **ERC-8004** (Reputation) | `0x2A0Af7fA4e8A39bF7B34201CdDba8faed88C27c2` | Audit Trail | [View](https://bscscan.com/address/0x2A0Af7fA4e8A39bF7B34201CdDba8faed88C27c2) |
| **ERC-8126** (Risk Scoring) | `0x1d693286CE314fE7dEB26AeDcA3DF7f45F386133` | Risk Analysis | [View](https://bscscan.com/address/0x1d693286CE314fE7dEB26AeDcA3DF7f45F386133) |
| **ERC-8021** (Attribution) | `0x9e5100EF4Dd701d59aeaF95C89403308cc6dF368` | IP Protection | [View](https://bscscan.com/address/0x9e5100EF4Dd701d59aeaF95C89403308cc6dF368) |
| **VestingGateIO** | `0x5798bbECAF20E013718bd89Ef7339b5Ae3643Ff1` | Gate.io Vesting | [View](https://bscscan.com/address/0x5798bbECAF20E013718bd89Ef7339b5Ae3643Ff1) |
| **Token LEVE** (BEP-20) | `0x67e463AcC3B35406B0f35C8Ed531da89f9670861` | Official Token | [View](https://bscscan.com/token/0x67e463AcC3B35406B0f35C8Ed531da89f9670861) |

**Total Deployment Cost:** ~$0.06 USD (March 12, 2026)

---

## 🏗️ Architecture | Arquitetura

```
┌─────────────────────────────────────────────────────────┐
│                    LEVE IA SYSTEM                        │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐      ┌──────────────┐                │
│  │   Frontend   │      │    Backend   │                │
│  │   (Next.js)  │◄────►│  (Node.js)   │                │
│  │  app.leve.   │      │   (Express)  │                │
│  │   app.br     │      │   Port 3002  │                │
│  └──────────────┘      └──────┬───────┘                │
│                                │                        │
│                                ▼                        │
│  ┌──────────────────────────────────────────┐          │
│  │         AI Alpha Engine                  │          │
│  │  - BTC/ETH/BNB Analysis 24/7            │          │
│  │  - Real-time Binance API                │          │
│  │  - Win/Loss Tracking                    │          │
│  └──────────────────────────────────────────┘          │
│                                │                        │
│                                ▼                        │
│  ┌──────────────────────────────────────────┐          │
│  │      Binance Smart Chain (BSC)           │          │
│  │  - 5 Smart Contracts                    │          │
│  │  - Signal Recording (ERC-8004)          │          │
│  │  - Payment System (ERC-8183)            │          │
│  │  - Token LEVE (BEP-20)                  │          │
│  └──────────────────────────────────────────┘          │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 📁 Repository Shape | Estrutura Atual do Repositório

The repository is being actively curated into institutional, technical and operational layers.
At this stage, the most reliable references are:

- `docs/official/` → institutional source of truth
- `alpha_signals/` → AI signal generation and related backend logic
- `erc-8183/` → smart contract deployment and verification material
- `contracts/` → selected contract artifacts and Solidity sources
- `scripts/` → deployment, sync and auxiliary automation scripts
- `docs/` → technical, operational and historical documentation

**Important:** some directories in this repository are still under sanitation and should not be interpreted as fully curated product-source trees yet.

---

## 🚀 Quick Start | Início Rápido

### Prerequisites | Pré-requisitos

```bash
- Node.js 18+ 
- Python 3.10+
- MetaMask (for Web3 features)
- BSC Testnet BNB (for testing)
```

### Frontend | Frontend

```bash
cd leveclaw
npm install
npm run dev
# Open http://localhost:3001
```

### Backend | Backend

```bash
cd alpha_signals
pip install -r requirements.txt
python api_server.py
# API running on http://localhost:5000
```

### Smart Contracts | Contratos Inteligentes

```bash
cd erc-8183
npm install
npx hardhat compile
npx hardhat test
# Deploy to BSC:
npx hardhat run scripts/deploy-bsc.js --network bsc
```

---

## 📊 Current Status | Status Atual

| Component | Status | Details |
|-----------|--------|---------|
| **Dashboard** | ✅ Production | app.leve.app.br |
| **AI Signals** | ✅ Active | 9 testers using |
| **Smart Contracts** | ✅ Deployed | 5 contracts on BSC |
| **Token LEVE** | ✅ Live | 53+ holders |
| **Payment System** | ⏳ Coming Soon | MetaMask integration |
| **Gate.io Listing** | ⏳ In Progress | $30k target |

---

## 🎯 Roadmap

### Phase 1: Foundation ✅ (Completed March 2026)
- [x] AI signal generator
- [x] Dashboard MVP
- [x] 5 smart contracts deployed
- [x] 9 beta testers

### Phase 2: Validation (March-April 2026)
- [ ] Collect user feedback (deadline: March 13, 18:00 UTC)
- [ ] Integrate MetaMask payment
- [ ] Gate.io listing ($30k target)
- [ ] Token migration (53 → 150+ holders)

### Phase 3: Scale (April-June 2026)
- [ ] 100+ active users
- [ ] $0.10/signal or $29-99/month
- [ ] Multi-language support
- [ ] Mobile app (iOS/Android)

---

## 📈 Traction | Tração

- **9 Active Testers** - Validating product-market fit
- **5 Smart Contracts** - $0.06 deployment cost
- **53+ Token Holders** - Growing community
- **24/7 AI Analysis** - BTC, ETH, BNB signals
- **100% Transparency** - All signals on-chain

---

## 🤝 Contributing | Contribuindo

We welcome contributions! Please see our [Contributing Guide](docs/CONTRIBUTING.md) for details.

Contribuições são bem-vindas! Veja nosso [Guia de Contribuição](docs/CONTRIBUTING.md).

### How to Help | Como Ajudar

1. 🐛 Report bugs (GitHub Issues)
2. 💡 Suggest features (GitHub Discussions)
3. 📝 Improve documentation (PRs welcome)
4. 🧪 Test new features (beta testers)

---

## 📄 License | Licença

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Team | Equipe

- **Renato Abreu** - CEO & Founder | [@rasrenato](https://github.com/rasrenato)
- **Cabral** - AI Assistant (CEO Agent)

---

## 📞 Contact | Contato

- **Website:** https://app.leve.app.br
- **Dashboard:** https://app.leve.app.br/dashboard
- **Token:** https://bscscan.com/token/0x67e463AcC3B35406B0f35C8Ed531da89f9670861
- **Email:** contact@leve.app.br (coming soon)

---

## 🙏 Acknowledgments | Agradecimentos

- **Beta Testers** - Hélcio, João, and 7 others validating the product
- **Binance** - Real-time market data API
- **BSC** - Low-cost, fast blockchain for smart contracts
- **OpenClaw** - AI assistant infrastructure

---

**Built with ❤️ for transparent, AI-powered trading**

**Construído com ❤️ para trading transparente com IA**

---

*Last Updated: March 12, 2026 | Última Atualização: 12 de Março, 2026*
