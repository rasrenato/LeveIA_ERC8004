#!/usr/bin/env node
const https = require('https');

const ACTIVE_TESTERS = [
  { nome: 'Weberson', whatsapp: '5568992243049' },
  { nome: 'Helcio', whatsapp: '5531988169949' },
  { nome: 'Joao', whatsapp: '351967443258' },
  { nome: 'Julio', whatsapp: '5521965821439' }  // ✅ ADICIONADO: Feedback que gerou a correção USDC→USDT
];

const msg = `Bom dia! Leve IA aqui.

Atualizamos a plataforma com base no feedback de voces!

- Tela de pagamento mais clara
- Passo-a-passo explicativo
- Textos corrigidos (USDT BEP-20)

Link: https://app.leve.app.br/dashboard/alpha-signals

Consegue ver e me dizer se ficou mais claro?

Valeu!`;

function send(t, i) {
  return new Promise((ok) => {
    const d = JSON.stringify({ 
      phone: t.whatsapp, 
      message: `${msg}\n\n${t.nome}, conto com voce!`,
      schedule: 0
    });
    const r = https.request({
      hostname: 'api.z-api.io',
      port: 443,
      path: `/instances/3EB8E31B693F716D7D768EC56ABBB73A/token/B4233433A81BCA7E8F3CE6EA/send-text`,
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json', 
        'Content-Length': d.length,
        'client-token': 'F7e88834ec491402cb29fde076b05a68fS'
      }
    }, (res) => {
      let b = '';
      res.on('data', (c) => b += c);
      res.on('end', () => {
        console.log(`${res.statusCode === 200 ? '✅' : '❌'} ${t.nome} - ${res.statusCode}`);
        console.log('Response:', b);
        ok(res.statusCode === 200);
      });
    });
    r.on('error', (e) => { console.log(`❌ ${t.nome} - ${e.message}`); ok(false); });
    r.write(d);
    r.end();
  });
}

(async () => {
  console.log('🚀 Enviando upsell...\n');
  let ok = 0;
  for (let i = 0; i < ACTIVE_TESTERS.length; i++) {
    if (await send(ACTIVE_TESTERS[i], i)) ok++;
    if (i < ACTIVE_TESTERS.length - 1) await new Promise(r => setTimeout(r, 2000));
  }
  console.log(`\n✅ ${ok}/3\n`);
})();
