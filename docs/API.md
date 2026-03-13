# Leve IA - API Documentation

**Complete API reference for Leve IA platform**

---

## Base URL

```
Production: https://app.leve.app.br/api
Development: http://localhost:3002/api
```

---

## Authentication

Most endpoints require JWT authentication.

### Login

```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "success": true,
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "uuid",
    "email": "user@example.com"
  }
}
```

### Use Token

Include in headers:
```
Authorization: Bearer <token>
```

---

## Alpha Signals

### Get BTC Price

```http
GET /api/alpha-signals/btc-price
```

**Response:**
```json
{
  "success": true,
  "data": {
    "price": 70080,
    "change_24h": -0.539,
    "high_24h": 71321,
    "low_24h": 69205.91,
    "volume_24h": 24433.25,
    "quote_volume_24h": 1714833240.57,
    "timestamp": "2026-03-12T16:30:13.305Z",
    "source": "Binance"
  }
}
```

### Get Contracts

```http
GET /api/alpha-signals/contracts
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "name": "ERC-8183 (Alpha Signals)",
      "address": "0xcf0520e60ad602454f06Cd80f588634A332d169d",
      "network": "BSC (Binance Smart Chain)",
      "function": "Sinais pagos on-chain (x402)",
      "color": "emerald",
      "bscscan": "https://bscscan.com/address/0xcf0520e60ad602454f06Cd80f588634A332d169d"
    }
    // ... more contracts
  ]
}
```

### Get Signals

```http
GET /api/alpha-signals/signals?limit=10
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "uuid",
      "symbol": "BTC/USDT",
      "direction": "LONG",
      "entry": 88000,
      "targets": [95000, 100000],
      "stop_loss": 85000,
      "confidence": 85,
      "status": "active",
      "pnl": -2.5,
      "created_at": "2026-03-12T10:00:00Z"
    }
  ]
}
```

### Save Signal (Internal)

```http
POST /api/alpha-signals/save-internal
Content-Type: application/json

{
  "symbol": "BTC/USDT",
  "direction": "LONG",
  "entry_min": 88000,
  "entry_max": 90000,
  "targets": [95000, 100000],
  "stop_loss": 85000,
  "confidence": 85
}
```

---

## Analytics

### Get Dashboard Analytics

```http
GET /api/analytics/dashboard
Authorization: Bearer <token>
```

**Response:**
```json
{
  "success": true,
  "data": {
    "totalSignals": 128,
    "winRate": 72,
    "avgReturn": 4.6,
    "pnlChart": [...],
    "winLossByMonth": [...]
  }
}
```

---

## Users

### Get Profile

```http
GET /api/users/me
Authorization: Bearer <token>
```

**Response:**
```json
{
  "success": true,
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "name": "User Name",
    "created_at": "2026-01-01T00:00:00Z"
  }
}
```

---

## Error Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 429 | Too Many Requests |
| 500 | Internal Server Error |

---

## Rate Limits

- **Default:** 100 requests per 15 minutes
- **Auth endpoints:** 10 requests per minute
- **Signal endpoints:** 60 requests per minute

---

**Last Updated:** March 12, 2026  
**Version:** 1.0.0
