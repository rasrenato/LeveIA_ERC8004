#!/bin/bash
# Leve IA - Alpha Signals Engine Runner
# TRAVA DE CEO: Este script roda EXCLUSIVAMENTE na Nvidia para economizar a DeepSeek

cd /root/openclaw/alpha_signals

# Forçando as variáveis apenas para esta execução
export LLM_PROVIDER="nvidia-nim"
export DEFAULT_MODEL="moonshotai/kimi-k2.5"

# 1. Expirar sinais antigos (>3 dias) antes de gerar novos
echo "🔄 Expirando sinais antigos (>3 dias)..."
python3 expire_signals_simple.py --max-age-days 3

# 2. Gerar novos sinais
echo "🚀 Gerando novos sinais..."
python3 alpha_signals_v3.py --generate
