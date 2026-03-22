// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@chainlink/contracts/src/v0.8/shared/interfaces/AggregatorV3Interface.sol";

/**
 * @title ProofOfYield - Leve IA
 * @dev Contrato para registrar sinais de trading e provar yield on-chain
 * 
 * Funcionamento:
 * 1. IA gera sinal → registerSignal()
 * 2. Sinal registrado na blockchain com hash
 * 3. Qualquer um pode verificar no BscScan
 */
contract ProofOfYield is Ownable {
    
    // Estrutura do Sinal
    struct Signal {
        uint256 signalId;
        string symbol;           // "BTC/USDT", "ETH/USDT"
        string direction;        // "LONG" ou "SHORT"
        uint256 entryPrice;      // Preço de entrada (x10^8)
        uint256 targetPrice;     // Preço alvo (x10^8)
        uint256 stopLoss;        // Stop loss (x10^8)
        uint256 timestamp;       // Quando foi gerado
        address agentAddress;    // Quem gerou o sinal
        bool isResolved;         // Se já foi verificado
        int256 yieldBps;         // Yield em basis points (100 = 1%)
        string status;           // "WIN", "LOSS", "PENDING"
    }
    
    // Mapeamentos
    mapping(uint256 => Signal) public signals;
    mapping(address => uint256) public agentYield;    // Yield total por agente
    mapping(address => uint256) public agentSignals;  // Qtd sinais por agente
    
    // Contadores
    uint256 public signalCount;
    uint256 public totalYieldBps;  // Yield total acumulado (basis points)
    
    // Chainlink Oracles (Base Mainnet)
    address constant ETH_USD_FEED = 0x71041dddad3595F9CEd3DcCFBe3D1F4b0a16Bb70;
    address constant BTC_USD_FEED = 0xF4030086522a5bEEa4988F8cA5B36dbC97BeE88c;
    
    AggregatorV3Interface internal ethFeed;
    AggregatorV3Interface internal btcFeed;
    
    // Eventos
    event SignalRegistered(
        uint256 indexed signalId,
        string symbol,
        string direction,
        uint256 entryPrice,
        uint256 timestamp,
        address indexed agent
    );
    
    event SignalResolved(
        uint256 indexed signalId,
        int256 yieldBps,
        string status,
        uint256 timestamp
    );
    
    constructor() Ownable(msg.sender) {
        ethFeed = AggregatorV3Interface(ETH_USD_FEED);
        btcFeed = AggregatorV3Interface(BTC_USD_FEED);
    }
    
    /**
     * @dev Registra novo sinal da IA
     */
    function registerSignal(
        string memory symbol,
        string memory direction,
        uint256 entryPrice,
        uint256 targetPrice,
        uint256 stopLoss
    ) external returns (uint256) {
        require(bytes(symbol).length > 0, "Symbol required");
        require(entryPrice > 0, "Entry price must be > 0");
        require(targetPrice > 0, "Target price must be > 0");
        require(stopLoss > 0, "Stop loss must be > 0");
        
        signalCount++;
        
        signals[signalCount] = Signal({
            signalId: signalCount,
            symbol: symbol,
            direction: direction,
            entryPrice: entryPrice,
            targetPrice: targetPrice,
            stopLoss: stopLoss,
            timestamp: block.timestamp,
            agentAddress: msg.sender,
            isResolved: false,
            yieldBps: 0,
            status: "PENDING"
        });
        
        agentSignals[msg.sender]++;
        
        emit SignalRegistered(
            signalCount,
            symbol,
            direction,
            entryPrice,
            block.timestamp,
            msg.sender
        );
        
        return signalCount;
    }
    
    /**
     * @dev Resolve sinal (WIN ou LOSS)
     */
    function resolveSignal(
        uint256 signalId,
        int256 yieldBps,
        string memory status
    ) external {
        require(signalId <= signalCount, "Signal does not exist");
        require(!signals[signalId].isResolved, "Signal already resolved");
        require(
            keccak256(bytes(status)) == keccak256(bytes("WIN")) ||
            keccak256(bytes(status)) == keccak256(bytes("LOSS")),
            "Status must be WIN or LOSS"
        );
        
        Signal storage signal = signals[signalId];
        signal.isResolved = true;
        signal.yieldBps = yieldBps;
        signal.status = status;
        
        // Atualizar yield do agente
        if (yieldBps > 0) {
            agentYield[signal.agentAddress] += uint256(yieldBps);
            totalYieldBps += uint256(yieldBps);
        }
        
        emit SignalResolved(signalId, yieldBps, status, block.timestamp);
    }
    
    /**
     * @dev Obtém preço atual via Chainlink
     */
    function getPrice(string memory symbol) public view returns (uint256) {
        AggregatorV3Interface feed;
        
        if (keccak256(bytes(symbol)) == keccak256(bytes("BTC/USDT")) ||
            keccak256(bytes(symbol)) == keccak256(bytes("BTC/USD"))) {
            feed = btcFeed;
        } else {
            feed = ethFeed;
        }
        
        (, int256 price,,,) = feed.latestRoundData();
        require(price > 0, "Invalid price");
        
        return uint256(price);
    }
    
    /**
     * @dev Verifica se sinal foi WIN
     */
    function isWin(uint256 signalId, uint256 exitPrice) public view returns (bool) {
        require(signalId <= signalCount, "Signal does not exist");
        Signal memory signal = signals[signalId];
        
        if (keccak256(bytes(signal.direction)) == keccak256(bytes("LONG"))) {
            return exitPrice > signal.entryPrice;
        } else {
            return exitPrice < signal.entryPrice;
        }
    }
    
    /**
     * @dev Estatísticas do agente
     */
    function getAgentStats(address agent) external view returns (
        uint256 totalSignals,
        uint256 totalYield,
        uint256 avgYield
    ) {
        totalSignals = agentSignals[agent];
        totalYield = agentYield[agent];
        avgYield = totalSignals > 0 ? totalYield / totalSignals : 0;
    }
}
