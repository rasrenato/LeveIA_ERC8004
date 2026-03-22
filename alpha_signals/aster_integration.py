"""
Aster-MCP Integration - Alpha Signals

Integração com Aster-MCP para execução automática de sinais.
"""

import subprocess
import json
import logging
from typing import Dict, Optional, Any
from pathlib import Path

logger = logging.getLogger(__name__)

ASTER_MCP_PATH = Path("/root/openclaw/aster-mcp")
ASTER_VENV = ASTER_MCP_PATH / "venv" / "bin" / "activate"


class AsterIntegration:
    """
    Integração com Aster-MCP para execução de sinais
    
    Funcionalidades:
    - Executar ordens baseadas em sinais do Alpha Signals
    - Suporte para testnet e mainnet
    - Monitoramento de execuções
    """
    
    def __init__(self, account_id: str = "main", testnet: bool = True):
        """
        Inicializa integração com Aster-MCP
        
        Args:
            account_id: ID da conta configurada no Aster-MCP
            testnet: Se True, usa testnet (recomendado para produção)
        """
        self.account_id = account_id
        self.testnet = testnet
        self.mcp_cli = self._get_mcp_cli()
    
    def _get_mcp_cli(self) -> str:
        """Retorna caminho do CLI Aster-MCP"""
        return str(ASTER_VENV.parent.parent / "bin" / "aster-mcp")
    
    def _run_command(self, command: list) -> Dict[str, Any]:
        """
        Executa comando Aster-MCP
        
        Args:
            command: Lista de argumentos
            
        Returns:
            Resultado da execução
        """
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                try:
                    return json.loads(result.stdout)
                except json.JSONDecodeError:
                    return {"status": "success", "output": result.stdout}
            else:
                logger.error(f"Erro no comando: {result.stderr}")
                return {"status": "error", "error": result.stderr}
                
        except subprocess.TimeoutExpired:
            logger.error("Timeout no comando Aster-MCP")
            return {"status": "error", "error": "Timeout"}
        except Exception as e:
            logger.error(f"Exceção no Aster-MCP: {e}")
            return {"status": "error", "error": str(e)}
    
    def test_connection(self) -> bool:
        """
        Testa conexão com Aster-MCP
        
        Returns:
            True se conexão bem-sucedida
        """
        result = self._run_command([
            self.mcp_cli, "test", self.account_id
        ])
        
        return result.get("status") == "success"
    
    def execute_signal(self, signal: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executa sinal via Aster-MCP
        
        Args:
            signal: Dicionário com dados do sinal
                {
                    "asset": "BTCUSDT",
                    "direction": "UP" ou "DOWN",
                    "confidence": 0.85,
                    "size": 0.01  # Tamanho da ordem
                }
                
        Returns:
            Resultado da execução
        """
        # Converter direção do sinal para lado da ordem
        side = "BUY" if signal.get("direction") == "UP" else "SELL"
        symbol = signal.get("asset", "BTCUSDT")
        size = signal.get("size", 0.01)
        
        logger.info(f"Executando sinal: {side} {size} {symbol}")
        
        # Executar ordem via Aster-MCP
        result = self._run_command([
            self.mcp_cli, "start",  # Inicia servidor MCP
            "--account", self.account_id,
            "--symbol", symbol,
            "--side", side,
            "--size", str(size),
            "--type", "MARKET"  # Ordem a mercado para execução imediata
        ])
        
        # Log da execução
        if result.get("status") == "success":
            logger.info(f"Sinal executado com sucesso: {result}")
        else:
            logger.error(f"Falha na execução: {result}")
        
        return result
    
    def get_balance(self) -> Dict[str, Any]:
        """
        Obtém saldo da conta
        
        Returns:
            Saldo e informações da conta
        """
        result = self._run_command([
            self.mcp_cli, "list"
        ])
        
        return result
    
    def start_mcp_server(self) -> bool:
        """
        Inicia servidor MCP em background
        
        Returns:
            True se iniciado com sucesso
        """
        try:
            # Iniciar servidor MCP
            subprocess.Popen([
                self.mcp_cli, "start"
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            logger.info("Servidor MCP iniciado")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao iniciar MCP: {e}")
            return False
    
    def stop_mcp_server(self) -> bool:
        """
        Para servidor MCP
        
        Returns:
            True se parado com sucesso
        """
        result = self._run_command([
            self.mcp_cli, "stop"
        ])
        
        return result.get("status") == "success"
    
    def configure_account(
        self,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        auth_type: str = "hmac"
    ) -> bool:
        """
        Configura conta Aster-MCP
        
        Args:
            api_key: API Key da Aster
            api_secret: API Secret da Aster
            auth_type: "hmac" ou "eip712"
            
        Returns:
            True se configurado com sucesso
        """
        logger.info(f"Configurando conta {self.account_id} ({auth_type})")
        
        # Nota: Configuração interativa requer input do usuário
        # Para automação, usar arquivo de config direto
        
        config_file = Path.home() / ".config" / "aster-mcp" / "config.json"
        config_file.parent.mkdir(parents=True, exist_ok=True)
        
        config = {
            "accounts": {
                self.account_id: {
                    "api_key": api_key,
                    "api_secret": api_secret,
                    "auth_type": auth_type,
                    "base_url": "https://fapi.asterdex.com"
                }
            }
        }
        
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        logger.info(f"Conta {self.account_id} configurada")
        return True


# Exemplo de uso
if __name__ == "__main__":
    # Testar integração
    aster = AsterIntegration(account_id="main", testnet=True)
    
    print("Testando conexão com Aster-MCP...")
    if aster.test_connection():
        print("✅ Conexão bem-sucedida!")
        
        # Exemplo de execução de sinal
        signal = {
            "asset": "BTCUSDT",
            "direction": "UP",
            "confidence": 0.85,
            "size": 0.01
        }
        
        print(f"\nExecutando sinal: {signal}")
        result = aster.execute_signal(signal)
        print(f"Resultado: {result}")
    else:
        print("❌ Falha na conexão")
        print("\n⚠️  Para configurar:")
        print("1. Execute: aster-mcp config")
        print("2. Preencha API Key e Secret")
        print("3. Teste: aster-mcp test main")
