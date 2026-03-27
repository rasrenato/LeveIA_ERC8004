#!/usr/bin/env node
const https = require('https');

const message = `Fala Julio! Tudo certo?

Te convidando pra testar a Leve IA antes do lancamento.

Link: https://app.leve.app.br

Eh o primeiro sistema de sinais de IA com transparencia via blockchain.

Consegue testar e me dar feedback ate segunda?

Valeu!`;

const data = JSON.stringify({
  phone: '5521965821439',
  message: message
});

const options = {
  hostname: 'api.z-api.io',
  port: 443,
  path: '/instances/3EB8E31B693F716D7D768EC56ABBB73A/token/B4233433A81BCA7E8F3CE6EA/send-text',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Content-Length': data.length,
    'client-token': 'F7e88834ec491402cb29fde076b05a68fS'
  }
};

const req = https.request(options, (res) => {
  let body = '';
  res.on('data', (chunk) => body += chunk);
  res.on('end', () => {
    console.log('Status:', res.statusCode);
    console.log('Response:', body);
    if (res.statusCode === 200) {
      console.log('\n✅ Mensagem enviada pro Julio com sucesso!');
    }
  });
});

req.on('error', (e) => console.error('Erro:', e.message));
req.write(data);
req.end();
