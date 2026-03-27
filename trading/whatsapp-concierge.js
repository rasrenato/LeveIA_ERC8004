#!/usr/bin/env node
/**
 * WhatsApp Concierge - Leve IA DeFAI Protocol
 * 
 * Novo modelo: Concierge Web3 (não vendedor)
 * 
 * Gatilhos:
 * 1. ALERTA DE SINAL - Quando BTC/ETH chega na Zona de Entrada
 * 2. COMEMORAÇÃO DE WIN - Quando TP1 é batido
 * 3. AFILIADOS - Lembrete de 30% de comissão em USDT
 * 
 * Zero Telegram - 100% WhatsApp (Z-API)
 */

const https = require('https');

// Configuração Z-API
const ZAPI_CONFIG = {
  hostname: 'api.z-api.io',
  port: 443,
  path_base: '/instances/3EB8E31B693F716D7D768EC56ABBB73A/token/B4233433A81BCA7E8F3CE6EA/send-text',
  client_token: 'F7e88834ec491402cb29fde076b05a68fS', // TODO: Substituir pelo token oficial
};

/**
 * Enviar mensagem WhatsApp via Z-API
 */
async function sendWhatsApp(phone, message) {
  return new Promise((resolve) => {
    const data = JSON.stringify({ phone, message });
    
    const req = https.request({
      hostname: ZAPI_CONFIG.hostname,
      port: ZAPI_CONFIG.port,
      path: ZAPI_CONFIG.path_base,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(data, 'utf8'),
        'client-token': ZAPI_CONFIG.client_token,
      },
    }, (res) => {
      let body = '';
      res.on('data', (chunk) => body += chunk);
      res.on('end', () => {
        const success = res.statusCode === 200;
        console.log(`[${success ? '✅' : '❌'}] ${phone} - ${res.statusCode}`);
        resolve(success);
      });
    });
    
    req.on('error', (e) => {
      console.log(`[❌] ${phone} - ${e.message}`);
      resolve(false);
    });
    
    req.write(data);
    req.end();
  });
}

/**
 * TEMPLATE 1: ALERTA DE SINAL
 * Quando BTC/ETH chega na Zona de Entrada
 */
function buildSignalAlert(nome, symbol, direction, currentPrice, entryMin, entryMax, tp1, stopLoss) {
  const emoji = direction === 'LONG' ? '🟢' : '🔴';
  const action = direction === 'LONG' ? 'COMPRAR' : 'VENDER';
  
  return `🚨 *ALERTA DE SINAL - LEVE IA* 🚨

${emoji} *${symbol}* - ${direction}

🎯 *OPORTUNIDADE AGORA!*

💰 Preço Atual: *$${currentPrice.toLocaleString('en-US', { minimumFractionDigits: 2 })}*
📊 Zona de Entrada: *$${entryMin.toLocaleString()} - $${entryMax.toLocaleString()}*

✅ *Preço NA ZONA!* Hora de entrar!

📈 *Setup Completo:*
• Alvo 1 (30%): $${tp1.toLocaleString()}
• Stop Loss: $${stopLoss.toLocaleString()}
• Risco/Retorno: 1:2.5+

🔗 *Acessar Sinal Completo:*
https://app.leve.app.br/dashboard/alpha-signals

⚠️ *Lembrete:*
• Use no máximo 2-5% do capital
• Configure ordens automáticas
• Respeite o stop loss!

Qualquer dúvida, tô aqui! 🤖`;
}

/**
 * TEMPLATE 2: COMEMORAÇÃO DE WIN
 * Quando TP1 é batido
 */
function buildWinCelebration(nome, symbol, direction, entryPrice, tp1Price, currentPrice, pnlPercent) {
  return `🎉 *BATUO O ALVO! - LEVE IA* 🎉

✅ *${symbol}* - ${direction}

🎯 *TP1 BATIDO!*

💰 Entrada: *$${entryPrice.toLocaleString()}*
🎯 TP1: *$${tp1Price.toLocaleString()}*
💵 Preço Atual: *$${currentPrice.toLocaleString()}*

📈 *Lucro:* *+${pnlPercent.toFixed(2)}%* 🚀

🏆 *PARABÉNS!* Mais um no bolso!

📱 *Gere seu Card de Lucro:*
1. Acesse: https://app.leve.app.br/dashboard/alpha-signals
2. Clique no sinal
3. Botão "Compartilhar Vitória"
4. Poste nas redes!

🔗 *Seu Link de Afiliado:*
${walletAddress ? `https://app.leve.app.br/dashboard/alpha-signals?ref=${walletAddress}` : '⚠️ Vincule sua carteira nas configurações!'}

💎 *Lembrete:* Você ganha 30% em USDT direto na carteira quando amigos usam seu link!

Compartilhe esse win! 🏆`;
}

/**
 * TEMPLATE 3: AFILIADOS
 * Lembrete de comissão 30%
 * @param {string} nome - Nome do usuário
 * @param {string} walletAddress - Endereço da carteira (0x...)
 * @param {number} commissionsEarned - Comissões ganhas em USDT (valor REAL do banco)
 * @param {number} totalVolume - Volume total gerado em USDT (valor REAL do banco)
 */
function buildAffiliateReminder(nome, walletAddress, commissionsEarned, totalVolume) {
  // Formatar wallet para exibição (ex: 0x1234...ABCD)
  const walletShort = walletAddress && walletAddress.length > 10 
    ? `${walletAddress.slice(0, 6)}...${walletAddress.slice(-4)}`
    : 'não vinculada';
  
  // Link de afiliado com wallet REAL do usuário
  const affiliateLink = walletAddress 
    ? `https://app.leve.app.br/dashboard/alpha-signals?ref=${walletAddress}`
    : 'https://app.leve.app.br/dashboard/alpha-signals (vincule sua carteira primeiro!)';
  
  return `💎 *OPORTUNIDADE DE AFILIADO - LEVE IA* 💎

👋 Fala ${nome}! Aqui é a IA da Leve.

🎯 *Você Sabia?*

Você pode ganhar *30% em USDT* direto na sua carteira toda vez que um amigo usar seu link!

💰 *Como Funciona:*
1. Copie seu link: ${affiliateLink}
2. Mande para amigos traders
3. Eles pagam $0.99 USDT por sinal
4. Você recebe $0.30 USDT na hora! 💸

👛 *Sua Carteira:* \`${walletShort}\`

📊 *Seus Ganhos Reais:*
• Comissões: *$${commissionsEarned.toFixed(2)} USDT*
• Volume Gerado: *$${totalVolume.toFixed(2)} USDT*

🚀 *Dica:* Compartilhe seus cards de WIN!
Quando bater um alvo, gere o card e poste. Amigos vão perguntar!

🔗 *Acesse seu Dashboard:*
https://app.leve.app.br/dashboard/alpha-signals

Qualquer dúvida, tô aqui! 🤖`;
}

