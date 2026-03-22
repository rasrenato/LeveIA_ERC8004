"""
Leaderboard - Ranking de Agentes Alpha Signals

Inspirado no ClawWork leaderboard
Adaptado para LeveCoin Alpha Signals

Ranking por:
1. Total Revenue (USDC)
2. Win Rate (% acertos)
3. Average Score (qualidade dos sinais)
4. Survival Days (dias ativo)
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path


class Leaderboard:
    """
    Ranking de agentes Alpha Signals
    
    Métricas:
    - Total Revenue (USDC)
    - Win Rate (%)
    - Average Score (0.0-1.0)
    - Survival Days
    - Total Signals
    """

    def __init__(self, data_path: Optional[str] = None):
        """
        Inicializa Leaderboard
        
        Args:
            data_path: Path para salvar rankings
        """
        self.data_path = data_path or "./data/leaderboard"
        Path(self.data_path).mkdir(parents=True, exist_ok=True)
        
        # Agentes registrados
        self.agents: Dict[str, Dict] = {}
        
        # Carregar dados salvos
        self._load_data()

    def _load_data(self):
        """Carrega dados salvos"""
        data_path = os.path.join(self.data_path, "leaderboard.json")
        if os.path.exists(data_path):
            try:
                with open(data_path, 'r') as f:
                    self.agents = json.load(f)
            except:
                self.agents = {}

    def _save_data(self):
        """Salva dados"""
        data_path = os.path.join(self.data_path, "leaderboard.json")
        with open(data_path, 'w') as f:
            json.dump(self.agents, f, indent=2)

    def register_agent(
        self,
        agent_id: str,
        agent_name: str,
        initial_balance: float = 100.0
    ) -> Dict:
        """
        Registra novo agente no leaderboard
        
        Args:
            agent_id: ID único do agente
            agent_name: Nome exibido
            initial_balance: Saldo inicial
        
        Returns:
            Dict com dados do agente
        """
        if agent_id not in self.agents:
            self.agents[agent_id] = {
                'agent_id': agent_id,
                'agent_name': agent_name,
                'initial_balance': initial_balance,
                'current_balance': initial_balance,
                'total_revenue': 0.0,
                'total_costs': 0.0,
                'win_count': 0,
                'loss_count': 0,
                'total_signals': 0,
                'average_score': 0.0,
                'created_at': datetime.utcnow().isoformat(),
                'last_active': datetime.utcnow().isoformat(),
                'status': 'active'  # active, inactive, dead
            }
            self._save_data()
            print(f"✅ Agente registrado: {agent_name} ({agent_id})")
        
        return self.agents[agent_id]

    def update_agent_stats(
        self,
        agent_id: str,
        revenue: float = 0.0,
        costs: float = 0.0,
        signal_score: Optional[float] = None,
        is_win: Optional[bool] = None
    ):
        """
        Atualiza estatísticas do agente
        
        Args:
            agent_id: ID do agente
            revenue: Receita da operação
            costs: Custos da operação
            signal_score: Score do sinal (0.0-1.0)
            is_win: Se o sinal foi lucrativo
        """
        if agent_id not in self.agents:
            print(f"⚠️ Agente {agent_id} não registrado")
            return
        
        agent = self.agents[agent_id]
        
        # Atualizar financeiro
        agent['current_balance'] += revenue - costs
        agent['total_revenue'] += revenue
        agent['total_costs'] += costs
        
        # Atualizar sinais
        if signal_score is not None:
            agent['total_signals'] += 1
            # Média móvel do score
            n = agent['total_signals']
            old_avg = agent['average_score']
            agent['average_score'] = ((old_avg * (n-1)) + signal_score) / n
        
        # Atualizar win/loss
        if is_win is not None:
            if is_win:
                agent['win_count'] += 1
            else:
                agent['loss_count'] += 1
        
        # Atualizar last_active
        agent['last_active'] = datetime.utcnow().isoformat()
        
        # Verificar se "morreu"
        if agent['current_balance'] <= 0:
            agent['status'] = 'dead'
            print(f"💀 Agente {agent['agent_name']} faleceu! (saldo: ${agent['current_balance']:.2f})")
        
        self._save_data()

    def get_rankings(self, sort_by: str = 'total_revenue') -> List[Dict]:
        """
        Retorna ranking ordenado
        
        Args:
            sort_by: Critério de ordenação
                - 'total_revenue' (padrão)
                - 'win_rate'
                - 'average_score'
                - 'survival_days'
        
        Returns:
            Lista de agentes ordenada
        """
        agents_list = list(self.agents.values())
        
        # Calcular métricas derivadas
        for agent in agents_list:
            # Win rate
            total_trades = agent['win_count'] + agent['loss_count']
            agent['win_rate'] = (agent['win_count'] / total_trades * 100) if total_trades > 0 else 0.0
            
            # Survival days
            created = datetime.fromisoformat(agent['created_at'])
            agent['survival_days'] = (datetime.utcnow() - created).days
            
            # Profit margin
            if agent['total_costs'] > 0:
                agent['profit_margin'] = ((agent['total_revenue'] - agent['total_costs']) / agent['total_costs']) * 100
            else:
                agent['profit_margin'] = 0.0
        
        # Ordenar
        if sort_by == 'win_rate':
            agents_list.sort(key=lambda x: x['win_rate'], reverse=True)
        elif sort_by == 'average_score':
            agents_list.sort(key=lambda x: x['average_score'], reverse=True)
        elif sort_by == 'survival_days':
            agents_list.sort(key=lambda x: x['survival_days'], reverse=True)
        else:  # total_revenue
            agents_list.sort(key=lambda x: x['total_revenue'], reverse=True)
        
        return agents_list

    def get_top_agents(self, n: int = 10, sort_by: str = 'total_revenue') -> List[Dict]:
        """Retorna top N agentes"""
        return self.get_rankings(sort_by)[:n]

    def print_leaderboard(self, n: int = 10):
        """Imprime leaderboard formatado"""
        rankings = self.get_top_agents(n)
        
        print("\n" + "="*80)
        print("🏆 ALPHA SIGNALS LEADERBOARD")
        print("="*80)
        print(f"{'Rank':<5} {'Agent':<20} {'Revenue':<12} {'Win Rate':<10} {'Score':<8} {'Days':<6} {'Status':<8}")
        print("-"*80)
        
        for i, agent in enumerate(rankings, 1):
            medal = ['🥇', '🥈', '🥉'][i-1] if i <= 3 else f'{i}º'
            status_emoji = {'active': '🟢', 'inactive': '🟡', 'dead': '💀'}.get(agent['status'], '⚪')
            
            print(f"{medal:<5} {agent['agent_name']:<20} ${agent['total_revenue']:<11.2f} {agent['win_rate']:>5.1f}%    {agent['average_score']:.3f}    {agent['survival_days']:<6} {status_emoji} {agent['status']}")
        
        print("="*80 + "\n")

    def export_json(self, filename: Optional[str] = None) -> str:
        """Exporta leaderboard para JSON"""
        if filename is None:
            filename = f"leaderboard_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = os.path.join(self.data_path, filename)
        
        export_data = {
            'exported_at': datetime.utcnow().isoformat(),
            'total_agents': len(self.agents),
            'rankings': self.get_rankings()
        }
        
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        return filepath


# Exemplo de uso
if __name__ == "__main__":
    print("🧪 Testando Leaderboard\n")
    
    # Criar leaderboard
    leaderboard = Leaderboard()
    
    # Registrar agentes
    leaderboard.register_agent("agent_001", "Alpha Wolf", 100.0)
    leaderboard.register_agent("agent_002", "Crypto King", 100.0)
    leaderboard.register_agent("agent_003", "Signal Master", 100.0)
    leaderboard.register_agent("agent_004", "BTC Hunter", 100.0)
    
    # Simular operações
    print("="*60)
    print("SIMULANDO OPERAÇÕES...")
    print("="*60 + "\n")
    
    # Agent 1: Bom desempenho
    leaderboard.update_agent_stats("agent_001", revenue=0.50, costs=0.10, signal_score=0.85, is_win=True)
    leaderboard.update_agent_stats("agent_001", revenue=0.45, costs=0.10, signal_score=0.78, is_win=True)
    leaderboard.update_agent_stats("agent_001", revenue=0.40, costs=0.10, signal_score=0.72, is_win=True)
    
    # Agent 2: Desempenho médio
    leaderboard.update_agent_stats("agent_002", revenue=0.30, costs=0.10, signal_score=0.65, is_win=True)
    leaderboard.update_agent_stats("agent_002", revenue=0.00, costs=0.10, signal_score=0.45, is_win=False)
    leaderboard.update_agent_stats("agent_002", revenue=0.35, costs=0.10, signal_score=0.68, is_win=True)
    
    # Agent 3: Desempenho ruim
    leaderboard.update_agent_stats("agent_003", revenue=0.00, costs=0.10, signal_score=0.35, is_win=False)
    leaderboard.update_agent_stats("agent_003", revenue=0.00, costs=0.10, signal_score=0.28, is_win=False)
    leaderboard.update_agent_stats("agent_003", revenue=0.20, costs=0.10, signal_score=0.50, is_win=True)
    
    # Agent 4: Faliu
    leaderboard.update_agent_stats("agent_004", revenue=0.00, costs=0.10, signal_score=0.30, is_win=False)
    leaderboard.update_agent_stats("agent_004", revenue=0.00, costs=0.10, signal_score=0.25, is_win=False)
    leaderboard.update_agent_stats("agent_004", revenue=0.00, costs=90.00, signal_score=0.10, is_win=False)
    
    # Imprimir leaderboard
    print("="*60)
    print("LEADERBOARD FINAL (por Revenue)")
    print("="*60)
    leaderboard.print_leaderboard()
    
    # Exportar JSON
    filepath = leaderboard.export_json()
    print(f"📊 Leaderboard exportado: {filepath}\n")
