#!/usr/bin/env node
const https = require('https');

// MENSAGEM COMPLETA COM EMOJIS (como no script original)
const msg = `Fala Renato! Aqui é a IA da Leve.

Atualização baseada no feedback de vocês:

✅ Saiu USDC, entrou USDT (BEP-20)
✅ Passo a passo claro antes de pagar
✅ Taxa de gás (BNB) agora visível (~$0.02)
✅ Endereço da carteira oficial exibido

Link: https://app.leve.app.br/dashboard/alpha-signals

Entram lá e me falam: a nova UX ficou melhor?

Obrigado pelo feedback que gerou isso! 🙏

Valeu!`;

const data = JSON.stringify({ 
  phone: '5521965821439', 
  message: msg 
});

console.log('Payload size:', data.length, 'bytes');
console.log('Contains emojis:', msg.includes('✅') || msg.includes('🙏'));
console.log('Contains accents:', msg.includes('é') || msg.includes('ã') || msg.includes('á'));

const req = https.request({
  hostname: 'api.z-api.io',
  port: 443,
  path: '/instances/3EB8E31B693F716D7D768EC56ABBB73A/token/B4233433A81BCA7E8F3CE6EA/send-text',
  method: 'POST',
  headers: { 
    'Content-Type': 'application/json', 
    'Content-Length': Buffer.byteLength(data, 'utf8'),
    'client-token': 'F7e88834ec491402cb29fde076b05a68fS'
  }
}, (res) => {
  let body = '';
  res.on('data', (chunk) => body += chunk);
  res.on('end', () => {
    console.log('\n=== RESPONSE ===');
    console.log('Status:', res.statusCode);
    console.log('Body:', body);
  });
});

req.on('error', (e) => {
  console.log('\n=== ERROR ===');
  console.error('Error:', e.message);
});

req.write(data);
req.end();
