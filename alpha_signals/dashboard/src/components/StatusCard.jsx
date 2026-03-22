import { TrendingUp, TrendingDown } from 'lucide-react'

/**
 * Status Card Component
 * Exibe métricas com indicador de mudança
 */
export default function StatusCard({ title, value, change, icon: Icon, color = 'cyan', changeLabel = 'Change' }) {
  const isPositive = change >= 0
  const colorClasses = {
    cyan: 'from-cyan-500 to-cyan-600',
    emerald: 'from-emerald-500 to-emerald-600',
    red: 'from-red-500 to-red-600',
    amber: 'from-amber-500 to-amber-600',
    violet: 'from-violet-500 to-violet-600'
  }

  return (
    <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className={`w-10 h-10 rounded-lg bg-gradient-to-br ${colorClasses[color]} flex items-center justify-center`}>
            <Icon className="w-5 h-5 text-white" />
          </div>
          <span className="text-gray-400 text-sm">{title}</span>
        </div>
      </div>

      <div className="flex items-end justify-between">
        <p className="text-3xl font-bold text-white">{value}</p>
        {change !== undefined && (
          <div className={`flex items-center gap-1 text-sm ${isPositive ? 'text-emerald-400' : 'text-red-400'}`}>
            {isPositive ? <TrendingUp className="w-4 h-4" /> : <TrendingDown className="w-4 h-4" />}
            <span className="font-medium">
              {isPositive ? '+' : ''}{typeof change === 'number' ? change.toFixed(2) : change}
            </span>
          </div>
        )}
      </div>

      {changeLabel && (
        <p className="text-xs text-gray-500 mt-2">{changeLabel}</p>
      )}
    </div>
  )
}
