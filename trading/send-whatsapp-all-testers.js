#!/usr/bin/env node
const https = require('https');

const TESTERS = [
  { nome: 'Weberson', whatsapp: '5568992243049' },
  { nome: 'Joelson', whatsapp: '5527992932935' },
  { nome: 'Helcio', whatsapp: '5531988169949' },
  { nome: 'Joao', whatsapp: '351967443258' },
  { nome: 'Sam', whatsapp: '5511961749960' },
  { nome: 'Ronaldo', whatsapp: '5532988751905' },
  { nome: 'Reinaldo', whatsapp: '5521973426651' },
  { nome: 'Luciano', whatsapp: '5537988362930' }
];

const msg = `Bom dia! Leve IA aqui.

Ontem atualizamos:
- 5 contratos verificados BSC
- Seguranca blindada
- Frontend novo

Link: https://app.leve.app.br

Consegue testar e dar feedback ate segunda?

Valeu!`;

function send(t, i) {
  return new Promise((ok) => {
    const d = JSON.stringify({ phone: t.whatsapp, message: `${msg}\n\n${t.nome}, conto com voce!` });
    const r = https.request({
      hostname: 'api.z-api.io',
      port: 443,
      path: '/instances/3EB8E31B693F716D7D768EC56ABBB73A/token/B4233433A81BCA7E8F3CE6EA/send-text',
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
        ok(res.statusCode === 200);
      });
    });
    r.on('error', (e) => { console.log(`❌ ${t.nome} - ${e.message}`); ok(false); });
    r.write(d);
    r.end();
  });
}

(async () => {
  console.log('🚀 Enviando...\n');
  let ok = 0;
  for (let i = 0; i < TESTERS.length; i++) {
    if (await send(TESTERS[i], i)) ok++;
    if (i < TESTERS.length - 1) await new Promise(r => setTimeout(r, 2000));
  }
  console.log(`\n✅ ${ok}/8\n`);
})();
