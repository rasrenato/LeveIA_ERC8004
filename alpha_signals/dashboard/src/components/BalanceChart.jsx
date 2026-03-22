import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

/**
 * Balance Chart Component
 * Gráfico de evolução do saldo ao longo do tempo
 */
export default function BalanceChart({ agentId }) {
  // Mock data - será substituído por API real
  const data = [
    { day: 'Day 1', balance: 100.00, revenue: 0, costs: 0 },
    { day: 'Day 2', balance: 98.50, revenue: 2.50, costs: 4.00 },
    { day: 'Day 3', balance: 97.20, revenue: 5.20, costs: 8.00 },
    { day: 'Day 4', balance: 99.80, revenue: 8.80, costs: 9.00 },
    { day: 'Day 5', balance: 98.75, revenue: 12.50, costs: 13.75 },
  ]

  return (
    <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-lg font-semibold text-white">Balance Over Time</h3>
          <p className="text-sm text-gray-400">Agent: {agentId}</p>
        </div>
      </div>

      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
            <XAxis
              dataKey="day"
              stroke="#9CA3AF"
              fontSize={12}
              tickLine={false}
              axisLine={false}
            />
            <YAxis
              stroke="#9CA3AF"
              fontSize={12}
              tickLine={false}
              axisLine={false}
              tickFormatter={(value) => `$${value}`}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: '#1F2937',
                border: '1px solid #374151',
                borderRadius: '8px'
              }}
              labelStyle={{ color: '#9CA3AF' }}
              formatter={(value) => [`$${value.toFixed(2)}`, 'Balance']}
            />
            <Line
              type="monotone"
              dataKey="balance"
              stroke="#06B6D4"
              strokeWidth={3}
              dot={{ fill: '#06B6D4', strokeWidth: 2, r: 4 }}
              activeDot={{ r: 6 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Legend */}
      <div className="flex items-center justify-center gap-6 mt-4 pt-4 border-t border-gray-700">
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-cyan-500"></div>
          <span className="text-sm text-gray-400">Balance</span>
        </div>
      </div>
    </div>
  )
}
