# Leve IA Alpha Signals API Documentation

## 🚀 Overview

Leve IA Alpha Signals API provides real-time BTC, ETH, and BNB predictions via x402 pay-per-use protocol on Base network.

**Base URL:** `https://api.coinmarketleve.com`

**Price:** $0.10 USDC per signal

**Merchant Wallet:** `0x077e8d29e11ff1c0ccb236e0380d0053dcba2b1c`

**Network:** Base (Ethereum L2)

## 📡 Endpoints

### 1. Get Service Info
```
GET /
```

**Response:**
```json
{
  "service": "Alpha Engine x402 API",
  "version": "1.0.0",
  "description": "Venda de sinais do Alpha Engine usando protocolo x402",
  "price": "$0.1 USDC",
  "wallet": "0x077e8d29e11ff1c0ccb236e0380d0053dcba2b1c",
  "network": "Base"
}
```

### 2. Health Check
```
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": 1770940469,
  "web3_connected": true
}
```

### 3. Get Prediction Sample (Free)
```
GET /prediction-sample
```

**Response:**
```json
{
  "last_update": 1770897612,
  "assets": ["BTC", "ETH", "BNB"],
  "sample_prediction": {
    "asset": "BTC",
    "current_price": 68500,
    "bias": "LONG_BIAS",
    "probability": 0.88
  }
}
```

### 4. Get Full Predictions (Paid)
```
POST /alpha-prediction
```

**Parameters (form data or query params):**
- `tx_hash` (string): **Required** - Transaction hash of USDC payment
- `user_address` (string): **Required** - Address that sent the payment

**Payment Requirements:**
- Amount: ≥ $0.10 USDC
- Destination: `0x077e8d29e11ff1c0ccb236e0380d0053dcba2b1c`
- Network: Base
- Time window: Within last 5 minutes

**Response (Success):**
```json
{
  "success": true,
  "predictions": {
    "last_update": 1770897612,
    "predictions": [
      {
        "asset": "BTC",
        "current_price": 68500,
        "analysis": {
          "bias": "LONG_BIAS",
          "probability": 0.88,
          "scenarios": ["bullish_continuation", "consolidation"],
          "deep_reasoning": "Technical analysis indicates..."
        }
      },
      {
        "asset": "ETH",
        "current_price": 3850,
        "analysis": {
          "bias": "NEUTRAL_BIAS",
          "probability": 0.72,
          "scenarios": ["range_bound", "breakout"],
          "deep_reasoning": "Market structure shows..."
        }
      },
      {
        "asset": "BNB",
        "current_price": 620,
        "analysis": {
          "bias": "SHORT_BIAS",
          "probability": 0.65,
          "scenarios": ["correction", "support_test"],
          "deep_reasoning": "Volume profile suggests..."
        }
      }
    ]
  },
  "timestamp": 1770940469
}
```

**Response (Payment Required - 402):**
```json
{
  "detail": "Payment verification failed: Transaction not found or insufficient amount"
}
```

## 💰 Payment Flow

### Step 1: Send USDC Payment
Send ≥ $0.10 USDC to the merchant wallet on Base network:
- **Wallet:** `0x077e8d29e11ff1c0ccb236e0380d0053dcba2b1c`
- **Network:** Base
- **Token:** USDC (Contract: `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`)

### Step 2: Call API with Payment Proof
```bash
curl -X POST "https://api.coinmarketleve.com/alpha-prediction" \
  -d "tx_hash=0x1234..." \
  -d "user_address=0x5678..."
```

### Step 3: Receive Predictions
If payment is verified (within 5 minutes, correct amount), you'll receive the full predictions.

## 🐍 Python Example

```python
import requests

# Step 1: User sends USDC payment to merchant wallet
# (This happens in the user's wallet)

# Step 2: After payment, call API
tx_hash = "0x1234567890abcdef..."  # From user's wallet
user_address = "0xabcdef1234567890..."  # User's wallet address

response = requests.post(
    "https://api.coinmarketleve.com/alpha-prediction",
    data={"tx_hash": tx_hash, "user_address": user_address}
)

if response.status_code == 200:
    predictions = response.json()
    print(f"BTC Prediction: {predictions['predictions'][0]['analysis']['bias']}")
    print(f"Probability: {predictions['predictions'][0]['analysis']['probability']*100}%")
elif response.status_code == 402:
    print("Payment required or verification failed")
else:
    print(f"Error: {response.status_code}")
```

## 🔧 JavaScript Example

```javascript
async function getAlphaPredictions(txHash, userAddress) {
  const response = await fetch('https://api.coinmarketleve.com/alpha-prediction', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: new URLSearchParams({
      tx_hash: txHash,
      user_address: userAddress
    })
  });
  
  if (response.status === 200) {
    const data = await response.json();
    return data.predictions;
  } else if (response.status === 402) {
    throw new Error('Payment required or verification failed');
  } else {
    throw new Error(`API error: ${response.status}`);
  }
}
```

## 🛡️ Error Handling

| Status Code | Description |
|-------------|-------------|
| 200 | Success - Predictions returned |
| 400 | Bad request - Missing parameters |
| 402 | Payment required - Payment verification failed |
| 404 | Not found - Endpoint or prediction file not found |
| 500 | Server error - Internal server error |

## 🔗 Links

- **Interactive Documentation:** https://api.coinmarketleve.com/docs
- **Dashboard:** https://coinmarketleve.com
- **GitHub:** https://github.com/rasrenato/LeveIA_ERC8004 (Private)
- **ERC-8004 Contract:** `0x2333cBC71805b47D64C2867Ef66682c7257B5D4f`

## 📞 Support

For API issues or questions, contact @rasrenato on Telegram.

---

**Last Updated:** February 12, 2026  
**API Version:** 1.0.0  
**Precision:** 88.4% (verified on-chain via ERC-8004)