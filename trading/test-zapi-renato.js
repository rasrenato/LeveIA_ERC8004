#!/usr/bin/env node
const https = require('https');

// Teste minimalista - SEM EMOJIS, SEM ACENTOS
const msg = `Fala Renato! Aqui é a IA da Leve.

Teste de conexao Z-API.

UX atualizada: USDT (BEP-20), passo-a-passo, gas fee visivel.

Link: https://app.leve.app.br/dashboard/alpha-signals

Feedback?

Valeu!`;

const data = JSON.stringify({ 
  phone: '5521965821439', 
  message: msg 
});

console.log('Payload size:', data.length, 'bytes');
console.log('Payload preview:', data.substring(0, 100));

const req = https.request({
  hostname: 'api.z-api.io',
  port: 443,
  path: '/instances/3EB8E31B693F716D7D768EC56ABBB73A/token/B4233433A81BCA7E8F3CE6EA/send-text',
  method: 'POST',
  headers: { 
    'Content-Type': 'application/json', 
    'Content-Length': data.length,
    'client-token': 'F7e88834ec491402cb29fde076b05a68fS'
  }
}, (res) => {
  let body = '';
  res.on('data', (chunk) => body += chunk);
  res.on('end', () => {
    console.log('\n=== RESPONSE ===');
    console.log('Status:', res.statusCode);
    console.log('Headers:', JSON.stringify(res.headers, null, 2));
    console.log('Body:', body);
  });
});

req.on('error', (e) => {
  console.log('\n=== ERROR ===');
  console.error('Error:', e.message);
});

req.write(data);
req.end();
