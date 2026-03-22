import { useState } from 'react'
import { Activity, TrendingUp, Users, Wallet, Shield, RefreshCw, AlertTriangle } from 'lucide-react'
import { useEconomicData, useSurvivalStatus } from './hooks/useEconomicData'
import StatusCard from './components/StatusCard'
import Leaderboard from './components/Leaderboard'
import SignalsTable from './components/SignalsTable'
import BalanceChart from './components/BalanceChart'

/**
 * Alpha Signals Dashboard - ClawWork Adaptation
 * Monitora agentes em tempo real com pressão econômica
 */
function App() {
  const [agentId, setAgentId] = useState('default')
  const { data, leaderboard, signals, loading, error, refresh } = useEconomicData(agentId)
  const survivalStatus = useSurvivalStatus(data?.balance || 0, data?.initial_balance || 100)

  if (loading && !data) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-cyan-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-cyan-400 text-lg font-semibold">Carregando Alpha Signals...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-900">
      {/* Header */}
      <header className="bg-gray-800 border-b border-gray-700 px-6 py-4 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-cyan-500 to-emerald-500 flex items-center justify-center">
              <Activity className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-white">Alpha Signals</h1>
              <p className="text-sm text-gray-400">ClawWork Economic Benchmark</p>
            </div>
          </div>

          <div className="flex items-center gap-4">
            {/* Survival Status */}
            {data && (
              <div className={`flex items-center gap-2 px-4 py-2 rounded-lg bg-${survivalStatus.color}-500/10 border border-${survivalStatus.color}-500/30`}>
                <span className="text-2xl">{survivalStatus.icon}</span>
                <div>
                  <p className={`text-sm font-semibold text-${survivalStatus.color}-400`}>
                    {survivalStatus.status.toUpperCase()}
                  </p>
                  <p className="text-xs text-gray-400">Balance: ${data.balance.toFixed(2)}</p>
                </div>
              </div>
            )}

            {/* Refresh Button */}
            <button
              onClick={refresh}
              disabled={loading}
              className="p-2 rounded-lg bg-gray-700 hover:bg-gray-600 transition-colors disabled:opacity-50"
            >
              <RefreshCw className={`w-5 h-5 text-gray-300 ${loading ? 'animate-spin' : ''}`} />
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-6 py-8 space-y-6">
        {/* Error Banner */}
        {error && (
          <div className="bg-red-500/10 border border-red-500/30 rounded-lg p-4 flex items-center gap-3">
            <AlertTriangle className="w-5 h-5 text-red-500" />
            <div>
              <p className="text-red-400 font-semibold">Erro ao carregar dados</p>
              <p className="text-sm text-gray-400">{error}</p>
            </div>
          </div>
        )}

        {/* Stats Grid */}
        {data && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <StatusCard
              title="Balance"
              value={`$${data.balance.toFixed(2)}`}
              change={data.profit_loss}
              icon={Wallet}
              color="cyan"
            />
            <StatusCard
              title="Revenue"
              value={`$${data.total_revenue.toFixed(2)}`}
              change={data.total_revenue - data.total_costs}
              icon={TrendingUp}
              color="emerald"
            />
            <StatusCard
              title="Costs"
              value={`$${data.total_costs.toFixed(2)}`}
              change={-data.total_costs}
              icon={Shield}
              color="red"
            />
            <StatusCard
              title="Signals"
              value={data.signals_generated}
              change={data.win_rate}
              icon={Activity}
              color="amber"
              changeLabel="Win Rate"
            />
          </div>
        )}

        {/* Balance Chart + Survival Info */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2">
            <BalanceChart agentId={agentId} />
          </div>
          <div className="space-y-4">
            {data && (
              <>
                <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
                  <h3 className="text-lg font-semibold text-white mb-4">Survival Info</h3>
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span className="text-gray-400">Initial Balance</span>
                      <span className="text-white font-medium">${data.initial_balance}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-400">Current Balance</span>
                      <span className={`font-medium text-${survivalStatus.color}-400`}>${data.balance.toFixed(2)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-400">Profit/Loss</span>
                      <span className={`font-medium ${data.profit_loss >= 0 ? 'text-emerald-400' : 'text-red-400'}`}>
                        ${data.profit_loss.toFixed(2)}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-400">Survival Days</span>
                      <span className="text-white font-medium">{data.survival_days}</span>
                    </div>
                    <div className="pt-3 border-t border-gray-700">
                      <div className="flex justify-between">
                        <span className="text-gray-400">Avg Score</span>
                        <span className="text-cyan-400 font-medium">{data.avg_score.toFixed(3)}</span>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
                  <h3 className="text-lg font-semibold text-white mb-4">Agent Selection</h3>
                  <select
                    value={agentId}
                    onChange={(e) => setAgentId(e.target.value)}
                    className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-2 text-white focus:outline-none focus:ring-2 focus:ring-cyan-500"
                  >
                    <option value="default">Default Agent</option>
                    <option value="alpha-001">Alpha Wolf</option>
                    <option value="alpha-002">Crypto King</option>
                    <option value="alpha-003">Signal Master</option>
                  </select>
                </div>
              </>
            )}
          </div>
        </div>

        {/* Leaderboard + Signals */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <Leaderboard agents={leaderboard} />
          <SignalsTable signals={signals} />
        </div>

        {/* Cost Footer */}
        <footer className="bg-gray-800 border-t border-gray-700 px-6 py-4">
          <div className="max-w-7xl mx-auto flex items-center justify-between text-sm">
            <div className="flex items-center gap-4">
              <span className="text-gray-400">Last update:</span>
              <span className="text-white">
                {data?.last_updated ? new Date(data.last_updated).toLocaleTimeString('pt-BR') : 'Now'}
              </span>
            </div>
            <div className="flex items-center gap-4">
              <span className="text-gray-400">Cost per signal:</span>
              <span className="text-cyan-400 font-medium">$0.10 USDC</span>
            </div>
            <div className="flex items-center gap-2">
              <div className={`w-2 h-2 rounded-full ${survivalStatus.color === 'emerald' ? 'bg-emerald-500 animate-pulse' : survivalStatus.color === 'amber' ? 'bg-amber-500' : survivalStatus.color === 'red' ? 'bg-red-500' : 'bg-gray-500'}`}></div>
              <span className="text-gray-400">Status: <span className={`text-${survivalStatus.color}-400`}>{survivalStatus.status}</span></span>
            </div>
          </div>
        </footer>
      </main>
    </div>
  )
}

export default App
