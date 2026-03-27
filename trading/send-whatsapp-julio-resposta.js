#!/usr/bin/env node
const https = require('https');

const message = `Fala Julio! Boa pergunta!

Sim, exato! Pra desbloquear os sinais voce precisa:

1. Ter USDC na carteira (nao é USDT, é USDC mesmo)
2. Valor: 0.10 USDC por sinal (mais gas fee da BSC, barato)
3. Enviar pra: 0x077e8d29e11ff1c0ccb236e0380d0053dcba2b1c
4. Colar o hash da transacao no dashboard
5. Click em Unlock Signal

Dica: Gas fee na BSC é uns $0.01-0.02!

A gente ta melhorando a UX pra ficar mais claro. Seu feedback ajudou!

Qualquer duvida, to aqui! Valeu!`;

const data = JSON.stringify({
  phone: '5521965821439',
  message: message
});

const req = https.request({
  hostname: 'api.z-api.io',
  port: 443,
  path: '/instances/3EB8E31B693F716D7D768EC56ABBB73A/token/B4233433A81BCA7E8F3CE6EA/send-text',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Content-Length': data.length
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
