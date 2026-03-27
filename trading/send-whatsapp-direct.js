#!/usr/bin/env node
/**
 * Envia WhatsApp direto via Z-API (sem n8n)
 * Run: node send-whatsapp-direct.js
 */

const https = require('https');

// Configurações Z-API
const ZAPI_CONFIG = {
  instance: '3EB8E31B693F716D7D768EC56ABBB73A',
  token: 'B4233433A81BCA7E8F3CE6EA',
  // client-token precisa ser configurado
  clientToken: 'F7e88834ec491402cb29fde076b05a68fS'
};

// Lista de testers
const TESTERS = [
  { nome: 'Weberson', email: 'weberson18@yahoo.com.br', whatsapp: '5568992243049' },
  { nome: 'Joelson', email: 'joelson.samora1977@gmail.com', whatsapp: '5527992932935' },
  { nome: 'Helcio', email: 'helciojose@hotmail.com', whatsapp: '5531988169949' },
  { nome: 'João', email: 'joao_pereira1963@hotmail.com', whatsapp: '351967443258' },
  { nome: 'Sam', email: 'samuelmonteirodesousa663@gmail.com', whatsapp: '5511961749960' },
  { nome: 'Ronaldo', email: 'rnader2@yahoo.com.br', whatsapp: '5532988751905' },
  { nome: 'Reinaldo', email: 'santosreinaldo04958@gmail.com', whatsapp: '5521973426651' },
  { nome: 'Luciano', email: 'lucianorobsonm@gmail.com', whatsapp: '5537988362930' }
];

function sendMessage(tester) {
  return new Promise((resolve, reject) => {
    const message = `🚀 ${tester.nome}! Aqui é Alpha Signals IA!

Seu acesso tá LIBERADO!

📧 Email: ${tester.email}
🔑 Senha: AlphaTest2026!
🌐 Link: https://app.leve.app.br

Consegue acessar hoje? (15 min)

Bug do Reinaldo já corrigido! ✅

Qualquer dúvida, tô aqui! 🤖`;

    const data = JSON.stringify({
      phone: tester.whatsapp,
      message: message
    });

    const options = {
      hostname: 'api.z-api.io',
      port: 443,
      path: `/instances/${ZAPI_CONFIG.instance}/token/${ZAPI_CONFIG.token}/send-text`,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': data.length,
        ...(ZAPI_CONFIG.clientToken && { 'client-token': ZAPI_CONFIG.clientToken })
      }
    };

    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', (chunk) => body += chunk);
      res.on('end', () => {
        console.log(`✅ ${tester.nome}: ${res.statusCode} - ${body}`);
        resolve({ tester, status: res.statusCode, response: body });
      });
    });

    req.on('error', (error) => {
      console.log(`❌ ${tester.nome}: ${error.message}`);
      reject(error);
    });

    req.write(data);
    req.end();
  });
}

async function sendAll() {
  console.log('🚀 Iniciando envio de mensagens...\n');
  
  const results = [];
  for (const tester of TESTERS) {
    try {
      const result = await sendMessage(tester);
      results.push(result);
      // Delay entre mensagens
      await new Promise(resolve => setTimeout(resolve, 1000));
    } catch (error) {
      results.push({ tester, error: error.message });
    }
  }
  
  console.log('\n📊 Resumo:');
  console.log(`Enviados: ${results.filter(r => r.status === 200).length}`);
  console.log(`Falhas: ${results.filter(r => r.error || r.status !== 200).length}`);
}

sendAll().catch(console.error);
