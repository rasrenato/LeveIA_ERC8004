"""
EconomicTracker - Rastreamento econômico para Alpha Signals x402

Inspirado no ClawWork LiveAgent EconomicTracker
Adaptado para LeveCoin - Alpha Signals

Funcionalidades:
- Rastrear saldo (USDC)
- Custos por API call / token
- Income por sinal vendido
- Survival status (thriving, struggling, critical, dead)
- Notificações de saldo crítico
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path


class EconomicTracker:
    """
    EconomicTracker para Alpha Signals
    
    Monitora saúde econômica do agente:
    - Saldo atual (USDC)
    - Custos acumulados (API + tokens)
    - Revenue (sinais vendidos)
    - Survival status
    """

    def __init__(
        self,
        agent_id: str = "alpha_signals_001",
        initial_balance: float = 100.0,  # USDC
        api_call_cost: float = 0.10,     # $0.10 por sinal (fixo)
        token_cost_per_1k: float = 0.001,  # $0.001 por 1K tokens
        critical_threshold: float = 20.0,   # Alerta quando saldo < $20
        data_path: Optional[str] = None
    ):
        """
        Inicializa EconomicTracker
        
        Args:
            agent_id: ID único do agente
            initial_balance: Saldo inicial em USDC
            api_call_cost: Custo fixo por chamada de API (gerar sinal)
            token_cost_per_1k: Custo variável por 1K tokens
            critical_threshold: Saldo crítico para alerta
            data_path: Path para salvar dados econômicos
        """
        self.agent_id = agent_id
        self.initial_balance = initial_balance
        self.api_call_cost = api_call_cost
        self.token_cost_per_1k = token_cost_per_1k
        self.critical_threshold = critical_threshold
        
        # Data path
        self.data_path = data_path or f"./data/economic/{agent_id}"
        Path(self.data_path).mkdir(parents=True, exist_ok=True)
        
        # Estado econômico
        self.balance = initial_balance
        self.total_costs = 0.0
        self.total_revenue = 0.0
        self.total_api_calls = 0
        self.total_tokens_used = 0
        
        # Histórico de transações
        self.transactions: List[Dict] = []
        
        # Status de sobrevivência
        self.survival_status = "thriving"  # thriving, struggling, critical, dead
        self.created_at = datetime.utcnow().isoformat()
        self.last_updated = self.created_at
        
        # Carregar estado salvo (se existir)
        self._load_state()

    def _get_state_path(self) -> str:
        """Retorna path do arquivo de estado"""
        return os.path.join(self.data_path, "economic_state.json")

    def _load_state(self):
        """Carrega estado salvo do disco"""
        state_path = self._get_state_path()
        if os.path.exists(state_path):
            try:
                with open(state_path, 'r') as f:
                    state = json.load(f)
                
                self.balance = state.get('balance', self.initial_balance)
                self.total_costs = state.get('total_costs', 0.0)
                self.total_revenue = state.get('total_revenue', 0.0)
                self.total_api_calls = state.get('total_api_calls', 0)
                self.total_tokens_used = state.get('total_tokens_used', 0)
                self.transactions = state.get('transactions', [])
                self.survival_status = state.get('survival_status', 'thriving')
                self.created_at = state.get('created_at', self.created_at)
                
                print(f"📊 EconomicTracker carregado: Saldo ${self.balance:.2f}")
            except Exception as e:
                print(f"⚠️ Erro ao carregar estado: {e}")
                self._save_state()  # Salva estado inicial

    def _save_state(self):
        """Salva estado no disco"""
        state = {
            'agent_id': self.agent_id,
            'balance': self.balance,
            'total_costs': self.total_costs,
            'total_revenue': self.total_revenue,
            'total_api_calls': self.total_api_calls,
            'total_tokens_used': self.total_tokens_used,
            'transactions': self.transactions[-100:],  # Últimas 100 transações
            'survival_status': self.survival_status,
            'created_at': self.created_at,
            'last_updated': datetime.utcnow().isoformat()
        }
        
        with open(self._get_state_path(), 'w') as f:
            json.dump(state, f, indent=2, ensure_ascii=False)

    def _update_survival_status(self):
        """Atualiza status de sobrevivência baseado no saldo"""
        if self.balance <= 0:
            self.survival_status = "dead"
        elif self.balance < self.critical_threshold * 0.5:
            self.survival_status = "critical"
        elif self.balance < self.critical_threshold:
            self.survival_status = "struggling"
        else:
            self.survival_status = "thriving"
        
        self._save_state()

    def record_api_call(
        self,
        tokens_used: int = 0,
        description: str = "API call",
        metadata: Optional[Dict] = None
    ) -> Dict:
        """
        Registra chamada de API (custo fixo + variável)
        
        Args:
            tokens_used: Quantidade de tokens usados
            description: Descrição da chamada
            metadata: Metadados adicionais
            
        Returns:
            Dict com detalhes da transação
        """
        # Calcular custos
        fixed_cost = self.api_call_cost
        variable_cost = (tokens_used / 1000) * self.token_cost_per_1k
        total_cost = fixed_cost + variable_cost
        
        # Atualizar estado
        self.balance -= total_cost
        self.total_costs += total_cost
        self.total_api_calls += 1
        self.total_tokens_used += tokens_used
        self.last_updated = datetime.utcnow().isoformat()
        
        # Registrar transação
        transaction = {
            'timestamp': self.last_updated,
            'type': 'api_call',
            'amount': -total_cost,
            'balance_after': self.balance,
            'tokens_used': tokens_used,
            'fixed_cost': fixed_cost,
            'variable_cost': variable_cost,
            'description': description,
            'metadata': metadata or {}
        }
        self.transactions.append(transaction)
        
        # Atualizar survival status
        self._update_survival_status()
        
        # Alerta se crítico
        if self.survival_status in ["critical", "dead"]:
            print(f"⚠️ ALERTA: {self.survival_status.upper()} - Saldo: ${self.balance:.2f}")
        
        return transaction

    def record_revenue(
        self,
        amount: float,
        signal_id: str = "",
        description: str = "Signal sold",
        metadata: Optional[Dict] = None
    ) -> Dict:
        """
        Registra receita (sinal vendido)
        
        Args:
            amount: Valor recebido em USDC
            signal_id: ID do sinal vendido
            description: Descrição
            metadata: Metadados adicionais
            
        Returns:
            Dict com detalhes da transação
        """
        # Atualizar estado
        self.balance += amount
        self.total_revenue += amount
        self.last_updated = datetime.utcnow().isoformat()
        
        # Registrar transação
        transaction = {
            'timestamp': self.last_updated,
            'type': 'revenue',
            'amount': amount,
            'balance_after': self.balance,
            'signal_id': signal_id,
            'description': description,
            'metadata': metadata or {}
        }
        self.transactions.append(transaction)
        
        # Atualizar survival status
        self._update_survival_status()
        
        return transaction

    def get_status(self) -> Dict:
        """
        Retorna status econômico atual
        
        Returns:
            Dict com status completo
        """
        profit_margin = 0.0
        if self.total_costs > 0:
            profit_margin = ((self.total_revenue - self.total_costs) / self.total_costs) * 100
        
        return {
            'agent_id': self.agent_id,
            'balance': self.balance,
            'initial_balance': self.initial_balance,
            'total_costs': self.total_costs,
            'total_revenue': self.total_revenue,
            'profit': self.total_revenue - self.total_costs,
            'profit_margin_percent': profit_margin,
            'total_api_calls': self.total_api_calls,
            'total_tokens_used': self.total_tokens_used,
            'survival_status': self.survival_status,
            'survival_emoji': self._get_status_emoji(),
            'created_at': self.created_at,
            'last_updated': self.last_updated
        }

    def _get_status_emoji(self) -> str:
        """Retorna emoji baseado no status"""
        emojis = {
            'thriving': '🟢',
            'struggling': '🟡',
            'critical': '🔴',
            'dead': '💀'
        }
        return emojis.get(self.survival_status, '⚪')

    def get_cost_footer(self) -> str:
        """
        Retorna footer de custo para incluir em respostas
        
        Returns:
            String formatada com custos e status
        """
        status = self.get_status()
        return (
            f"Cost: ${status['total_costs']:.4f} | "
            f"Balance: ${status['balance']:.2f} | "
            f"Status: {status['survival_emoji']} {status['survival_status']}"
        )

    def print_status(self):
        """Imprime status formatado no console"""
        status = self.get_status()
        print("\n" + "="*60)
        print(f"📊 ECONOMIC STATUS - {self.agent_id}")
        print("="*60)
        print(f"💰 Balance:        ${status['balance']:.2f} {status['survival_emoji']}")
        print(f"📈 Total Revenue:  ${status['total_revenue']:.2f}")
        print(f"📉 Total Costs:    ${status['total_costs']:.2f}")
        print(f"💵 Profit:         ${status['profit']:.2f} ({status['profit_margin_percent']:.1f}%)")
        print(f"📞 API Calls:      {status['total_api_calls']}")
        print(f"🔢 Tokens Used:    {status['total_tokens_used']:,}")
        print(f"⏰ Last Updated:   {status['last_updated']}")
        print("="*60 + "\n")


# Exemplo de uso
if __name__ == "__main__":
    # Criar tracker
    tracker = EconomicTracker(
        agent_id="alpha_signals_test",
        initial_balance=100.0,
        api_call_cost=0.10,
        token_cost_per_1k=0.001
    )
    
    # Simular algumas operações
    print("🚀 Simulando operações...\n")
    
    # Chamada de API (gerar sinal)
    tracker.record_api_call(
        tokens_used=500,
        description="Generate BTC signal",
        metadata={"asset": "BTC", "signal_type": "BUY"}
    )
    
    # Venda de sinal
    tracker.record_revenue(
        amount=0.10,
        signal_id="signal_001",
        description="Signal sold"
    )
    
    # Mais uma operação
    tracker.record_api_call(
        tokens_used=800,
        description="Generate ETH signal",
        metadata={"asset": "ETH", "signal_type": "SELL"}
    )
    
    # Imprimir status
    tracker.print_status()
    
    # Footer de custo
    print(f"\n{tracker.get_cost_footer()}\n")
