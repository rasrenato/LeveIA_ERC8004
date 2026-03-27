#!/usr/bin/env node
const https = require('https');

const TESTERS = [
  { 
    nome: 'Tiago', 
    whatsapp: '351914034708', 
    tipo: 'onboarding',
    msg: `Fala Tiago! Aqui é a IA da Leve.

Te convidando pra um Beta Fechado da nossa plataforma.

É a primeira de sinais com transparência total via blockchain.

UX atualizada:
- Tudo em USDT (BEP-20)
- Passo-a-passo claro antes de pagar
- Gas fee visível (~$0.02)

Link: https://app.leve.app.br/dashboard/alpha-signals

Quero seu feedback sincero como Trader Consciente.

O que tá claro? O que tá confuso?

Consegue testar hoje e me falar?

Valeu!`
  },
  { 
    nome: 'Weberson', 
    whatsapp: '5568992243049', 
    tipo: 'changelog',
    msg: `Fala Weberson! Aqui é a IA da Leve.

Atualização baseada no feedback de vocês:

✅ Saiu USDC, entrou USDT (BEP-20)
✅ Passo a passo claro antes de pagar
✅ Taxa de gás (BNB) agora visível (~$0.02)
✅ Endereço da carteira oficial exibido

Link: https://app.leve.app.br/dashboard/alpha-signals

Entram lá e me falam: a nova UX ficou melhor?

Obrigado pelo feedback que gerou isso! 🙏

Valeu!`
  },
  { 
    nome: 'Helcio', 
    whatsapp: '5531988169949', 
    tipo: 'changelog',
    msg: `Fala Hélcio! Aqui é a IA da Leve.

Atualização baseada no feedback de vocês:

✅ Saiu USDC, entrou USDT (BEP-20)
✅ Passo a passo claro antes de pagar
✅ Taxa de gás (BNB) agora visível (~$0.02)
✅ Endereço da carteira oficial exibido

Link: https://app.leve.app.br/dashboard/alpha-signals

Entram lá e me falam: a nova UX ficou melhor?

Obrigado pelo feedback que gerou isso! 🙏

Valeu!`
  },
  { 
    nome: 'Joao', 
    whatsapp: '351967443258', 
    tipo: 'changelog',
    msg: `Fala João! Aqui é a IA da Leve.

Atualização baseada no feedback de vocês:

✅ Saiu USDC, entrou USDT (BEP-20)
✅ Passo a passo claro antes de pagar
✅ Taxa de gás (BNB) agora visível (~$0.02)
✅ Endereço da carteira oficial exibido

Link: https://app.leve.app.br/dashboard/alpha-signals

Entram lá e me falam: a nova UX ficou melhor?

Obrigado pelo feedback que gerou isso! 🙏

Valeu!`
  },
  { 
    nome: 'Julio', 
    whatsapp: '5521965821439', 
    tipo: 'changelog',
    msg: `Fala Júlio! Aqui é a IA da Leve.

Atualização baseada no feedback de vocês:

✅ Saiu USDC, entrou USDT (BEP-20)
✅ Passo a passo claro antes de pagar
✅ Taxa de gás (BNB) agora visível (~$0.02)
✅ Endereço da carteira oficial exibido

Link: https://app.leve.app.br/dashboard/alpha-signals

Entram lá e me falam: a nova UX ficou melhor?

Obrigado pelo feedback que gerou isso! 🙏

Valeu!`
  }
];

async function send(tester, i) {
  return new Promise((ok) => {
    const data = JSON.stringify({ phone: tester.whatsapp, message: tester.msg });
    const r = https.request({
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
      let b = '';
      res.on('data', (c) => b += c);
      res.on('end', () => {
        console.log(`[${res.statusCode === 200 ? '✅' : '❌'}] ${tester.nome} (${tester.tipo}) - ${res.statusCode}`);
        console.log(`Response: ${b}`);
        ok(res.statusCode === 200);
      });
    });
    r.on('error', (e) => { console.log(`[❌] ${tester.nome} - ${e.message}`); ok(false); });
    r.write(data);
    r.end();
  });
}

(async () => {
  console.log('🚀 Disparando mensagens...\n');
  let ok = 0;
  for (let i = 0; i < TESTERS.length; i++) {
    if (await send(TESTERS[i], i)) ok++;
    if (i < TESTERS.length - 1) await new Promise(r => setTimeout(r, 2000));
  }
  console.log(`\n✅ ${ok}/${TESTERS.length} enviadas\n`);
})();
