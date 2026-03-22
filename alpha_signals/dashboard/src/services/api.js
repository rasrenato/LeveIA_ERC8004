/**
 * API Service - Alpha Signals Dashboard
 * Conecta com EconomicTracker e WorkEvaluator
 */

const API_BASE = '/api/alpha-signals'

/**
 * Busca dados econômicos do agente
 */
export async function getEconomicData(agentId = 'default') {
  try {
    const res = await fetch(`${API_BASE}/status?agent=${agentId}`)
    if (!res.ok) throw new Error('Falha ao buscar dados')
    return await res.json()
  } catch (error) {
    console.error('API error:', error)
    // Mock data para desenvolvimento
    return {
      agent_id: agentId,
      balance: 98.75,
      initial_balance: 100,
      total_revenue: 12.50,
      total_costs: 13.75,
      profit_loss: -1.25,
      survival_days: 5,
      status: 'thriving', // thriving, struggling, critical, dead
      signals_generated: 125,
      avg_score: 0.783,
      win_rate: 67.5,
      last_updated: new Date().toISOString()
    }
  }
}

/**
 * Busca leaderboard de agentes
 */
export async function getLeaderboard(limit = 10) {
  try {
    const res = await fetch(`${API_BASE}/leaderboard?limit=${limit}`)
    if (!res.ok) throw new Error('Falha ao buscar leaderboard')
    return await res.json()
  } catch (error) {
    console.error('Leaderboard error:', error)
    // Mock data
    return [
      { agent_id: 'alpha-001', agent_name: 'Alpha Wolf', balance: 145.30, revenue: 45.30, win_rate: 78.5, avg_score: 0.856, status: 'thriving', survival_days: 12 },
      { agent_id: 'alpha-002', agent_name: 'Crypto King', balance: 132.80, revenue: 32.80, win_rate: 72.3, avg_score: 0.798, status: 'thriving', survival_days: 10 },
      { agent_id: 'alpha-003', agent_name: 'Signal Master', balance: 98.75, revenue: 12.50, win_rate: 67.5, avg_score: 0.783, status: 'thriving', survival_days: 5 },
      { agent_id: 'alpha-004', agent_name: 'BTC Hunter', balance: 45.20, revenue: 5.20, win_rate: 45.2, avg_score: 0.512, status: 'struggling', survival_days: 3 },
      { agent_id: 'alpha-005', agent_name: 'ETH Trader', balance: 18.50, revenue: 2.50, win_rate: 38.7, avg_score: 0.423, status: 'critical', survival_days: 2 },
    ]
  }
}

/**
 * Busca sinais recentes
 */
export async function getRecentSignals(limit = 20) {
  try {
    const res = await fetch(`${API_BASE}/signals?limit=${limit}`)
    if (!res.ok) throw new Error('Falha ao buscar sinais')
    return await res.json()
  } catch (error) {
    console.error('Signals error:', error)
    // Mock data
    return [
      { id: 'sig-001', agent_id: 'alpha-003', asset: 'BTC/USD', direction: 'UP', confidence: 0.85, score: 0.92, payment: 0.092, status: 'evaluated', timestamp: new Date(Date.now() - 1000 * 60 * 15).toISOString() },
      { id: 'sig-002', agent_id: 'alpha-001', asset: 'ETH/USD', direction: 'DOWN', confidence: 0.72, score: 0.78, payment: 0.078, status: 'evaluated', timestamp: new Date(Date.now() - 1000 * 60 * 45).toISOString() },
      { id: 'sig-003', agent_id: 'alpha-002', asset: 'BTC/USD', direction: 'UP', confidence: 0.68, score: 0.00, payment: 0.00, status: 'pending', timestamp: new Date(Date.now() - 1000 * 60 * 120).toISOString() },
      { id: 'sig-004', agent_id: 'alpha-003', asset: 'SOL/USD', direction: 'UP', confidence: 0.91, score: 0.88, payment: 0.088, status: 'evaluated', timestamp: new Date(Date.now() - 1000 * 60 * 180).toISOString() },
      { id: 'sig-005', agent_id: 'alpha-004', asset: 'BTC/USD', direction: 'DOWN', confidence: 0.55, score: 0.45, payment: 0.045, status: 'evaluated', timestamp: new Date(Date.now() - 1000 * 60 * 300).toISOString() },
    ]
  }
}

/**
 * Decide atividade (work vs learn)
 */
export async function decideActivity(activity, reasoning) {
  try {
    const res = await fetch(`${API_BASE}/decide`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ activity, reasoning })
    })
    if (!res.ok) throw new Error('Falha ao decidir atividade')
    return await res.json()
  } catch (error) {
    console.error('Decide error:', error)
    return { success: false, error: error.message }
  }
}

/**
 * Submete sinal para avaliação
 */
export async function submitSignal(signalData) {
  try {
    const res = await fetch(`${API_BASE}/submit`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(signalData)
    })
    if (!res.ok) throw new Error('Falha ao submeter sinal')
    return await res.json()
  } catch (error) {
    console.error('Submit error:', error)
    return { success: false, error: error.message }
  }
}
