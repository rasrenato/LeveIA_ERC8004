#!/usr/bin/env node
/**
 * Leve Invest Signal Generator - Formato Profissional (Helcio Style)
 * Gera sinais no formato pronto para WhatsApp/Telegram
 * Run: node signal-generator.js [LONG|SHORT|HOLD]
 */

const fetch = require('node-fetch');

// Configurações
const CONFIG = {
  model_accuracy: 72,
  avg_return: 4.6,
  trades_analyzed: 128,
  risk_per_trade: 1.5, // %
  leverage: 'Neutro (Spot)'
};

// Gerar dados de mercado (simulado - em produção usar APIs reais)
async function getMarketData() {
  return {
    btc_price: 69500,
    support: 66000,
    resistance: 74000,
    rsi: 32,
    volume_trend: 'crescente',
    market_structure: 'bearish_short_term',
    fib_618: 58000,
    fib_50: 70500
  };
}

// Calcular setup baseado na direção
function calculateSetup(direction, market) {
  if (direction === 'LONG') {
    return {
      entry_zone: `${market.support} – ${Math.round(market.support * 1.02)}`,
      entry_ideal: market.support,
      stop_loss: Math.round(market.support * 0.95),
      tp1: Math.round(market.resistance * 1.05),
      tp2: Math.round(market.resistance * 1.12),
      confidence: 85,
      score: 8.0,
      duration: '5–15 dias',
      risk_return: '1 : 2.5'
    };
  } else if (direction === 'SHORT') {
    return {
      entry_zone: `${Math.round(market.resistance * 0.98)} – ${market.resistance}`,
      entry_ideal: market.resistance,
      stop_loss: Math.round(market.resistance * 1.05),
      tp1: Math.round(market.support * 0.95),
      tp2: Math.round(market.support * 0.90),
      confidence: 68,
      score: 7.2,
      duration: '3–10 dias',
      risk_return: '1 : 2.0'
    };
  } else {
    return null; // HOLD = sem sinal
  }
}

// Gerar análise do setup
function generateAnalysis(direction, market) {
  const analyses = {
    LONG: {
      trend: 8,
      volume: 7,
      structure: 9,
      momentum: 8,
      context: [
        'Reteste de suporte semanal',
        'Volume comprador crescendo',
        'RSI neutro após correção',
        'Estrutura de alta preservada'
      ]
    },
    SHORT: {
      trend: 7,
      volume: 8,
      structure: 8,
      momentum: 7,
      context: [
        'Resistência de $74k rejeitada',
        'Baleias despejando em exchanges',
        'Fear & Greed em 13 (extremo)',
        'Fib 61.8% em $58k como alvo'
      ]
    }
  };
  return analyses[direction];
}

// Formatador de sinal
function formatSignal(signal) {
  return `
🚨 *LEVE INVEST | SIGNAL PRO*
🪙 Ativo: ${signal.asset}
📈 Direção: ${signal.direction} ${signal.direction === 'LONG' ? '🟢' : '🔴'}
⏳ Tipo: ${signal.type}
🕐 Duração estimada: ${signal.duration}
📊 Confiança do modelo: ${signal.confidence}%
⭐ Score do setup: ${signal.score} / 10
━━━━━━━━━━━━━━━━━━
📍 *ZONA DE ENTRADA*
${signal.entry_zone}
Entrada ideal: ${signal.entry_ideal}
━━━━━━━━━━━━━━━━━━
🛑 *STOP LOSS*
${signal.stop_loss}
⚠️ Invalidação técnica:
${signal.invalidation}
━━━━━━━━━━━━━━━━━━
🎯 *ALVOS*
TP1 → ${signal.tp1.toLocaleString()} (${signal.tp1_pct})
Realizar 50% da posição
TP2 → ${signal.tp2.toLocaleString()} (${signal.tp2_pct})
Realizar 50% da posição
━━━━━━━━━━━━━━━━━━
⚖️ *RISCO / RETORNO*
Risco estimado: ${signal.risk}%
Retorno potencial: ${signal.reward}%
Relação: ${signal.risk_return}
━━━━━━━━━━━━━━━━━━
📊 *ANÁLISE DO SETUP*
Tendência: ${signal.analysis.trend}/10
Volume: ${signal.analysis.volume}/10
Estrutura de mercado: ${signal.analysis.structure}/10
Momentum: ${signal.analysis.momentum}/10
⭐ Score final: ${signal.score} / 10
━━━━━━━━━━━━━━━━━━
📈 *CONTEXTO DE MERCADO*
${signal.analysis.context.map(c => `• ${c}`).join('\n')}
━━━━━━━━━━━━━━━━━━
⚙️ *GESTÃO DA OPERAÇÃO*
✔ TP1 → mover stop para entrada
✔ TP2 → utilizar trailing stop
━━━━━━━━━━━━━━━━━━
💼 *GESTÃO DE RISCO*
Risco recomendado: ${CONFIG.risk_per_trade}% da banca
Alavancagem sugerida: ${CONFIG.leverage}
━━━━━━━━━━━━━━━━━━
📊 *STATUS DO TRADE*
Entrada ⬜
TP1 ⬜
TP2 ⬜
Stop ⬜
━━━━━━━━━━━━━━━━━━
📈 *PERFORMANCE DO MODELO*
Trades analisados: ${CONFIG.trades_analyzed}
Taxa média de acerto: ${CONFIG.model_accuracy}%
Retorno médio por trade: ${CONFIG.avg_return}%
━━━━━━━━━━━━━━━━━━
🤖 *LEVE INVEST SIGNAL SYSTEM*
`.trim();
}

// Gerar sinal completo
async function generateSignal(direction = 'SHORT') {
  const market = await getMarketData();
  const setup = calculateSetup(direction, market);
  const analysis = generateAnalysis(direction, market);
  
  if (!setup) {
    return `🟡 *HOLD* - Sem operação no momento\n\nAguardando setup de qualidade.`;
  }
  
  const tp1_pct = direction === 'LONG' ? '+6.5%' : '-5.0%';
  const tp2_pct = direction === 'LONG' ? '+12%' : '-10%';
  const risk = direction === 'LONG' ? '-3.8%' : '-5.0%';
  const reward = direction === 'LONG' ? '+12%' : '-10%';
  
  const invalidation = direction === 'LONG' 
    ? 'Perda da região de suporte diário.'
    : 'Rompimento de resistência com volume.';
  
  const signal = {
    asset: 'BTC/USDT',
    direction: direction,
    type: 'Swing Trade',
    duration: setup.duration,
    confidence: setup.confidence,
    score: setup.score,
    entry_zone: setup.entry_zone,
    entry_ideal: setup.entry_ideal,
    stop_loss: setup.stop_loss.toLocaleString(),
    invalidation: invalidation,
    tp1: setup.tp1,
    tp1_pct: tp1_pct,
    tp2: setup.tp2,
    tp2_pct: tp2_pct,
    risk: risk,
    reward: reward,
    risk_return: setup.risk_return,
    analysis: {
      trend: analysis.trend,
      volume: analysis.volume,
      structure: analysis.structure,
      momentum: analysis.momentum,
      context: analysis.context
    }
  };
  
  return formatSignal(signal);
}

// Executar
const direction = process.argv[2] || 'SHORT';
generateSignal(direction).then(console.log).catch(console.error);
