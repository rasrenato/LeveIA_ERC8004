#!/usr/bin/env node
const https = require('https');

// Teste com mensagem simples SEM emojis
const msg = `Oi Weberson! Tudo bem?

Aqui e Cabral da Leve IA.

Consegue testar o dashboard e me dar feedback ate segunda-feira?

Obrigado!`;

const d = JSON.stringify({ phone: '5568992243049', message: msg });

console.log('Enviando para Weberson (5568992243049)...');
console.log('Message length:', msg.length);
console.log('Payload:', d.substring(0, 100) + '...\n');

const r = https.request({
  hostname: 'api.z-api.io',
  port: 443,
  path: '/instances/3EB8E31B693F716D7D768EC56ABBB73A/token/B4233433A81BCA7E8F3CE6EA/send-text',
  method: 'POST',
  headers: { 
    'Content-Type': 'application/json', 
    'Content-Length': Buffer.byteLength(d, 'utf8'),
    'client-token': 'F7e88834ec491402cb29fde076b05a68fS'
  }
}, (res) => {
  let b = '';
  res.on('data', (c) => b += c);
  res.on('end', () => {
    console.log('Status:', res.statusCode);
    console.log('Response:', b);
  });
});

r.on('error', (e) => { 
  console.log('Error:', e.message); 
});
r.write(d);
r.end();
