import { CheckCircle, XCircle, Clock, TrendingUp, TrendingDown } from 'lucide-react'

/**
 * Signals Table Component
 * Tabela de sinais recentes com scores e payments
 */
export default function SignalsTable({ signals = [] }) {
  const getStatusIcon = (status) => {
    switch (status) {
      case 'evaluated':
        return <CheckCircle className="w-4 h-4 text-emerald-500" />
      case 'pending':
        return <Clock className="w-4 h-4 text-amber-500" />
      case 'rejected':
        return <XCircle className="w-4 h-4 text-red-500" />
      default:
        return <Clock className="w-4 h-4 text-gray-500" />
    }
  }

  const getDirectionIcon = (direction) => {
    if (direction === 'UP') {
      return <TrendingUp className="w-4 h-4 text-emerald-500" />
    } else if (direction === 'DOWN') {
      return <TrendingDown className="w-4 h-4 text-red-500" />
    }
    return null
  }

  const formatTimeAgo = (timestamp) => {
    const seconds = Math.floor((new Date() - new Date(timestamp)) / 1000)
    if (seconds < 60) return 'Now'
    if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`
    if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`
    return `${Math.floor(seconds / 86400)}d ago`
  }

  return (
    <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-lg font-semibold text-white">Recent Signals</h3>
          <p className="text-sm text-gray-400">Latest submissions</p>
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="text-left border-b border-gray-700">
              <th className="pb-3 text-gray-400 text-xs font-medium">Asset</th>
              <th className="pb-3 text-gray-400 text-xs font-medium">Direction</th>
              <th className="pb-3 text-gray-400 text-xs font-medium">Confidence</th>
              <th className="pb-3 text-gray-400 text-xs font-medium">Score</th>
              <th className="pb-3 text-gray-400 text-xs font-medium">Payment</th>
              <th className="pb-3 text-gray-400 text-xs font-medium">Status</th>
              <th className="pb-3 text-gray-400 text-xs font-medium text-right">Time</th>
            </tr>
          </thead>
          <tbody>
            {signals.map((signal) => (
              <tr key={signal.id} className="border-b border-gray-700/50 hover:bg-gray-700/30 transition-colors">
                <td className="py-4">
                  <span className="text-white font-medium">{signal.asset}</span>
                </td>
                <td className="py-4">
                  <div className="flex items-center gap-2">
                    {getDirectionIcon(signal.direction)}
                    <span className={`text-sm ${signal.direction === 'UP' ? 'text-emerald-400' : 'text-red-400'}`}>
                      {signal.direction}
                    </span>
                  </div>
                </td>
                <td className="py-4">
                  <div className="flex items-center gap-2">
                    <div className="w-16 h-2 bg-gray-700 rounded-full overflow-hidden">
                      <div
                        className="h-full bg-cyan-500"
                        style={{ width: `${signal.confidence * 100}%` }}
                      ></div>
                    </div>
                    <span className="text-sm text-gray-400">{(signal.confidence * 100).toFixed(0)}%</span>
                  </div>
                </td>
                <td className="py-4">
                  <span className={`text-sm font-medium ${signal.score > 0.7 ? 'text-emerald-400' : signal.score > 0.4 ? 'text-amber-400' : 'text-red-400'}`}>
                    {signal.score.toFixed(2)}
                  </span>
                </td>
                <td className="py-4">
                  <span className="text-emerald-400 font-medium">${signal.payment.toFixed(3)}</span>
                </td>
                <td className="py-4">
                  <div className="flex items-center gap-2">
                    {getStatusIcon(signal.status)}
                    <span className="text-sm text-gray-400 capitalize">{signal.status}</span>
                  </div>
                </td>
                <td className="py-4 text-right">
                  <span className="text-gray-400 text-sm">{formatTimeAgo(signal.timestamp)}</span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {signals.length === 0 && (
        <div className="text-center py-8 text-gray-400">
          <Clock className="w-12 h-12 mx-auto mb-3 opacity-50" />
          <p>No signals yet</p>
        </div>
      )}
    </div>
  )
}
