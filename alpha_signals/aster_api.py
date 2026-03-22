"""
Aster API - NOSSA API de execução de ordens

API própria que simula/executa ordens de trading.
Padrão: MODO TESTE (simula execução, sem risco real)
Futuro: MODO PRODUÇÃO (integra com exchange real)
"""

import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List
from pathlib import Path
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)


@dataclass
class Order:
    """Ordem de trading"""
    id: str
    symbol: str
    side: str  # "BUY" ou "SELL"
    size: float
    price: Optional[float] = None
    type: str = "MARKET"  # "MARKET" ou "LIMIT"
    status: str = "PENDING"  # PENDING, FILLED, CANCELLED, REJECTED
    created_at: str = ""
    filled_at: Optional[str] = None
    filled_price: Optional[float] = None
    error: Optional[str] = None


@dataclass
class Position:
    """Posição aberta"""
    symbol: str
    side: str
    size: float
    entry_price: float
    unrealized_pnl: float = 0.0
    created_at: str = ""


@dataclass
class Account:
    """Conta do usuário"""
    balance: float = 1000.0  # Saldo inicial (USDC)
    equity: float = 1000.0
    unrealized_pnl: float = 0.0
    positions: List[Position] = None
    
    def __post_init__(self):
        if self.positions is None:
            self.positions = []


