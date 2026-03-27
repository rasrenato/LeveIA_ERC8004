#!/bin/bash
# Script para rodar todos os testes

cd /root/openclaw

# Ativar ambiente virtual
source venv_chainlink/bin/activate

echo "============================================================"
echo "🧪 RODANDO TESTES - LEVE IA"
echo "============================================================"

# Rodar testes do yield calculator
echo ""
echo "1️⃣ Testes do Yield Calculator..."
python3 -m pytest alpha_signals/test_yield_calculator.py -v --tb=short

# Rodar testes do smart contract (se existir)
if [ -f "contracts/test_proof_of_yield.py" ]; then
    echo ""
    echo "2️⃣ Testes do Smart Contract..."
    python3 -m pytest contracts/test_proof_of_yield.py -v --tb=short
fi

echo ""
echo "============================================================"
echo "✅ TESTES CONCLUÍDOS!"
echo "============================================================"
