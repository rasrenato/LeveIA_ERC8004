// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title ERC-8126 - Risk Scoring Layer for AI Agents
 * @dev Implementação do padrão ERC-8126 para scoring de risco de agentes
 * 
 * Deploy na Binance Smart Chain (BSC)
 * 
 * Features:
 * - Risk scores para agentes (0-1000)
 * - Histórico de performance
 * - Slashing por mau comportamento
 * - Reputation integration
 */
contract ERC8126 is Ownable {
    
    // Estrutura do Risk Score
    struct AgentRisk {
        uint256 score; // 0-1000 (1000 = máximo risco)
        uint256 totalTasks;
        uint256 successfulTasks;
        uint256 failedTasks;
        uint256 lastUpdated;
        bool isRegistered;
    }
    
    // Mapeamentos
    mapping(address => AgentRisk) public agentRisks;
    mapping(address => uint256[]) public agentHistory;
    mapping(uint256 => RiskEvent) public riskEvents;
    
    uint256 public riskEventCount;
    
    // Eventos de Risk
    enum RiskEventType {
        TASK_SUCCESS,
        TASK_FAILURE,
        SCORE_UPDATE,
        SLASHING,
        REGISTRATION
    }
    
    struct RiskEvent {
        address agent;
        RiskEventType eventType;
        uint256 oldScore;
        uint256 newScore;
        uint256 timestamp;
        string metadata;
    }
    
    // Configurações
    uint256 public constant MAX_SCORE = 1000;
    uint256 public constant BASE_SUCCESS_BONUS = 10;
    uint256 public constant BASE_FAILURE_PENALTY = 50;
    uint256 public constant SLASHING_PERCENTAGE = 100; // 10% do score
    
    // Events
    event AgentRegistered(address indexed agent, uint256 initialScore);
    event RiskScoreUpdated(address indexed agent, uint256 oldScore, uint256 newScore);
    event TaskCompleted(address indexed agent, bool success, uint256 scoreChange);
    event SlashingApplied(address indexed agent, uint256 amount, string reason);
    event RiskEventCreated(uint256 indexed eventId, address indexed agent, RiskEventType eventType);
    
    constructor() Ownable(msg.sender) {}
    
    /**
     * @dev Registrar novo agente
     */
    function registerAgent(address agent, uint256 initialScore) external onlyOwner {
        require(!agentRisks[agent].isRegistered, "Agent already registered");
        require(initialScore <= MAX_SCORE, "Score exceeds maximum");
        
        agentRisks[agent] = AgentRisk({
            score: initialScore,
            totalTasks: 0,
            successfulTasks: 0,
            failedTasks: 0,
            lastUpdated: block.timestamp,
            isRegistered: true
        });
        
        _createRiskEvent(agent, RiskEventType.REGISTRATION, 0, initialScore, "Agent registered");
        emit AgentRegistered(agent, initialScore);
    }
    
    /**
     * @dev Reportar tarefa completada com sucesso
     */
    function reportSuccess(address agent) external onlyOwner {
        require(agentRisks[agent].isRegistered, "Agent not registered");
        
        AgentRisk storage risk = agentRisks[agent];
        uint256 oldScore = risk.score;
        
        risk.totalTasks++;
        risk.successfulTasks++;
        risk.lastUpdated = block.timestamp;
        
        // Bonus por sucesso (diminui com score alto)
        uint256 bonus = BASE_SUCCESS_BONUS;
        if (risk.score > 500) {
            bonus = bonus * (MAX_SCORE - risk.score) / MAX_SCORE;
        }
        
        risk.score = risk.score + bonus > MAX_SCORE ? MAX_SCORE : risk.score + bonus;
        
        _createRiskEvent(agent, RiskEventType.TASK_SUCCESS, oldScore, risk.score, "Task completed successfully");
        emit TaskCompleted(agent, true, risk.score - oldScore);
        emit RiskScoreUpdated(agent, oldScore, risk.score);
    }
    
    /**
     * @dev Reportar tarefa falhada
     */
    function reportFailure(address agent) external onlyOwner {
        require(agentRisks[agent].isRegistered, "Agent not registered");
        
        AgentRisk storage risk = agentRisks[agent];
        uint256 oldScore = risk.score;
        
        risk.totalTasks++;
        risk.failedTasks++;
        risk.lastUpdated = block.timestamp;
        
        // Penalidade por falha
        risk.score = risk.score > BASE_FAILURE_PENALTY ? risk.score - BASE_FAILURE_PENALTY : 0;
        
        _createRiskEvent(agent, RiskEventType.TASK_FAILURE, oldScore, risk.score, "Task failed");
        emit TaskCompleted(agent, false, oldScore - risk.score);
        emit RiskScoreUpdated(agent, oldScore, risk.score);
    }
    
    /**
     * @dev Aplicar slashing por mau comportamento grave
     */
    function applySlashing(address agent, uint256 percentage, string calldata reason) external onlyOwner {
        require(agentRisks[agent].isRegistered, "Agent not registered");
        require(percentage <= 1000, "Percentage exceeds maximum"); // 1000 = 100%
        
        AgentRisk storage risk = agentRisks[agent];
        uint256 oldScore = risk.score;
        
        uint256 slashAmount = (risk.score * percentage) / 1000;
        risk.score = risk.score - slashAmount;
        risk.lastUpdated = block.timestamp;
        
        _createRiskEvent(agent, RiskEventType.SLASHING, oldScore, risk.score, reason);
        emit SlashingApplied(agent, slashAmount, reason);
        emit RiskScoreUpdated(agent, oldScore, risk.score);
    }
    
    /**
     * @dev Atualizar score manualmente
     */
    function updateScore(address agent, uint256 newScore) external onlyOwner {
        require(agentRisks[agent].isRegistered, "Agent not registered");
        require(newScore <= MAX_SCORE, "Score exceeds maximum");
        
        AgentRisk storage risk = agentRisks[agent];
        uint256 oldScore = risk.score;
        
        risk.score = newScore;
        risk.lastUpdated = block.timestamp;
        
        _createRiskEvent(agent, RiskEventType.SCORE_UPDATE, oldScore, newScore, "Manual score update");
        emit RiskScoreUpdated(agent, oldScore, newScore);
    }
    
    /**
     * @dev Obter risk score de um agente
     */
    function getRiskScore(address agent) external view returns (uint256 score, bool isRegistered) {
        if (!agentRisks[agent].isRegistered) {
            return (0, false);
        }
        return (agentRisks[agent].score, true);
    }
    
    /**
     * @dev Obter estatísticas de um agente
     */
    function getAgentStats(address agent) external view returns (
        uint256 score,
        uint256 totalTasks,
        uint256 successfulTasks,
        uint256 failedTasks,
        uint256 successRate
    ) {
        require(agentRisks[agent].isRegistered, "Agent not registered");
        
        AgentRisk memory risk = agentRisks[agent];
        successRate = risk.totalTasks > 0 ? (risk.successfulTasks * 10000) / risk.totalTasks : 0;
        
        return (
            risk.score,
            risk.totalTasks,
            risk.successfulTasks,
            risk.failedTasks,
            successRate
        );
    }
    
    /**
     * @dev Obter histórico de risk events
     */
    function getRiskEvents(address agent, uint256 offset, uint256 limit) external view returns (RiskEvent[] memory) {
        // Implementação simplificada - pode ser expandida
        return new RiskEvent[](0);
    }
    
    /**
     * @dev Criar risk event
     */
    function _createRiskEvent(
        address agent,
        RiskEventType eventType,
        uint256 oldScore,
        uint256 newScore,
        string memory metadata
    ) internal {
        riskEventCount++;
        riskEvents[riskEventCount] = RiskEvent({
            agent: agent,
            eventType: eventType,
            oldScore: oldScore,
            newScore: newScore,
            timestamp: block.timestamp,
            metadata: metadata
        });
        
        emit RiskEventCreated(riskEventCount, agent, eventType);
    }
}