class AsterAPI:
    """
    NOSSA API Aster para execução de ordens
    
    Modo padrão: TESTE (simula execução)
    Futuro: PRODUÇÃO (integra com exchange real)
    """
    
    def __init__(self, mode: str = "TEST", log_path: Optional[str] = None):
        """
        Inicializa API Aster
        
        Args:
            mode: "TEST" (simula) ou "PRODUCTION" (executa real)
            log_path: Caminho para log de execuções
        """
        self.mode = mode
        self.log_path = Path(log_path) if log_path else Path("/root/openclaw/alpha_signals/logs/aster_executions.jsonl")
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Contas por usuário (em produção, viria do banco)
        self.accounts: Dict[str, Account] = {}
        
        # Preços mockados (em produção, viria da exchange)
        self.prices = {
            "BTCUSDT": 65000.0,
            "ETHUSDT": 3500.0,
            "BNBUSDT": 600.0
        }
        
        logger.info(f"Aster API inicializada (modo: {self.mode})")
    
    def _log_execution(self, order: Order, user_id: str):
        """Loga execução em arquivo (auditoria)"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + 'Z',
            "user_id": user_id,
            "mode": self.mode,
            "order": asdict(order)
        }
        
        with open(self.log_path, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
        
        logger.info(f"Ordem {order.id} logada em {self.log_path}")
    
    def _get_account(self, user_id: str) -> Account:
        """Obtém ou cria conta do usuário"""
        if user_id not in self.accounts:
            self.accounts[user_id] = Account()
        return self.accounts[user_id]
    
    def _get_price(self, symbol: str) -> float:
        """Obtém preço atual (mock em TEST, real em PRODUCTION)"""
        # Em TEST, usa preço mockado com pequena variação
        base_price = self.prices.get(symbol, 100.0)
        variation = (datetime.utcnow().timestamp() % 100) / 1000  # Variação 0-10%
        return base_price * (1 + variation)
    
    def execute_order(
        self,
        user_id: str,
        symbol: str,
        side: str,
        size: float,
        type: str = "MARKET",
        price: Optional[float] = None
    ) -> Order:
        """
        Executa ordem de trading
        
        Args:
            user_id: ID do usuário
            symbol: Par de trading (ex: BTCUSDT)
            side: "BUY" ou "SELL"
            size: Tamanho da ordem
            type: "MARKET" ou "LIMIT"
            price: Preço limite (para ordens LIMIT)
            
        Returns:
            Order com resultado da execução
        """
        # Criar ordem
        order = Order(
            id=f"order_{datetime.utcnow().timestamp()}",
            symbol=symbol,
            side=side,
            size=size,
            price=price,
            type=type,
            created_at=datetime.utcnow().isoformat() + 'Z'
        )
        
        logger.info(f"Executando ordem: {order.id} - {side} {size} {symbol}")
        
        try:
            # Obter conta
            account = self._get_account(user_id)
            
            # Obter preço de execução
            if type == "MARKET":
                execution_price = self._get_price(symbol)
            else:
                execution_price = price or self._get_price(symbol)
            
            # Calcular valor total
            total_value = size * execution_price
            
            # Verificar saldo (para BUY)
            if side == "BUY" and account.balance < total_value:
                order.status = "REJECTED"
                order.error = f"Saldo insuficiente. Necessário: ${total_value:.2f}, Disponível: ${account.balance:.2f}"
                logger.warning(f"Ordem rejeitada: {order.error}")
            else:
                # Executar ordem
                if side == "BUY":
                    account.balance -= total_value
                else:
                    account.balance += total_value
                
                # Atualizar ordem
                order.status = "FILLED"
                order.filled_at = datetime.utcnow().isoformat() + 'Z'
                order.filled_price = execution_price
                
                # Criar/atualizar posição
                self._update_position(account, symbol, side, size, execution_price)
                
                # Atualizar equity
                account.equity = account.balance + sum(
                    p.size * (self._get_price(p.symbol) - p.entry_price)
                    for p in account.positions if p.side == "BUY"
                )
                
                logger.info(f"Ordem executada: {order.id} @ ${execution_price:.2f}")
            
        except Exception as e:
            order.status = "REJECTED"
            order.error = str(e)
            logger.error(f"Erro na execução: {e}")
        
        # Logar execução (sempre, mesmo se rejeitada)
        self._log_execution(order, user_id)
        
        return order
    
    def _update_position(
        self,
        account: Account,
        symbol: str,
        side: str,
        size: float,
        price: float
    ):
        """Atualiza ou cria posição"""
        # Procurar posição existente
        for pos in account.positions:
            if pos.symbol == symbol and pos.side == side:
                # Atualizar posição existente (preço médio)
                total_size = pos.size + size
                pos.entry_price = ((pos.size * pos.entry_price) + (size * price)) / total_size
                pos.size = total_size
                return
        
        # Criar nova posição
        account.positions.append(Position(
            symbol=symbol,
            side=side,
            size=size,
            entry_price=price,
            created_at=datetime.utcnow().isoformat() + 'Z'
        ))
    
    def get_account_status(self, user_id: str) -> Dict[str, Any]:
        """
        Obtém status da conta
        
        Returns:
            Dicionário com saldo, equity, posições, etc.
        """
        account = self._get_account(user_id)
        
        # Atualizar PnL não realizado
        for pos in account.positions:
            current_price = self._get_price(pos.symbol)
            if pos.side == "BUY":
                pos.unrealized_pnl = (current_price - pos.entry_price) * pos.size
            else:
                pos.unrealized_pnl = (pos.entry_price - current_price) * pos.size
        
        account.unrealized_pnl = sum(p.unrealized_pnl for p in account.positions)
        account.equity = account.balance + account.unrealized_pnl
        
        return {
            "user_id": user_id,
            "balance": round(account.balance, 2),
            "equity": round(account.equity, 2),
            "unrealized_pnl": round(account.unrealized_pnl, 2),
            "positions": [asdict(p) for p in account.positions],
            "mode": self.mode
        }
    
    def cancel_order(self, order_id: str, user_id: str) -> bool:
        """
        Cancela ordem pendente
        
        Args:
            order_id: ID da ordem
            user_id: ID do usuário
            
        Returns:
            True se cancelado, False se não encontrado ou já executada
        """
        # Em modo TEST, ordens MARKET são executadas instantaneamente
        # Então só ordens LIMIT podem ser canceladas
        logger.info(f"Cancelando ordem {order_id} para usuário {user_id}")
        
        # Em produção, buscaria ordem no banco e cancelaria
        # Em TEST, só loga
        self._log_execution(
            Order(
                id=order_id,
                symbol="N/A",
                side="N/A",
                size=0,
                status="CANCELLED",
                created_at=datetime.utcnow().isoformat() + 'Z'
            ),
            user_id
        )
        
        return True
    
    def get_execution_history(self, user_id: str, limit: int = 100) -> List[Dict]:
        """
        Obtém histórico de execuções
        
        Args:
            user_id: ID do usuário
            limit: Máximo de ordens para retornar
            
        Returns:
            Lista de ordens executadas
        """
        if not self.log_path.exists():
            return []
        
        executions = []
        with open(self.log_path, 'r') as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    if entry.get("user_id") == user_id:
                        executions.append(entry)
                except:
                    continue
        
        return executions[-limit:]


# Singleton para uso global
_aster_api: Optional[AsterAPI] = None

def get_aster_api(mode: str = "TEST") -> AsterAPI:
    """Obtém instância singleton da Aster API"""
    global _aster_api
    if _aster_api is None or _aster_api.mode != mode:
        _aster_api = AsterAPI(mode=mode)
    return _aster_api


# Exemplo de uso
if __name__ == "__main__":
    # Testar API
    api = AsterAPI(mode="TEST")
    
    print("="*60)
    print("ASTER API - TESTE")
    print("="*60)
    
    # Executar ordem de compra
    print("\n📈 Executando BUY 0.01 BTCUSDT...")
    order = api.execute_order(
        user_id="test_user",
        symbol="BTCUSDT",
        side="BUY",
        size=0.01
    )
    
    print(f"Ordem: {order.id}")
    print(f"Status: {order.status}")
    print(f"Preço: ${order.filled_price:.2f}" if order.filled_price else f"Erro: {order.error}")
    
    # Status da conta
    print("\n📊 Status da Conta:")
    status = api.get_account_status("test_user")
    print(f"Saldo: ${status['balance']:.2f}")
    print(f"Equity: ${status['equity']:.2f}")
    print(f"Posições: {len(status['positions'])}")
    
    # Histórico
    print("\n📜 Histórico de Execuções:")
    history = api.get_execution_history("test_user")
    print(f"{len(history)} execuções encontradas")
    
    print("\n" + "="*60)
