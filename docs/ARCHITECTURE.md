# 🏗️ Leve IA - System Architecture

**Complete technical documentation of the Leve IA platform**

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Frontend Architecture](#frontend-architecture)
4. [Backend Architecture](#backend-architecture)
5. [Smart Contracts](#smart-contracts)
6. [Data Flow](#data-flow)
7. [Security](#security)
8. [Deployment](#deployment)

---

## Overview

Leve IA is a SaaS platform that combines AI-powered trading signals with blockchain transparency.

### Tech Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Frontend** | Next.js 14 + React | User interface |
| **Backend** | Node.js (Express) | API server |
| **AI Engine** | Python + Flask | Signal generation |
| **Database** | PostgreSQL | Data storage |
| **Blockchain** | BSC (Binance Smart Chain) | Smart contracts |
| **Hosting** | VPS (Ubuntu) | Production deployment |

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      USER INTERFACE                          │
│                    (Next.js Frontend)                        │
│                  https://app.leve.app.br                     │
└─────────────────────┬───────────────────────────────────────┘
                      │ HTTPS
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                      API GATEWAY                             │
│                    (Nginx Reverse Proxy)                     │
│                 Port 80/443 → 3001/3002                      │
└─────────────────────┬───────────────────────────────────────┘
                      │
         ┌────────────┴────────────┐
         │                         │
         ▼                         ▼
┌─────────────────┐       ┌─────────────────┐
│    Frontend     │       │    Backend      │
│   (Port 3001)   │       │   (Port 3002)   │
│   Next.js SSR   │       │   Express API   │
└─────────────────┘       └────────┬────────┘
                                   │
                                   ▼
                          ┌─────────────────┐
                          │  AI Alpha Engine│
                          │   (Port 5000)   │
                          │   Python Flask  │
                          └────────┬────────┘
                                   │
                          ┌────────┴────────┐
                          │                 │
                          ▼                 ▼
                   ┌─────────────┐   ┌─────────────┐
                   │  PostgreSQL │   │   Binance   │
                   │  (Localhost)│   │    API      │
                   └─────────────┘   └─────────────┘
                                   │
                                   ▼
                          ┌─────────────────┐
                          │  BSC Blockchain │
                          │  5 Smart Ctrcts │
                          └─────────────────┘
```

---

## Frontend Architecture

### Stack
- **Framework:** Next.js 14.2.35 (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **Charts:** Recharts
- **State:** React Hooks

### Key Components

```
/src/app/
├── dashboard/           # Main dashboard
│   ├── page.tsx        # Dashboard home
│   ├── alpha-signals/  # Signals page
│   ├── agents/         # AI agents
│   ├── analytics/      # Analytics
│   └── leveia/         # Leve IA section
├── login/              # Authentication
├── register/           # Registration
└── pricing/            # Pricing page

/src/components/
├── leveia/            # Leve IA components
│   ├── BTCPrediction.tsx
│   ├── ContractList.tsx
│   └── SignalGuide.tsx
└── ui/                # Reusable UI components
```

### Data Flow

```
User Action → React Component → API Call → Backend → Response → UI Update
```

---

## Backend Architecture

### Stack
- **Runtime:** Node.js 22
- **Framework:** Express.js
- **Database:** PostgreSQL (via node-postgres)
- **Auth:** JWT tokens
- **Security:** Helmet, CORS, Rate Limiting

### Key Routes

```javascript
/api/auth          // Authentication
/api/users         // User management
/api/alpha-signals // AI signals
  ├── GET /btc-price      // Real-time BTC price
  ├── GET /contracts      // Smart contract list
  ├── GET /signals        // Signal list
  └── POST /save          // Save unlocked signal
/api/analytics     // Analytics data
/api/agents        // AI agents
```

### Database Schema

```sql
-- Users table
CREATE TABLE users (
  id UUID PRIMARY KEY,
  email VARCHAR(255) UNIQUE,
  password_hash VARCHAR(255),
  created_at TIMESTAMP
);

-- Alpha signals table
CREATE TABLE alpha_signals (
  id UUID PRIMARY KEY,
  symbol VARCHAR(20),
  direction VARCHAR(10),
  entry_min DECIMAL,
  entry_max DECIMAL,
  stop_loss DECIMAL,
  targets JSONB,
  status VARCHAR(20),
  pnl DECIMAL,
  created_at TIMESTAMP
);
```

---

## Smart Contracts

### Overview

5 contracts deployed on BSC Mainnet:

| Contract | Purpose | Address |
|----------|---------|---------|
| ERC-8183 | Paid signals (x402) | `0xcf0520e60ad602454f06Cd80f588634A332d169d` |
| ERC-8004 | Reputation/Audit | `0x2A0Af7fA4e8A39bF7B34201CdDba8faed88C27c2` |
| ERC-8126 | Risk scoring | `0x1d693286CE314fE7dEB26AeDcA3DF7f45F386133` |
| ERC-8021 | Attribution | `0x9e5100EF4Dd701d59aeaF95C89403308cc6dF368` |
| VestingGateIO | Gate.io vesting | `0x5798bbECAF20E013718bd89Ef7339b5Ae3643Ff1` |

### Development Stack

- **Framework:** Hardhat
- **Language:** Solidity 0.8.20
- **Testing:** Hardhat + Chai
- **Deployment:** Custom scripts

---

## Data Flow

### Signal Generation Flow

```
1. AI Engine analyzes market (BTC, ETH, BNB)
2. Generates signal (entry, targets, stop)
3. Saves to PostgreSQL
4. Frontend fetches via API
5. Displays to user
6. (Future) User pays $0.10 in LEVE
7. (Future) Contract records payment
8. (Future) Signal unlocked
```

### Payment Flow (Future)

```
1. User clicks "Unlock Signal"
2. MetaMask opens
3. User approves $0.10 LEVE transfer
4. ERC-8183 contract processes payment
5. 90% → Treasury, 10% → Buyback
6. Signal unlocked for user
7. Transaction recorded on BSC
```

---

## Security

### Implemented

- ✅ JWT authentication
- ✅ Password hashing (bcrypt)
- ✅ CORS restrictions
- ✅ Rate limiting
- ✅ Helmet security headers
- ✅ Environment variables (.env)
- ✅ PostgreSQL Row Level Security (planned)

### Best Practices

- Never commit .env files
- Use hardware wallets for contract deployment
- Implement multisig for treasury
- Regular security audits
- Bug bounty program (planned)

---

## Deployment

### Current Setup

```
Server: Ubuntu 22.04 LTS
CPU: Multi-core
RAM: 16GB+
Storage: 200GB SSD

Services:
- Nginx (reverse proxy)
- PM2 (process manager)
- PostgreSQL (database)
- Node.js (backend)
- Next.js (frontend)
- Python Flask (AI engine)
```

### Deployment Commands

```bash
# Frontend
cd /opt/leveclaw/frontend
npm run build
pm2 restart leveclaw-frontend

# Backend
cd /opt/leveclaw/backend
pm2 restart leveclaw-backend

# AI Engine
cd /root/openclaw/alpha_signals
python3 api_server.py

# Nginx
sudo systemctl reload nginx
```

---

## Monitoring

### Current

- PM2 logs
- Manual BSCScan checks
- User feedback

### Planned

- Uptime monitoring
- Error tracking (Sentry)
- Analytics (Google Analytics)
- Performance monitoring

---

**Last Updated:** March 12, 2026  
**Version:** 1.0.0  
**Maintained by:** Renato Abreu (CEO)