/**
 * TEMPLATE 4: BOAS-VINDAS WEB3
 * Para novos usuários
 */
function buildWeb3Welcome(nome) {
  return `🚀 *BEM-VINDO À LEVE IA!* 🚀

👋 Fala ${nome}! Aqui é seu Concierge Web3.

🎯 *O Que É Leve IA?*

Somos o primeiro protocolo *DeFAI* do mundo!

🤖 IA Analista + Auditor Independente
⛓️ Transparência total via Blockchain
💰 Microtransações Web3 ($0.99 USDT)
🎁 30% de comissão para afiliados

📱 *Como Funciona:*

1️⃣ *Conecte sua Carteira*
   • MetaMask, Trust Wallet ou Rainbow
   • Rede: BSC (Binance Smart Chain)

2️⃣ *Escolha USDT ou LEVE*
   • $0.99 USDT por sinal
   • ou 100 LEVE (mais barato!)

3️⃣ *Receba Sinais Profissionais*
   • Entrada, Alvos, Stop Loss
   • Validação Dupla de IA
   • Preço em tempo real!

4️⃣ *Compartilhe e Ganhe*
   • 30% de comissão em USDT
   • Direto na sua carteira!

🔗 *Acesse Agora:*
https://app.leve.app.br/dashboard/alpha-signals

📚 *Tutorial Completo:*
https://app.leve.app.br/dashboard/tutorial

💡 *Dica:* Tenha um pouco de BNB (~$0.02) para taxa de gás!

Qualquer dúvida, tô aqui 24/7! 🤖`;
}

/**
 * TEMPLATE 5: RECUPERAÇÃO
 * Para usuários inativos
 */
function buildRecoveryMessage(nome, daysInactive, lastSignal) {
  return `👋 *SENTIMOS SUA FALTA - LEVE IA* 👋

🤖 Fala ${nome}! Aqui é seu Concierge Web3.

📅 *Faz ${daysInactive} dias* que você não acessa!

🎯 *O Que Você Perdeu:*

${lastSignal ? `• Último sinal: ${lastSignal.symbol} ${lastSignal.direction}
• Resultado: ${lastSignal.result}
• Lucro: ${lastSignal.pnl}%` : '• Vários sinais profissionais'}

💎 *Lembrete:*
• Apenas $0.99 USDT por sinal
• ou 100 LEVE (promocional!)
• 30% de comissão se indicar amigos

🔗 *Volte Agora:*
https://app.leve.app.br/dashboard/alpha-signals

📱 *Preços em Tempo Real:*
Agora você vê o preço atualizado a cada 10 segundos!

💡 *Dica:* Configure alertas de entrada!

Qualquer dúvida, tô aqui! 🤖`;
}

// Exportar funções
module.exports = {
  sendWhatsApp,
  buildSignalAlert,
  buildWinCelebration,
  buildAffiliateReminder,
  buildWeb3Welcome,
  buildRecoveryMessage,
  ZAPI_CONFIG,
};

// Exemplo de uso (se executado diretamente)
if (require.main === module) {
  console.log('🤖 WhatsApp Concierge - Leve IA DeFAI Protocol');
  console.log('==============================================');
  console.log('');
  console.log('Templates disponíveis:');
  console.log('1. buildSignalAlert() - Alerta de Zona de Entrada');
  console.log('2. buildWinCelebration() - Comemoração de TP1 batido');
  console.log('3. buildAffiliateReminder() - Lembrete de Afiliados');
  console.log('4. buildWeb3Welcome() - Boas-vindas Web3');
  console.log('5. buildRecoveryMessage() - Recuperação de Inativos');
  console.log('');
  console.log('Para usar: require("./whatsapp-concierge.js")');
}
