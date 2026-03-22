#!/usr/bin/env python3
"""
Testes unitários para Yield Calculator

Executar:
    pytest alpha_signals/test_yield_calculator.py -v --cov=alpha_signals/yield_calculator
"""

import pytest
from decimal import Decimal
from unittest.mock import patch, MagicMock
import sys
sys.path.insert(0, '/root/openclaw/alpha_signals')

# Importar funções para testar
from yield_calculator import calculate_yield, get_current_price


class TestCalculateYield:
    """Testes para função calculate_yield."""
    
    def test_long_profit(self):
        """LONG com lucro (preço subiu)."""
        entry = Decimal("100.00")
        exit = Decimal("120.00")
        direction = "LONG"
        
        result = calculate_yield(entry, exit, direction)
        
        assert result == Decimal("20.00")  # 20% de lucro
    
    def test_long_loss(self):
        """LONG com prejuízo (preço caiu)."""
        entry = Decimal("100.00")
        exit = Decimal("80.00")
        direction = "LONG"
        
        result = calculate_yield(entry, exit, direction)
        
        assert result == Decimal("-20.00")  # -20% de prejuízo
    
    def test_short_profit(self):
        """SHORT com lucro (preço caiu)."""
        entry = Decimal("100.00")
        exit = Decimal("80.00")
        direction = "SHORT"
        
        result = calculate_yield(entry, exit, direction)
        
        assert result == Decimal("20.00")  # 20% de lucro
    
    def test_short_loss(self):
        """SHORT com prejuízo (preço subiu)."""
        entry = Decimal("100.00")
        exit = Decimal("120.00")
        direction = "SHORT"
        
        result = calculate_yield(entry, exit, direction)
        
        assert result == Decimal("-20.00")  # -20% de prejuízo
    
    def test_breakeven(self):
        """Breakeven (mesmo preço)."""
        entry = Decimal("100.00")
        exit = Decimal("100.00")
        direction = "LONG"
        
        result = calculate_yield(entry, exit, direction)
        
        assert result == Decimal("0.00")
    
    def test_large_profit(self):
        """Lucro grande (10x)."""
        entry = Decimal("10.00")
        exit = Decimal("100.00")
        direction = "LONG"
        
        result = calculate_yield(entry, exit, direction)
        
        assert result == Decimal("900.00")  # 900% de lucro
    
    def test_large_loss(self):
        """Prejuízo grande (-90%)."""
        entry = Decimal("100.00")
        exit = Decimal("10.00")
        direction = "LONG"
        
        result = calculate_yield(entry, exit, direction)
        
        assert result == Decimal("-90.00")  # -90% de prejuízo
    
    def test_decimal_precision(self):
        """Precisão decimal."""
        entry = Decimal("100.00")
        exit = Decimal("100.50")
        direction = "LONG"
        
        result = calculate_yield(entry, exit, direction)
        
        assert result == Decimal("0.50")  # 0.5% de lucro


class TestGetCurrentPrice:
    """Testes para função get_current_price."""
    
    @patch('yield_calculator.requests.get')
    def test_binance_api_success(self, mock_get):
        """Binance API retorna com sucesso."""
        # Mock da resposta
        mock_response = MagicMock()
        mock_response.json.return_value = {'price': '50000.00'}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = get_current_price("BTC/USDT")
        
        assert result == Decimal("50000.00")
        mock_get.assert_called_once()
    
    @patch('yield_calculator.requests.get')
    def test_binance_api_failure(self, mock_get):
        """Binance API falha."""
        mock_get.side_effect = Exception("API Error")
        
        result = get_current_price("BTC/USDT")
        
        assert result == Decimal(0)
    
    def test_unknown_symbol(self):
        """Símbolo desconhecido."""
        result = get_current_price("UNKNOWN/USDT")
        
        # Deve tentar extrair símbolo base e falhar
        assert result == Decimal(0)


class TestIntegration:
    """Testes de integração."""
    
    def test_calculate_yield_workflow(self):
        """Fluxo completo de cálculo."""
        # Simular cenário real
        entry_price = Decimal("89000.00")  # BTC entrada
        current_price = Decimal("67376.16")  # BTC atual (queda)
        direction = "LONG"
        
        yield_pct = calculate_yield(entry_price, current_price, direction)
        
        # Deve ser negativo (LOSS)
        assert yield_pct < 0
        assert yield_pct == Decimal("-24.29644943820224719101123596")
    
    def test_multiple_signals(self):
        """Múltiplos sinais com diferentes resultados."""
        signals = [
            {"entry": Decimal("100"), "exit": Decimal("120"), "dir": "LONG", "expected": Decimal("20")},
            {"entry": Decimal("100"), "exit": Decimal("80"), "dir": "LONG", "expected": Decimal("-20")},
            {"entry": Decimal("100"), "exit": Decimal("80"), "dir": "SHORT", "expected": Decimal("20")},
            {"entry": Decimal("100"), "exit": Decimal("120"), "dir": "SHORT", "expected": Decimal("-20")},
        ]
        
        for signal in signals:
            result = calculate_yield(signal["entry"], signal["exit"], signal["dir"])
            assert result == signal["expected"], f"Falhou para {signal}"


class TestEdgeCases:
    """Testes para casos extremos."""
    
    def test_zero_entry_price(self):
        """Preço de entrada zero (divisão por zero)."""
        with pytest.raises(ZeroDivisionError):
            calculate_yield(Decimal("0"), Decimal("100"), "LONG")
    
    def test_negative_prices(self):
        """Preços negativos (não deve acontecer)."""
        # Na prática, preços não são negativos
        # Mas o código deve lidar com isso
        entry = Decimal("-100")
        exit = Decimal("-80")
        direction = "LONG"
        
        result = calculate_yield(entry, exit, direction)
        
        # Deve calcular normalmente (matematicamente correto)
        assert result == Decimal("-20")
    
    def test_very_small_yield(self):
        """Yield muito pequeno."""
        entry = Decimal("100.00")
        exit = Decimal("100.01")
        direction = "LONG"
        
        result = calculate_yield(entry, exit, direction)
        
        assert result > 0
        assert result < Decimal("1")  # Menor que 1%


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=alpha_signals/yield_calculator"])
