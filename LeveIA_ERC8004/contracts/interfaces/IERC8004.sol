// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title IERC8004 - ERC-8004 Trustless Agents Interface
 * @dev Interface for ERC-8004 compliant AI agent registries
 * @notice Based on EIP-8004 specification for trustless AI agents
 */
interface IERC8004 {
    
    // ============ EVENTS ============
    
    /**
     * @dev Emitted when a new agent is registered
     */
    event AgentRegistered(
        uint256 indexed agentId,
        address indexed owner,
        string agentName,
        string[] endpoints,
        string[] supportedTrustModels
    );
    
    /**
     * @dev Emitted when agent metadata is updated
     */
    event MetadataSet(
        uint256 indexed agentId,
        string indexed indexedMetadataKey,
        string metadataKey,
        bytes metadataValue
    );
    
    /**
     * @dev Emitted when agent wallet is set
     */
    event AgentWalletSet(
        uint256 indexed agentId,
        address indexed oldWallet,
        address indexed newWallet
    );
    
    // ============ STRUCTS ============
    
    struct AgentInfo {
        uint256 agentId;
        address owner;
        string agentURI;
        bool active;
        uint256 reputationScore;
        uint256 totalInteractions;
        uint256 successfulValidations;
    }
    
    struct ValidationRequest {
        uint256 requestId;
        uint256 agentId;
        address requester;
        bytes inputData;
        string validationType;
        uint256 stakeAmount;
        uint256 deadline;
        bool fulfilled;
    }
    
    // ============ FUNCTIONS ============
    
    /**
     * @dev Register a new AI agent
     * @param agentName Name of the AI agent
     * @param agentDescription Description of capabilities
     * @param endpoints Array of service endpoints
     * @param supportedTrustModels Array of supported trust models
     * @param registrationURI URI for agent registration file
     * @return agentId The registered agent ID
     */
    function registerAgent(
        string memory agentName,
        string memory agentDescription,
        string[] memory endpoints,
        string[] memory supportedTrustModels,
        string memory registrationURI
    ) external returns (uint256);
    
    /**
     * @dev Get agent information
     * @param agentId The agent ID
     * @return AgentInfo struct with agent details
     */
    function getAgentInfo(uint256 agentId) external view returns (AgentInfo memory);
    
    /**
     * @dev Set agent metadata
     * @param agentId The agent ID
     * @param metadataKey Key for metadata
     * @param metadataValue Value for metadata
     */
    function setMetadata(
        uint256 agentId,
        string memory metadataKey,
        bytes memory metadataValue
    ) external;
    
    /**
     * @dev Get agent metadata
     * @param agentId The agent ID
     * @param metadataKey Key for metadata
     * @return metadataValue The metadata value
     */
    function getMetadata(
        uint256 agentId,
        string memory metadataKey
    ) external view returns (bytes memory);
    
    /**
     * @dev Set agent wallet for payments
     * @param agentId The agent ID
     * @param newWallet New wallet address
     * @param deadline Signature deadline
     * @param signature EIP-712 signature proving wallet control
     */
    function setAgentWallet(
        uint256 agentId,
        address newWallet,
        uint256 deadline,
        bytes calldata signature
    ) external;
    
    /**
     * @dev Get agent wallet
     * @param agentId The agent ID
     * @return walletAddress The agent's wallet address
     */
    function getAgentWallet(uint256 agentId) external view returns (address);
    
    /**
     * @dev Submit validation request
     * @param agentId The agent ID to validate
     * @param inputData Input data for validation
     * @param validationType Type of validation (zkML, TEE, stake-based, etc.)
     * @param stakeAmount Amount staked for validation
     * @return requestId The validation request ID
     */
    function submitValidationRequest(
        uint256 agentId,
        bytes memory inputData,
        string memory validationType,
        uint256 stakeAmount
    ) external payable returns (uint256);
    
    /**
     * @dev Fulfill validation request
     * @param requestId The validation request ID
     * @param validationScore 0-100 validation score
     * @param evidenceURI URI to validation evidence
     */
    function fulfillValidationRequest(
        uint256 requestId,
        uint256 validationScore,
        string memory evidenceURI
    ) external;
    
    /**
     * @dev Update agent reputation
     * @param agentId The agent ID
     * @param scoreDelta Change in reputation score
     * @param reason Reason for reputation change
     */
    function updateReputation(
        uint256 agentId,
        int256 scoreDelta,
        string memory reason
    ) external;
    
    /**
     * @dev Check if agent supports specific trust model
     * @param agentId The agent ID
     * @param trustModel Trust model to check
     * @return supported Whether the trust model is supported
     */
    function supportsTrustModel(
        uint256 agentId,
        string memory trustModel
    ) external view returns (bool);
    
    /**
     * @dev Get total registered agents
     * @return count Number of registered agents
     */
    function totalAgents() external view returns (uint256);
    
    /**
     * @dev Get agent ID by owner address
     * @param owner Agent owner address
     * @return agentId The agent ID, 0 if not found
     */
    function getAgentIdByOwner(address owner) external view returns (uint256);
}