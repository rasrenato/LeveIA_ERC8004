#!/usr/bin/env node
const https = require('https');

// Testers inativos (sem uso há 48h+)
const INACTIVE_TESTERS = [
  { nome: "Joelson", whatsapp: "5527992932935" },
  { nome: "João", whatsapp: "351967443258" },
  { nome: "Sam", whatsapp: "5511961749960" },
  { nome: "Ronaldo", whatsapp: "5532988751905" },
  { nome: "Reinaldo", whatsapp: "5521973426651" }
];

const msg = `Oi {NOME}, tudo bem? 🍃

Vi que você testou o Alpha Signals mas não voltou mais.

Posso te ajudar com algo? Alguma dúvida sobre os sinais?

Se quiser, posso te mostrar os últimos resultados (temos 78% de acerto essa semana).

É só me avisar! 😊`;

function send(tester) {
  return new Promise((ok) => {
    const message = msg.replace('{NOME}', tester.nome);
    const d = JSON.stringify({ phone: tester.whatsapp, message: message });
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
        const status = res.statusCode === 200 ? '✅' : '❌';
        console.log(`${status} ${tester.nome} (${tester.whatsapp}) - ${res.statusCode}`);
        if (res.statusCode !== 200) console.log(`   Response: ${b}`);
        ok(res.statusCode === 200);
      });
    });
    r.on('error', (e) => { 
      console.log(`❌ ${tester.nome} - ${e.message}`); 
      ok(false); 
    });
    r.write(d);
    r.end();
  });
}

(async () => {
  console.log('🚀 Follow-up: Testers Inativos - Alpha Signals\n');
  console.log(`Total: ${INACTIVE_TESTERS.length} testers\n`);
  
  let ok = 0;
  for (let i = 0; i < INACTIVE_TESTERS.length; i++) {
    const t = INACTIVE_TESTERS[i];
    console.log(`[${i+1}/${INACTIVE_TESTERS.length}] Enviando para ${t.nome}...`);
    if (await send(t)) ok++;
    if (i < INACTIVE_TESTERS.length - 1) {
      console.log('   Aguardando 2s...\n');
      await new Promise(r => setTimeout(r, 2000));
    }
  }
  
  console.log(`\n📊 Resultado: ${ok}/${INACTIVE_TESTERS.length} enviados com sucesso\n`);
  
  if (ok === INACTIVE_TESTERS.length) {
    console.log('🎉 Todos os testers inativos receberam follow-up!');
  } else {
    console.log('⚠️ Alguns falharam - verificar logs acima');
  }
})();
