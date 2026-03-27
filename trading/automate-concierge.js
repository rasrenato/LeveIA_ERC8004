#!/usr/bin/env node
/**
 * Automation - WhatsApp Concierge Triggers
 * 
 * Integra com Result Tracker para disparos automáticos:
 * 1. Quando preço chega na Zona de Entrada → ALERTA
 * 2. Quando TP1 é batido → COMEMORAÇÃO
 * 3. A cada 7 dias → LEMBRETE DE AFILIADOS
 */

const { 
  sendWhatsApp, 
  buildSignalAlert, 
  buildWinCelebration, 
  buildAffiliateReminder 
} = require('./whatsapp-concierge');
const { Pool } = require('pg');

// Configuração do Banco
const DB_CONFIG = {
  host: 'localhost',
  port: 5432,
  database: 'leveclaw',
  user: 'leveclaw_user',
  password: 'leveclaw_password',
};

/**
 * Buscar usuários com WhatsApp do banco de dados
 */
async function getUsersWithPhone() {
  const pool = new Pool(DB_CONFIG);
  
  try {
    const query = `
      SELECT id, name, email, phone, wallet_address
      FROM "User"
      WHERE phone IS NOT NULL
      ORDER BY name
    `;
    
    const result = await pool.query(query);
    
    console.log(`📊 Usuários encontrados no banco: ${result.rows.length}`);
    result.rows.forEach(row => {
      console.log(`   - ${row.name}: phone=${row.phone}, wallet=${row.wallet_address || 'null'}`);
    });
    
    return result.rows.map(row => ({
      id: row.id,
      nome: row.name,
      email: row.email,
      whatsapp: row.phone,
      wallet: row.wallet_address || null, // Garantir que null seja explícito
    }));
  } catch (error) {
    console.error('Erro ao buscar usuários:', error);
    return [];
  } finally {
    await pool.end();
  }
}

/**
 * Verificar sinais que estão na zona de entrada
 */
async function checkEntryZoneSignals() {
  console.log('🔍 Verificando sinais na zona de entrada...');
  
  const pool = new Pool(DB_CONFIG);
  
  try {
    // Buscar sinais ativos com preço atual
    const query = `
      SELECT 
        s.id, s.symbol, s.direction, s.entry_min, s.entry_max, 
        s.stop_loss, s.targets,
        (s.targets->0->>'tp')::numeric as tp1
      FROM alpha_signals s
      WHERE s.status = 'active'
      AND s.direction = 'LONG'
    `;
    
    const result = await pool.query(query);
    
    for (const signal of result.rows) {
      // Simular preço atual (na produção, viria da Binance API)
      const currentPrice = parseFloat(signal.entry_min) * 1.01; // Simulando dentro da zona
      
      // Verificar se está na zona
      if (currentPrice >= parseFloat(signal.entry_min) && 
          currentPrice <= parseFloat(signal.entry_max)) {
        
        console.log(`🚨 SINAL NA ZONA: ${signal.symbol}`);
        
        // Enviar alerta para todos os usuários
        for (const user of USERS) {
          const message = buildSignalAlert(
            user.nome,
            signal.symbol,
            signal.direction,
            currentPrice,
            parseFloat(signal.entry_min),
            parseFloat(signal.entry_max),
            parseFloat(signal.tp1),
            parseFloat(signal.stop_loss)
          );
          
          await sendWhatsApp(user.whatsapp, message);
          console.log(`✅ Alerta enviado para ${user.nome}`);
        }
      }
    }
    
  } catch (error) {
    console.error('❌ Erro ao verificar zona de entrada:', error);
  } finally {
    await pool.end();
  }
}

/**
 * Verificar sinais que bateram TP1
 */
