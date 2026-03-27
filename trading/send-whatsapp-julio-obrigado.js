#!/usr/bin/env node
const https = require('https');

const msg = `Fala Julio!

Vim agradecer pelo feedback sobre USDC vs USDT!

Gracas a voce ja corrigimos tudo!

Link: https://app.leve.app.br/dashboard/alpha-signals

Voce virou testador oficial!

Valeu!`;

const data = JSON.stringify({ phone: '5521965821439', message: msg });

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
    console.log('Status:', res.statusCode);
    console.log('Response:', body);
  });
});

req.on('error', (e) => console.error('Erro:', e.message));
req.write(data);
req.end();
