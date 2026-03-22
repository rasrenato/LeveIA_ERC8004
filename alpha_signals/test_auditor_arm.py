#!/usr/bin/env python3
"""
Teste do Braço Auditor - Validação Dupla
Testa a função validate_signal_alibaba_auditor() diretamente
"""

import os
import sys
sys.path.insert(0, '/root/openclaw/alpha_signals')
os.chdir('/root/openclaw/alpha_signals')

# Importar a função do auditor
from alpha_signals_v3 import validate_signal_alibaba_auditor, logger

# Sinal de teste (simulado)
test_signal = {
    'symbol': 'BTC/USDT',
    'direction': 'LONG',
    'entry_min': 88000,
    'entry_max': 90000,
    'stop_loss': 85000,
    'targets': [
        {'tp': 95000, 'percentage': 30},
        {'tp': 100000, 'percentage': 35},
        {'tp': 105000, 'percentage': 35}
    ],
    'risk_reward': 2.5,
    'confidence': 85,
    'timeframe': 'Swing Trade (5-15 dias)'
}

print("=" * 60)
print("🧪 TESTE DO BRAÇO AUDITOR - LEVE IA")
print("=" * 60)

# Verificar se a key está carregada
auditor_key = os.getenv('ALIBABA_AUDITOR_KEY', '')
print(f"\n📋 STATUS DA CHAVE:")
print(f"   ALIBABA_AUDITOR_KEY: {'✅ Carregada' if auditor_key and len(auditor_key) > 10 else '❌ NÃO CARREGADA'}")
print(f"   Tamanho: {len(auditor_key)} caracteres")

# Veredito do DeepSeek (simulado)
deepseek_verdict = "LONG @ 85%"

print(f"\n🔍 TESTANDO VALIDAÇÃO DUPLA:")
print(f"   Sinal: {test_signal['symbol']} {test_signal['direction']}")
print(f"   DeepSeek Verdict: {deepseek_verdict}")
print(f"   R/R: 1:{test_signal['risk_reward']}")
print(f"   Confiança: {test_signal['confidence']}%")

print(f"\n⏳ Chamando Auditor de IA Independente...")

# Chamar o auditor
result = validate_signal_alibaba_auditor(test_signal, deepseek_verdict)

print(f"\n{'=' * 60}")
print(f"📊 RESULTADO:")
print(f"   Veredito do Auditor: {'✅ VALIDATED' if result else '❌ REJECTED'}")
print(f"   Sinal APROVADO para operação: {'✅ SIM' if result else '❌ NÃO'}")
print(f"{'=' * 60}")

# Verificar logs
print(f"\n📝 Verifique o log em: /opt/leveclaw/backend/logs/alpha-signals.log")
print(f"   Procure por: 'DUAL-AI LOG' ou 'Auditor'")
