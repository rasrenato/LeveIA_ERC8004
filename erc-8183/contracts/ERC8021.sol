// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title ERC-8021 - Onchain Attribution for AI Agents
 * @dev Implementação do padrão ERC-8021 para atribuição onchain de contribuições
 * 
 * Deploy na Binance Smart Chain (BSC)
 * 
 * Features:
 * - Atribuição de contribuições para agentes
 * - Revenue sharing baseado em contribuições
 * - Histórico imutável de atribuições
 * - Integration com ERC-8183 (commercial layer)
 */
contract ERC8021 is Ownable {
    
    // Estrutura de Atribuição
    struct Attribution {
        uint256 attributionId;
        address contributor;
        address beneficiary;
        uint256 contributionType; // 0=Code, 1=Data, 2=Model, 3=Infrastructure, 4=Other
        uint256 weight; // 0-10000 (10000 = 100%)
        uint256 revenueShare; // Em basis points (100 = 1%)
        uint256 timestamp;
        string metadata; // IPFS hash ou descrição
        bool isActive;
    }
    
    // Estrutura de Revenue Share
    struct RevenueShare {
        address agent;
        uint256 totalRevenue;
        uint256 claimedRevenue;
        uint256[] attributionIds;
    }
    
    // Mapeamentos
    mapping(uint256 => Attribution) public attributions;
    mapping(address => RevenueShare) public revenueShares;
    mapping(address => uint256[]) public agentAttributions;
    mapping(address => mapping(address => uint256)) public contributorBeneficiary;
    
    uint256 public attributionCount;
    uint256 public totalRevenueDistributed;
    
    // Tipos de Contribuição
    enum ContributionType {
        Code,
        Data,
        Model,
        Infrastructure,
        Other
    }
    
    // Events
    event AttributionCreated(
        uint256 indexed attributionId,
        address indexed contributor,
        address indexed beneficiary,
        uint256 contributionType,
        uint256 weight,
        uint256 revenueShare
    );
    
    event AttributionUpdated(uint256 indexed attributionId, uint256 newWeight, uint256 newRevenueShare);
    event RevenueDistributed(address indexed agent, uint256 amount);
    event RevenueClaimed(address indexed agent, uint256 amount);
    event AttributionDeactivated(uint256 indexed attributionId);
    
    // Configurações
    uint256 public constant MAX_WEIGHT = 10000; // 100%
    uint256 public constant MAX_REVENUE_SHARE = 10000; // 100%
    uint256 public platformFeeBps; // Basis points
    
    constructor(uint256 _platformFeeBps) Ownable(msg.sender) {
        platformFeeBps = _platformFeeBps;
    }
    
    /**
     * @dev Criar nova atribuição
     */
    function createAttribution(
        address contributor,
        address beneficiary,
        uint256 contributionType,
        uint256 weight,
        uint256 revenueShareBps,
        string calldata metadata
    ) external onlyOwner returns (uint256) {
        require(contributor != address(0), "Contributor is zero address");
        require(beneficiary != address(0), "Beneficiary is zero address");
        require(weight <= MAX_WEIGHT, "Weight exceeds maximum");
        require(revenueShareBps <= MAX_REVENUE_SHARE, "Revenue share exceeds maximum");
        
        attributionCount++;
        
        attributions[attributionCount] = Attribution({
            attributionId: attributionCount,
            contributor: contributor,
            beneficiary: beneficiary,
            contributionType: contributionType,
            weight: weight,
            revenueShare: revenueShareBps,
            timestamp: block.timestamp,
            metadata: metadata,
            isActive: true
        });
        
        agentAttributions[contributor].push(attributionCount);
        contributorBeneficiary[contributor][beneficiary] = attributionCount;
        
        emit AttributionCreated(
            attributionCount,
            contributor,
            beneficiary,
            contributionType,
            weight,
            revenueShareBps
        );
        
        return attributionCount;
    }
    
    /**
     * @dev Atualizar atribuição existente
     */
    function updateAttribution(
        uint256 attributionId,
        uint256 newWeight,
        uint256 newRevenueShareBps
    ) external onlyOwner {
        require(attributionId <= attributionCount, "Attribution does not exist");
        require(attributions[attributionId].isActive, "Attribution is inactive");
        require(newWeight <= MAX_WEIGHT, "Weight exceeds maximum");
        require(newRevenueShareBps <= MAX_REVENUE_SHARE, "Revenue share exceeds maximum");
        
        Attribution storage attr = attributions[attributionId];
        attr.weight = newWeight;
        attr.revenueShare = newRevenueShareBps;
        
        emit AttributionUpdated(attributionId, newWeight, newRevenueShareBps);
    }
    
    /**
     * @dev Distribuir revenue para agentes
     */
    function distributeRevenue(address agent, uint256 amount) external onlyOwner {
        require(agent != address(0), "Agent is zero address");
        
        RevenueShare storage share = revenueShares[agent];
        share.agent = agent;
        share.totalRevenue += amount;
        totalRevenueDistributed += amount;
        
        emit RevenueDistributed(agent, amount);
    }
    
    /**
     * @dev Agente claimar revenue
     */
    function claimRevenue(address agent, address tokenAddress) external {
        RevenueShare storage share = revenueShares[agent];
        require(share.totalRevenue > share.claimedRevenue, "No revenue to claim");
        
        uint256 claimable = share.totalRevenue - share.claimedRevenue;
        uint256 platformFee = (claimable * platformFeeBps) / 10000;
        uint256 agentAmount = claimable - platformFee;
        
        share.claimedRevenue = claimable;
        
        // Transferir tokens (implementação simplificada)
        // Na prática, precisaria de IERC20(tokenAddress).transfer(agent, agentAmount);
        
        emit RevenueClaimed(agent, agentAmount);
    }
    
    /**
     * @dev Desativar atribuição
     */
    function deactivateAttribution(uint256 attributionId) external onlyOwner {
        require(attributionId <= attributionCount, "Attribution does not exist");
        
        attributions[attributionId].isActive = false;
        
        emit AttributionDeactivated(attributionId);
    }
    
    /**
     * @dev Obter detalhes de atribuição
     */
    function getAttribution(uint256 attributionId) external view returns (Attribution memory) {
        require(attributionId <= attributionCount, "Attribution does not exist");
        return attributions[attributionId];
    }
    
    /**
     * @dev Obter revenue share de um agente
     */
    function getRevenueShare(address agent) external view returns (
        uint256 totalRevenue,
        uint256 claimedRevenue,
        uint256 claimable
    ) {
        RevenueShare memory share = revenueShares[agent];
        claimable = share.totalRevenue - share.claimedRevenue;
        
        return (share.totalRevenue, share.claimedRevenue, claimable);
    }
    
    /**
     * @dev Obter todas atribuições de um agente
     */
    function getAgentAttributions(address agent) external view returns (uint256[] memory) {
        return agentAttributions[agent];
    }
    
    /**
     * @dev Obter atribuição entre contributor e beneficiary
     */
    function getAttributionBetween(address contributor, address beneficiary) external view returns (uint256) {
        return contributorBeneficiary[contributor][beneficiary];
    }
    
    /**
     * @dev Atualizar platform fee
     */
    function setPlatformFeeBps(uint256 newFeeBps) external onlyOwner {
        require(newFeeBps <= 1000, "Fee exceeds maximum (10%)"); // Max 10%
        platformFeeBps = newFeeBps;
    }
}
