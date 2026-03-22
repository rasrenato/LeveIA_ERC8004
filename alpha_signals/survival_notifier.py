"""
Survival Status Notifier - Notificações de status econômico

Inspirado no ClawWork survival status
Adaptado para LeveCoin Alpha Signals

Status:
- 🟢 thriving: Saldo > $20 (saudável)
- 🟡 struggling: $10 <= Saldo < $20 (atenção)
- 🔴 critical: $0 < Saldo < $10 (crítico)
- 💀 dead: Saldo <= $0 (faleceu)

Notificações:
- Telegram (via OpenClaw message tool)
- Console (logs)
- Webhook (opcional)
"""

import os
import json
from typing import Dict, Optional, Callable
from datetime import datetime
from pathlib import Path

# Import EconomicTracker
import sys
sys.path.insert(0, '/root/openclaw')
from alpha_signals.economic_tracker import EconomicTracker


class SurvivalNotifier:
    """
    Notificador de Survival Status
    
    Envia alertas quando:
    - Status muda (thriving → struggling, etc.)
    - Saldo crítico (< $10)
    - Agente "morre" (saldo <= 0)
    """

    def __init__(
        self,
        tracker: EconomicTracker,
        telegram_chat_id: Optional[str] = None,
        webhook_url: Optional[str] = None,
        data_path: Optional[str] = None
    ):
        """
        Inicializa notificador
        
        Args:
            tracker: EconomicTracker instância
            telegram_chat_id: ID do chat Telegram para alertas
            webhook_url: URL para webhooks (opcional)
            data_path: Path para salvar logs de notificações
        """
        self.tracker = tracker
        self.telegram_chat_id = telegram_chat_id or os.getenv('TELEGRAM_CHAT_ID')
        self.webhook_url = webhook_url
        self.data_path = data_path or f"./data/notifications/{tracker.agent_id}"
        
        Path(self.data_path).mkdir(parents=True, exist_ok=True)
        
        # Estado anterior (para detectar mudanças)
        self.last_status = tracker.survival_status
        self.last_balance = tracker.balance
        
        # Callbacks opcionais
        self.on_status_change: Optional[Callable] = None
        self.on_critical: Optional[Callable] = None
        self.on_death: Optional[Callable] = None
        
        # Carregar histórico
        self.notification_log = self._load_log()

    def _load_log(self) -> list:
        """Carrega log de notificações"""
        log_path = os.path.join(self.data_path, "notifications.json")
        if os.path.exists(log_path):
            with open(log_path, 'r') as f:
                return json.load(f)
        return []

    def _save_log(self):
        """Salva log de notificações"""
        log_path = os.path.join(self.data_path, "notifications.json")
        with open(log_path, 'w') as f:
            json.dump(self.notification_log, f, indent=2)

    def _log_notification(self, notification_type: str, message: str, metadata: Dict = None):
        """Registra notificação no log"""
        entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'type': notification_type,
            'message': message,
            'metadata': metadata or {}
        }
        self.notification_log.append(entry)
        self._save_log()

    def check_status(self) -> Dict:
        """
        Verifica status e envia notificações se necessário
        
        Returns:
            Dict com resultado da verificação
        """
        current_status = self.tracker.survival_status
        current_balance = self.tracker.balance
        
        result = {
            'status': current_status,
            'balance': current_balance,
            'notifications_sent': 0,
            'changes': []
        }
        
        # Detectar mudança de status
        if current_status != self.last_status:
            change_msg = f"Status changed: {self.last_status} → {current_status}"
            result['changes'].append(change_msg)
            
            # Notificar mudança
            self._send_status_change_notification(
                old_status=self.last_status,
                new_status=current_status,
                balance=current_balance
            )
            result['notifications_sent'] += 1
            
            # Callback
            if self.on_status_change:
                self.on_status_change(self.last_status, current_status, current_balance)
        
        # Detectar saldo crítico
        if current_status == "critical" and self.last_status != "critical":
            self._send_critical_alert(current_balance)
            result['notifications_sent'] += 1
            
            # Callback
            if self.on_critical:
                self.on_critical(current_balance)
        
        # Detectar morte do agente
        if current_status == "dead" and self.last_status != "dead":
            self._send_death_notification(current_balance)
            result['notifications_sent'] += 1
            
            # Callback
            if self.on_death:
                self.on_death(current_balance)
        
        # Atualizar estado
        self.last_status = current_status
        self.last_balance = current_balance
        
        return result

    def _send_status_change_notification(
        self,
        old_status: str,
        new_status: str,
        balance: float
    ):
        """Envia notificação de mudança de status"""
        emojis = {
            'thriving': '🟢',
            'struggling': '🟡',
            'critical': '🔴',
            'dead': '💀'
        }
        
        message = (
            f"{emojis.get(new_status, '⚪')} **Survival Status Changed**\n\n"
            f"From: {emojis.get(old_status, '?')} {old_status}\n"
            f"To: {emojis.get(new_status, '?')} {new_status}\n\n"
            f"💰 Balance: ${balance:.2f}\n"
            f"⏰ {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}"
        )
        
        # Log
        self._log_notification(
            'status_change',
            message,
            {'old_status': old_status, 'new_status': new_status, 'balance': balance}
        )
        
        # Console
        print(f"\n{message}\n")
        
        # Telegram (se configurado)
        if self.telegram_chat_id:
            self._send_telegram_message(message)

    def _send_critical_alert(self, balance: float):
        """Envia alerta crítico"""
        message = (
            f"🔴 **CRITICAL ALERT** 🔴\n\n"
            f"Agent {self.tracker.agent_id} is in CRITICAL condition!\n\n"
            f"💰 Balance: ${balance:.2f}\n"
            f"⚠️ Action required: Generate revenue immediately!\n\n"
            f"⏰ {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}"
        )
        
        # Log
        self._log_notification('critical_alert', message, {'balance': balance})
        
        # Console
        print(f"\n{message}\n")
        
        # Telegram
        if self.telegram_chat_id:
            self._send_telegram_message(message)

    def _send_death_notification(self, balance: float):
        """Envia notificação de morte do agente"""
        message = (
            f"💀 **AGENT DECEASED** 💀\n\n"
            f"Agent {self.tracker.agent_id} has run out of funds.\n\n"
            f"💰 Final Balance: ${balance:.2f}\n"
            f"📊 Total Revenue: ${self.tracker.total_revenue:.2f}\n"
            f"📉 Total Costs: ${self.tracker.total_costs:.2f}\n\n"
            f"⏰ {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}"
        )
        
        # Log
        self._log_notification('agent_death', message, {'balance': balance})
        
        # Console
        print(f"\n{message}\n")
        
        # Telegram
        if self.telegram_chat_id:
            self._send_telegram_message(message)

    def _send_telegram_message(self, message: str):
        """Envia mensagem via Telegram (via OpenClaw)"""
        try:
            # Import message tool do OpenClaw
            from openclaw import message
            
            message.send(
                action='send',
                channel='telegram',
                target=self.telegram_chat_id,
                message=message
            )
            print(f"📱 Telegram notification sent to {self.telegram_chat_id}")
        except Exception as e:
            print(f"⚠️ Failed to send Telegram notification: {e}")
            self._log_notification('telegram_error', str(e))

    def get_notification_history(self, limit: int = 10) -> list:
        """Retorna histórico de notificações"""
        return self.notification_log[-limit:]

    def print_summary(self):
        """Imprime resumo de notificações"""
        print("\n" + "="*60)
        print(f"📬 NOTIFICATION SUMMARY - {self.tracker.agent_id}")
        print("="*60)
        
        total = len(self.notification_log)
        by_type = {}
        for entry in self.notification_log:
            t = entry.get('type', 'unknown')
            by_type[t] = by_type.get(t, 0) + 1
        
        print(f"Total notifications: {total}")
        for t, count in sorted(by_type.items()):
            print(f"  • {t}: {count}")
        
        print("="*60 + "\n")


