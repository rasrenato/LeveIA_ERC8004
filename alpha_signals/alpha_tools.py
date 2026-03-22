"""
Alpha Signals Tools - Ferramentas inspiradas no ClawWork

Ferramentas principais:
1. decide_activity - Escolhe entre work (gerar sinais) ou learn (analisar dados)
2. get_status - Retorna status econômico atual
3. submit_signal - Envia sinal para avaliação e pagamento

Adaptado para integração com OpenClaw skills
"""

from typing import Dict, Any, Optional
import json
from datetime import datetime

# Import EconomicTracker
import sys
sys.path.insert(0, '/root/openclaw')
from alpha_signals.economic_tracker import EconomicTracker


# Global state (setado pelo agent loop)
_global_state = {
    'tracker': None,
    'agent_id': 'alpha_signals_001'
}


def set_global_state(tracker: EconomicTracker, agent_id: str = 'alpha_signals_001'):
    """Configura estado global para as tools"""
    global _global_state
    _global_state['tracker'] = tracker
    _global_state['agent_id'] = agent_id
    print(f"✅ Tools configuradas para agente: {agent_id}")


def decide_activity(activity: str, reasoning: str) -> Dict[str, Any]:
    """
    Decide atividade diária: work (gerar sinais) ou learn (analisar dados)
    
    Args:
        activity: "work" ou "learn"
        reasoning: Explicação da decisão (mínimo 50 caracteres)
    
    Returns:
        Dict com resultado da decisão
        
    Examples:
        decide_activity("work", "Preciso gerar revenue para manter o agente ativo...")
        decide_activity("learn", "Vou analisar dados históricos para melhorar acurácia...")
    """
    activity = activity.lower().strip()
    
    # Validar atividade
    if activity not in ["work", "learn"]:
        return {
            "error": "Invalid activity. Must be 'work' or 'learn'",
            "valid_options": ["work", "learn"],
            "received": activity
        }
    
    # Validar reasoning
    if len(reasoning) < 50:
        return {
            "error": "Reasoning must be at least 50 characters",
            "current_length": len(reasoning),
            "required": 50
        }
    
    # Registrar decisão
    tracker = _global_state.get('tracker')
    if tracker:
        print(f"🎯 Decisão registrada: {activity.upper()}")
        print(f"   Reasoning: {reasoning[:100]}...")
    
    # Retorno
    return {
        "success": True,
        "activity": activity,
        "reasoning": reasoning,
        "timestamp": datetime.utcnow().isoformat(),
        "message": f"✅ Decision made: {activity.upper()}",
        "next_step": "generate_signals()" if activity == "work" else "analyze_data()"
    }


def get_status() -> Dict[str, Any]:
    """
    Retorna status econômico atual do agente
    
    Returns:
        Dict com status completo (balance, costs, revenue, survival_status)
        
    Example:
        status = get_status()
        print(f"Saldo: ${status['balance']:.2f} - {status['survival_emoji']}")
    """
    tracker = _global_state.get('tracker')
    
    if not tracker:
        return {
            "error": "EconomicTracker not initialized",
            "status": "unknown"
        }
    
    status = tracker.get_status()
    
    # Adicionar footer formatado
    status['cost_footer'] = tracker.get_cost_footer()
    
    return status


def submit_signal(
    signal_json: str,
    asset: str = "BTC",
    signal_type: str = "BUY",
    confidence: float = 0.75,
    reasoning: str = ""
) -> Dict[str, Any]:
    """
    Envia sinal de trading para avaliação e pagamento
    
    Args:
        signal_json: JSON do sinal (direção, entry, stop, target)
        asset: Ativo (BTC, ETH, etc.)
        signal_type: BUY, SELL, ou ACCUMULATE
        confidence: Confiança do sinal (0.0-1.0)
        reasoning: Explicação do sinal
    
    Returns:
        Dict com resultado da submissão e payment
        
    Example:
        result = submit_signal(
            signal_json='{"direction": "UP", "entry": 50000}',
            asset="BTC",
            signal_type="BUY",
            confidence=0.85,
            reasoning="Análise técnica mostra suporte forte..."
        )
    """
    tracker = _global_state.get('tracker')
    
    if not tracker:
        return {
            "error": "EconomicTracker not initialized"
        }
    
    # Validar signal_json
    try:
        signal_data = json.loads(signal_json)
    except json.JSONDecodeError as e:
        return {
            "error": f"Invalid JSON: {str(e)}"
        }
    
    # Validar confidence
    if not 0.0 <= confidence <= 1.0:
        return {
            "error": "Confidence must be between 0.0 and 1.0",
            "received": confidence
        }
    
    # Validar signal_type
    valid_types = ["BUY", "SELL", "ACCUMULATE"]
    if signal_type.upper() not in valid_types:
        return {
            "error": f"Invalid signal_type. Must be one of: {valid_types}"
        }
    
    # Simular avaliação do sinal
    # Na implementação real, isso seria avaliado após o mercado fechar
    evaluation_score = min(1.0, confidence + 0.1)  # Simplificado
    base_payment = 0.10  # $0.10 USDC por sinal
    payment = base_payment * evaluation_score
    
    # Registrar revenue
    signal_id = f"signal_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
    tracker.record_revenue(
        amount=payment,
        signal_id=signal_id,
        description=f"Signal sold: {signal_type} {asset}",
        metadata={
            "asset": asset,
            "signal_type": signal_type,
            "confidence": confidence,
            "evaluation_score": evaluation_score
        }
    )
    
    # Retorno
    return {
        "success": True,
        "signal_id": signal_id,
        "asset": asset,
        "signal_type": signal_type,
        "confidence": confidence,
        "evaluation_score": evaluation_score,
        "payment": payment,
        "balance_after": tracker.balance,
        "timestamp": datetime.utcnow().isoformat(),
        "message": f"✅ Signal submitted: {signal_type} {asset} | Payment: ${payment:.4f}"
    }


# Tools export (para OpenClaw skills)
TOOLS = {
    'decide_activity': decide_activity,
    'get_status': get_status,
    'submit_signal': submit_signal
}


# Teste
if __name__ == "__main__":
    print("🧪 Testando Alpha Signals Tools\n")
    
    # Inicializar tracker
    tracker = EconomicTracker(
        agent_id="test_agent",
        initial_balance=100.0
    )
    set_global_state(tracker)
    
    # Test 1: Decide activity (work)
    print("="*60)
    print("TEST 1: decide_activity")
    print("="*60)
    result = decide_activity(
        "work",
        "Preciso gerar revenue para manter o agente ativo e saudável. Vou criar sinais de qualidade."
    )
    print(f"Result: {json.dumps(result, indent=2)}\n")
    
    # Test 2: Get status
    print("="*60)
    print("TEST 2: get_status")
    print("="*60)
    status = get_status()
    print(f"Status: {json.dumps(status, indent=2)}\n")
    
    # Test 3: Submit signal
    print("="*60)
    print("TEST 3: submit_signal")
    print("="*60)
    signal = {
        "direction": "UP",
        "entry": 50000,
        "stop_loss": 49000,
        "take_profit": 52000
    }
    result = submit_signal(
        signal_json=json.dumps(signal),
        asset="BTC",
        signal_type="BUY",
        confidence=0.85,
        reasoning="Suporte forte em $49k, RSI divergência positiva, volume aumentando"
    )
    print(f"Result: {json.dumps(result, indent=2)}\n")
    
    # Status final
    print("="*60)
    print("STATUS FINAL")
    print("="*60)
    tracker.print_status()
    print(f"\n{tracker.get_cost_footer()}\n")