async function checkTP1Hits() {
  console.log('🎯 Verificando TP1 batidos...');
  
  const pool = new Pool(DB_CONFIG);
  
  try {
    // Buscar sinais WIN (na produção, Result Tracker atualiza isso)
    const query = `
      SELECT 
        s.id, s.symbol, s.direction, 
        ((s.entry_min::numeric + s.entry_max::numeric) / 2) as entry_price,
        (s.targets->0->>'tp')::numeric as tp1,
        s.pnl
      FROM alpha_signals s
      WHERE s.status = 'WIN'
      AND s.pnl > 0
    `;
    
    const result = await pool.query(query);
    
    for (const signal of result.rows) {
      console.log(`🎉 TP1 BATIDO: ${signal.symbol} (+${signal.pnl}%)`);
      
      // Enviar comemoração para todos os usuários
      for (const user of USERS) {
        const message = buildWinCelebration(
          user.nome,
          signal.symbol,
          signal.direction,
          parseFloat(signal.entry_price),
          parseFloat(signal.tp1),
          parseFloat(signal.tp1) * 1.02, // Simulando preço atual
          parseFloat(signal.pnl)
        );
        
        await sendWhatsApp(user.whatsapp, message);
        console.log(`✅ Comemoração enviada para ${user.nome}`);
      }
    }
    
  } catch (error) {
    console.error('❌ Erro ao verificar TP1:', error);
  } finally {
    await pool.end();
  }
}

/**
 * Buscar comissões reais do usuário no banco
 * (Na produção, isso viria do PaymentSplitter via eventos on-chain)
 */
async function getUserCommissions(userId) {
  const pool = new Pool(DB_CONFIG);
  
  try {
    // Tabela de comissões (será populada pelo PaymentSplitter quando eventos on-chain forem processados)
    // Por enquanto, retorna 0 se não existir registro
    const query = `
      SELECT 
        COALESCE(SUM(commission_usd), 0) as commissions_earned,
        COALESCE(SUM(volume_usd), 0) as total_volume
      FROM affiliate_commissions
      WHERE user_id = $1
    `;
    
    const result = await pool.query(query, [userId]);
    
    return {
      commissionsEarned: parseFloat(result.rows[0].commissions_earned) || 0,
      totalVolume: parseFloat(result.rows[0].total_volume) || 0,
    };
  } catch (error) {
    // Tabela não existe ainda - retorna 0
    console.log(`⚠️  Tabela affiliate_commissions não existe - usando $0.00 para ${userId}`);
    return { commissionsEarned: 0, totalVolume: 0 };
  } finally {
    await pool.end();
  }
}

/**
 * Enviar lembrete de afiliados semanal
 */
async function sendAffiliateReminder() {
  console.log('💎 Enviando lembretes de afiliados...');
  
  for (const user of USERS) {
    // Buscar dados REAIS do banco
    const { commissionsEarned, totalVolume } = await getUserCommissions(user.id);
    
    const message = buildAffiliateReminder(
      user.nome,
      user.wallet, // Wallet address REAL do banco
      commissionsEarned, // Valor REAL (ou $0 se não tiver comissões)
      totalVolume // Valor REAL (ou $0 se não tiver volume)
    );
    
    await sendWhatsApp(user.whatsapp, message);
    console.log(`✅ Lembrete enviado para ${user.nome} (Wallet: ${user.wallet || 'não vinculada'}, Comissões: $${commissionsEarned.toFixed(2)})`);
  }
}

/**
 * Main - Executar verificações
 */
async function main() {
  console.log('🤖 WhatsApp Concierge Automation');
  console.log('================================\n');
  
  const mode = process.argv[2] || 'all';
  
  // Carregar usuários do banco
  global.USERS = await getUsersWithPhone();
  console.log(`👥 ${global.USERS.length} usuários com WhatsApp encontrados\n`);
  
  if (global.USERS.length === 0) {
    console.log('⚠️  Nenhum usuário com WhatsApp encontrado no banco!');
    console.log('💡 Dica: Usuários podem vincular WhatsApp em /dashboard/settings');
    return;
  }
  
  switch (mode) {
    case 'entry':
      await checkEntryZoneSignals();
      break;
    case 'tp1':
      await checkTP1Hits();
      break;
    case 'affiliate':
      await sendAffiliateReminder();
      break;
    case 'all':
    default:
      await checkEntryZoneSignals();
      await checkTP1Hits();
      break;
  }
  
  console.log('\n✅ Automação concluída!');
}

// Executar
main().catch(console.error);