# Exemplo de uso
if __name__ == "__main__":
    print("🧪 Testando Survival Notifier\n")
    
    # Criar tracker
    tracker = EconomicTracker(
        agent_id="test_notifier",
        initial_balance=50.0,
        critical_threshold=20.0
    )
    
    # Criar notifier
    notifier = SurvivalNotifier(tracker)
    
    # Test 1: Status inicial (thriving)
    print("="*60)
    print("TEST 1: Initial status (thriving)")
    print("="*60)
    result = notifier.check_status()
    print(f"Result: {result}\n")
    
    # Test 2: Simular gastos até struggling
    print("="*60)
    print("TEST 2: Simulate expenses → struggling")
    print("="*60)
    tracker.record_api_call(tokens_used=1000, description="Test call 1")
    tracker.record_api_call(tokens_used=1000, description="Test call 2")
    tracker.record_api_call(tokens_used=1000, description="Test call 3")
    tracker.record_api_call(tokens_used=1000, description="Test call 4")
    tracker.record_api_call(tokens_used=1000, description="Test call 5")
    tracker.record_api_call(tokens_used=1000, description="Test call 6")
    tracker.record_api_call(tokens_used=1000, description="Test call 7")
    tracker.record_api_call(tokens_used=1000, description="Test call 8")
    tracker.record_api_call(tokens_used=1000, description="Test call 9")
    tracker.record_api_call(tokens_used=1000, description="Test call 10")
    
    result = notifier.check_status()
    print(f"Result: {result}\n")
    
    # Test 3: Simular mais gastos até critical
    print("="*60)
    print("TEST 3: More expenses → critical")
    print("="*60)
    for i in range(20):
        tracker.record_api_call(tokens_used=500, description=f"Test call {i+11}")
    
    result = notifier.check_status()
    print(f"Result: {result}\n")
    
    # Test 4: Status final
    print("="*60)
    print("TEST 4: Final status")
    print("="*60)
    tracker.print_status()
    notifier.print_summary()
