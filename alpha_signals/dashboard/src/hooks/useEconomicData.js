import { useState, useEffect, useCallback } from 'react'
import { getEconomicData, getLeaderboard, getRecentSignals } from '../services/api'

/**
 * Hook para dados econômicos em tempo real
 * Atualiza a cada 30 segundos
 */
export function useEconomicData(agentId = 'default', refreshInterval = 30000) {
  const [data, setData] = useState(null)
  const [leaderboard, setLeaderboard] = useState([])
  const [signals, setSignals] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const fetchData = useCallback(async () => {
    try {
      const [economicData, leaderboardData, signalsData] = await Promise.all([
        getEconomicData(agentId),
        getLeaderboard(10),
        getRecentSignals(20)
      ])

      setData(economicData)
      setLeaderboard(leaderboardData)
      setSignals(signalsData)
      setError(null)
    } catch (err) {
      console.error('Fetch error:', err)
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }, [agentId])

  useEffect(() => {
    fetchData()

    if (refreshInterval > 0) {
      const interval = setInterval(fetchData, refreshInterval)
      return () => clearInterval(interval)
    }
  }, [fetchData, refreshInterval])

  const refresh = useCallback(async () => {
    setLoading(true)
    await fetchData()
  }, [fetchData])

  return {
    data,
    leaderboard,
    signals,
    loading,
    error,
    refresh
  }
}

/**
 * Hook para status de sobrevivência
 */
export function useSurvivalStatus(balance, initialBalance = 100) {
  const [status, setStatus] = useState('unknown')
  const [color, setColor] = useState('gray')
  const [icon, setIcon] = useState('⚪')

  useEffect(() => {
    if (balance <= 0) {
      setStatus('dead')
      setColor('gray')
      setIcon('💀')
    } else if (balance < initialBalance * 0.2) {
      setStatus('critical')
      setColor('red')
      setIcon('🔴')
    } else if (balance < initialBalance * 0.5) {
      setStatus('struggling')
      setColor('amber')
      setIcon('🟡')
    } else {
      setStatus('thriving')
      setColor('emerald')
      setIcon('🟢')
    }
  }, [balance, initialBalance])

  return { status, color, icon }
}

/**
 * Hook para custo por operação
 */
export function useCostTracker() {
  const [totalCost, setTotalCost] = useState(0)
  const [operationCount, setOperationCount] = useState(0)

  const addCost = useCallback((cost) => {
    setTotalCost(prev => prev + cost)
    setOperationCount(prev => prev + 1)
  }, [])

  const reset = useCallback(() => {
    setTotalCost(0)
    setOperationCount(0)
  }, [])

  return {
    totalCost,
    operationCount,
    avgCost: operationCount > 0 ? totalCost / operationCount : 0,
    addCost,
    reset
  }
}
