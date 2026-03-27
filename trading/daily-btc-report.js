#!/usr/bin/env node
/**
 * Daily BTC Report Generator
 * Generates a daily market analysis report using 4 sources
 * Run: node daily-btc-report.js
 */

const fetch = require('node-fetch');

// Config
const OUTPUT_FILE = '/root/openclaw/trading/logs/daily-report.md';
const TELEGRAM_CHANNEL = '@AlphaSignalsIA'; // Se tiver canal

// 4 Fontes de Dados
async function fetchRealtimeData() {
  // Simulado - em produção usar API da Binance/CoinGecko
  return {
    price: 69500,
    change_24h: -3.2,
    volume_24h: 28500000000,
    etf_flow: -150000000
  };
}

async function fetchWhaleData() {
  // Simulado - em produção usar Glassnode/Whale Alert
  return {
    exchange_whale_ratio: 0.60,
    net_flow_btc: -5000,
    exchange_inflow_usd: 351000000
  };
}

async function fetchSentiment() {
  // Simulado - em produção usar web search
  return {
    fear_greed_index: 13,
    label: 'Extreme Fear'
  };
}

async function fetchTechnical() {
  // Simulado - em produção usar análise técnica real
  return {
    rsi: 32,
    macd: 'bearish',
    support: 66000,
    resistance: 74000,
    fibonacci_618: 58000
  };
}

// Gerar Relatório
async function generateReport() {
  const date = new Date().toISOString().split('T')[0];
  
  const realtime = await fetchRealtimeData();
  const whales = await fetchWhaleData();
  const sentiment = await fetchSentiment();
  const technical = await fetchTechnical();
  
  // Determinar direção
  const bearishSignals = [
    whales.exchange_whale_ratio > 0.5,
    sentiment.fear_greed_index < 30,
    technical.macd === 'bearish',
    realtime.change_24h < 0
  ];
  
  const bearishCount = bearishSignals.filter(s => s).length;
  const direction = bearishCount >= 3 ? 'BEARISH' : bearishCount <= 1 ? 'BULLISH' : 'NEUTRAL';
  const confidence = Math.round((bearishCount / 4) * 100);
  
  const report = `
# 📈 ALPHA SIGNALS - LAUDO BTC DIÁRIO
**Data:** ${date}
**Gerado:** ${new Date().toISOString()}

## 🎯 DIREÇÃO: ${direction === 'BEARISH' ? '🔴' : direction === 'BULLISH' ? '🟢' : '🟡'} ${direction}
**Confiança:** ${confidence}%

---

## 📊 4 FONTES:

### 1. 🐋 Baleias (On-Chain)
- Exchange Whale Ratio: ${whales.exchange_whale_ratio} ${whales.exchange_whale_ratio > 0.5 ? '🔴 (Despejando)' : '🟢 (Acumulando)'}
- Net Flow: ${whales.net_flow_btc} BTC
- Exchange Inflow: $${(whales.exchange_inflow_usd / 1000000).toFixed(0)}M

### 2. 😰 Sentimento
- Fear & Greed: ${sentiment.fear_greed_index} (${sentiment.label})
- ${sentiment.fear_greed_index < 30 ? '🔴 Pânico extremo' : sentiment.fear_greed_index > 70 ? '🟢 Euforia' : '🟡 Neutro'}

### 3. 📉 Técnico
- RSI: ${technical.rsi} ${technical.rsi < 30 ? '(Oversold)' : technical.rsi > 70 ? '(Overbought)' : ''}
- MACD: ${technical.macd}
- Suporte: $${technical.support.toLocaleString()}
- Resistência: $${technical.resistance.toLocaleString()}

### 4. 💰 Tempo Real
- Preço: $${realtime.price.toLocaleString()}
- 24h: ${realtime.change_24h > 0 ? '+' : ''}${realtime.change_24h}%
- Volume: $${(realtime.volume_24h / 1000000000).toFixed(1)}B
- ETF Flow: $${(realtime.etf_flow / 1000000).toFixed(0)}M

---

## 🎯 FIBONACCI (Cycle 2022-2025)
- 61.8%: $${technical.fibonacci_618.toLocaleString()} ⭐ (Alvo principal)
- 50%: $70,500 (Testando)
- 38.2%: $83,000 (Perdido)

---

## 📋 ESTRATÉGIA:

${direction === 'BEARISH' ? `
**AÇÃO:** NÃO COMPRAR AGORA
**ESPERAR:** $${technical.fibonacci_618.toLocaleString()} (Fib 61.8%)
**SHORT:** Considerar se tiver posição aberta
` : direction === 'BULLISH' ? `
**AÇÃO:** COMPRAR GRADUAL
**ENTRY:** $${technical.support.toLocaleString()}
**TARGET:** $${technical.resistance.toLocaleString()}
` : `
**AÇÃO:** AGUARDAR
**WAIT:** Direção clara
**RANGE:** $${technical.support.toLocaleString()} - $${technical.resistance.toLocaleString()}
`}

---

## ⚠️ DISCLAIMER
Isso não é conselho financeiro. Crypto é volátil. Faça sua própria pesquisa.

---
🤖 Alpha Signals IA | Leve Invest
`.trim();

  console.log(report);
  return report;
}

// Executar
generateReport().catch(console.error);
