#!/bin/bash
# Cron job para calcular yield dos sinais
# Roda a cada 6 horas
set -euo pipefail

source /root/openclaw/.leveia_paths 2>/dev/null || true
WORKSPACE_DIR="${WORKSPACE_DIR:-/root/openclaw}"
cd "$WORKSPACE_DIR"

# Ativar ambiente virtual
source venv_chainlink/bin/activate

# Rodar calculadora
python3 alpha_signals/yield_calculator.py --calculate >> logs/yield_calculator.log 2>&1

echo "Yield calculado em $(date)" >> logs/yield_calculator.log
