#!/usr/bin/env node
const https = require('https');
const fs = require('fs');

// Carrega testers ativos do JSON atualizado
const data = JSON.parse(fs.readFileSync('/root/openclaw/trading/testers-ativos.json', 'utf8'));
const TESTERS = data.testersAtivos;

const msg = `Oi {NOME}! Tudo bem?

Que bom que voce esta usando o Alpha Signals!

Estamos lancando o plano premium:
- Sinais ilimitados
- Analise completa (entrada, alvo, stop, R/R)
- Suporte prioritario

De R$99/mes por R$49/mes (fundadores).

Quer conhecer? E so responder aqui!

Obrigado!`;

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
  console.log('🚀 Enviando upsell para testers ativos...\n');
  console.log(`Total: ${TESTERS.length} testers\n`);
  
  let ok = 0;
  for (let i = 0; i < TESTERS.length; i++) {
    const t = TESTERS[i];
    console.log(`[${i+1}/${TESTERS.length}] Enviando para ${t.nome}...`);
    if (await send(t)) ok++;
    if (i < TESTERS.length - 1) {
      console.log('   Aguardando 2s...\n');
      await new Promise(r => setTimeout(r, 2000));
    }
  }
  
  console.log(`\n📊 Resultado: ${ok}/${TESTERS.length} enviados com sucesso\n`);
  
  if (ok === TESTERS.length) {
    console.log('🎉 Todos os testers receberam a mensagem de upsell!');
  } else {
    console.log('⚠️ Alguns falharam - verificar logs acima');
  }
})();
