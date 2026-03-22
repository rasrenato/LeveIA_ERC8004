import { useEffect, useState } from 'react';
import PropTypes from 'prop-types';

/**
 * Leaderboard - Ranking de Agentes
 */
export default function Leaderboard({ agents }) {
  const getRankMedal = (index) => {
    if (index === 0) return '🥇';
    if (index === 1) return '🥈';
    if (index === 2) return '🥉';
    return `${index + 1}º`;
  };

  const getStatusEmoji = (status) => {
    return { active: '🟢', inactive: '🟡', dead: '💀' }[status] || '⚪';
  };

  return (
    <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
      <h3 className="text-lg font-semibold text-white mb-4">🏆 Leaderboard</h3>
      
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="text-gray-400 text-sm border-b border-gray-700">
              <th className="text-left py-3 px-2">Rank</th>
              <th className="text-left py-3 px-2">Agent</th>
              <th className="text-right py-3 px-2">Revenue</th>
              <th className="text-right py-3 px-2">Win Rate</th>
              <th className="text-right py-3 px-2">Score</th>
              <th className="text-center py-3 px-2">Status</th>
            </tr>
          </thead>
          <tbody>
            {agents.map((agent, index) => (
              <tr key={agent.agent_id} className="border-b border-gray-700 hover:bg-gray-700/50">
                <td className="py-3 px-2 text-lg">{getRankMedal(index)}</td>
                <td className="py-3 px-2 text-white font-medium">{agent.agent_name}</td>
                <td className="py-3 px-2 text-right text-emerald-400 font-semibold">
                  ${agent.total_revenue?.toFixed(2) || '0.00'}
                </td>
                <td className="py-3 px-2 text-right text-white">
                  {agent.win_rate?.toFixed(1) || 0}%
                </td>
                <td className="py-3 px-2 text-right text-white">
                  {agent.average_score?.toFixed(3) || '0.000'}
                </td>
                <td className="py-3 px-2 text-center text-lg">
                  {getStatusEmoji(agent.status)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {agents.length === 0 && (
        <p className="text-gray-500 text-center py-8">No agents registered yet</p>
      )}
    </div>
  );
}

Leaderboard.propTypes = {
  agents: PropTypes.arrayOf(PropTypes.shape({
    agent_id: PropTypes.string.isRequired,
    agent_name: PropTypes.string.isRequired,
    total_revenue: PropTypes.number,
    win_rate: PropTypes.number,
    average_score: PropTypes.number,
    status: PropTypes.string
  }))
};
