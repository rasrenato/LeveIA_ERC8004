// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
import "./utils/EmergencyStop.sol";
import "./interfaces/IERC8004.sol";

/**
 * @title LeveIA AI Audit Log - ERC-8004 Implementation
 * @dev Smart contract for immutable AI prediction logging on Ethereum
 * @notice This contract implements ERC-8004 standard for trustless AI agents
 * with focus on BTC market predictions (10TB data processing)
 */
contract LeveIA_AIAuditLog is ERC721, ERC721URIStorage, Ownable, ReentrancyGuard, EmergencyStop, IERC8004 {
    
    // ============ STRUCTS ============
    
    struct AIAuditRecord {
        bytes32 aiModelId;          // Hash of AI model identifier (e.g., "gemini-2.0-flash-exp")
        bytes32 inputHash;          // Keccak256 hash of input data (10TB market data)
        bytes32 outputHash;         // Keccak256 hash of prediction output
        bytes32 metadataHash;       // Hash of metadata (sentiment, target price, confidence)
        uint256 timestamp;          // Block timestamp of registration
        address registeredBy;       // Address that registered the prediction
        string ipfsEvidenceCID;     // IPFS CID for off-chain evidence storage
        bool validated;             // Whether prediction has been validated
        uint256 validationScore;    // 0-100 validation score (ERC-8004 compliant)
    }
    
    struct AgentRegistration {
        uint256 agentId;
        string agentName;
        string agentDescription;
        string[] endpoints;
        string[] supportedTrustModels;
        bool active;
        uint256 reputationScore;
        uint256 totalPredictions;
        uint256 successfulValidations;
    }
    
    // ============ STATE VARIABLES ============
    
    uint256 private _nextAgentId = 1;
    uint256 private _nextRecordId = 1;
    
    // Mappings
    mapping(uint256 => AgentRegistration) public agents;
    mapping(uint256 => AIAuditRecord) public auditRecords;
    mapping(bytes32 => uint256) public inputHashToRecordId;
    mapping(address => uint256[]) public agentPredictions;
    
    // ERC-8004 Registry Addresses
    address public identityRegistry;
    address public reputationRegistry;
    address public validationRegistry;
    
    // Constants
    uint256 public constant MAX_VALIDATION_SCORE = 100;
    uint256 public constant MIN_STAKE_AMOUNT = 0.1 ether;
    
    // Events (ERC-8004 compliant + custom)
    event AgentRegistered(
        uint256 indexed agentId,
        address indexed owner,
        string agentName,
        string[] endpoints,
        string[] supportedTrustModels
    );
    
    event AIAuditLogged(
        uint256 indexed recordId,
        uint256 indexed agentId,
        bytes32 aiModelId,
        bytes32 inputHash,
        bytes32 outputHash,
        bytes32 metadataHash,
        string ipfsEvidenceCID,
        address indexed registeredBy
    );
    
    event PredictionValidated(
        uint256 indexed recordId,
        uint256 indexed agentId,
        uint256 validationScore,
        address validator,
        string validationMethod
    );
    
    event EmergencyStopActivated(address indexed by, string reason);
    event EmergencyStopDeactivated(address indexed by);
    
    // ============ MODIFIERS ============
    
    modifier onlyAgentOwner(uint256 agentId) {
        require(ownerOf(agentId) == msg.sender, "Not agent owner");
        _;
    }
    
    modifier onlyActiveAgent(uint256 agentId) {
        require(agents[agentId].active, "Agent inactive");
        _;
    }
    
    modifier notStopped() {
        require(!stopped(), "Contract stopped");
        _;
    }
    
    // ============ CONSTRUCTOR ============
    
    constructor(
        address initialOwner,
        address _identityRegistry,
        address _reputationRegistry,
        address _validationRegistry
    ) 
        ERC721("LeveIA AI Agent", "LEVEIA") 
        Ownable(initialOwner)
    {
        identityRegistry = _identityRegistry;
        reputationRegistry = _reputationRegistry;
        validationRegistry = _validationRegistry;
    }
    
    // ============ ERC-8004 IMPLEMENTATION ============
    
    /**
     * @dev Register a new AI agent following ERC-8004 standard
     * @param agentName Name of the AI agent
     * @param agentDescription Description of capabilities
     * @param endpoints Array of service endpoints (A2A, MCP, etc.)
     * @param supportedTrustModels Array of supported trust models
     * @param registrationURI IPFS/HTTPS URI for agent registration file
     */
    function registerAgent(
        string memory agentName,
        string memory agentDescription,
        string[] memory endpoints,
        string[] memory supportedTrustModels,
        string memory registrationURI
    ) 
        external 
        notStopped 
        nonReentrant 
        returns (uint256)
    {
        uint256 agentId = _nextAgentId++;
        
        // Mint ERC-721 token for agent identity
        _safeMint(msg.sender, agentId);
        _setTokenURI(agentId, registrationURI);
        
        // Store agent registration data
        agents[agentId] = AgentRegistration({
            agentId: agentId,
            agentName: agentName,
            agentDescription: agentDescription,
            endpoints: endpoints,
            supportedTrustModels: supportedTrustModels,
            active: true,
            reputationScore: 0,
            totalPredictions: 0,
            successfulValidations: 0
        });
        
        emit AgentRegistered(
            agentId,
            msg.sender,
            agentName,
            endpoints,
            supportedTrustModels
        );
        
        return agentId;
    }
    
    /**
     * @dev Log AI prediction audit record
     * @param agentId ERC-8004 agent identifier
     * @param aiModelId Hash of AI model identifier
     * @param inputHash Keccak256 hash of input data (10TB market data)
     * @param outputHash Keccak256 hash of prediction output
     * @param metadataHash Hash of metadata (sentiment, target price, confidence)
     * @param ipfsEvidenceCID IPFS CID for off-chain evidence
     */
    function logPrediction(
        uint256 agentId,
        bytes32 aiModelId,
        bytes32 inputHash,
        bytes32 outputHash,
        bytes32 metadataHash,
        string memory ipfsEvidenceCID
    ) 
        external 
        onlyAgentOwner(agentId)
        onlyActiveAgent(agentId)
        notStopped
        nonReentrant
        returns (uint256)
    {
        // Prevent duplicate input hash registration
        require(inputHashToRecordId[inputHash] == 0, "Input already registered");
        
        uint256 recordId = _nextRecordId++;
        
        auditRecords[recordId] = AIAuditRecord({
            aiModelId: aiModelId,
            inputHash: inputHash,
            outputHash: outputHash,
            metadataHash: metadataHash,
            timestamp: block.timestamp,
            registeredBy: msg.sender,
            ipfsEvidenceCID: ipfsEvidenceCID,
            validated: false,
            validationScore: 0
        });
        
        inputHashToRecordId[inputHash] = recordId;
        agentPredictions[msg.sender].push(recordId);
        agents[agentId].totalPredictions++;
        
        emit AIAuditLogged(
            recordId,
            agentId,
            aiModelId,
            inputHash,
            outputHash,
            metadataHash,
            ipfsEvidenceCID,
            msg.sender
        );
        
        return recordId;
    }
    
    /**
     * @dev Validate a prediction using ERC-8004 validation mechanisms
     * @param recordId Audit record identifier
     * @param validationScore 0-100 validation score
     * @param validationMethod Method used for validation (zkML, TEE, stake-based, etc.)
     * @param validationEvidenceURI URI to validation evidence
     */
    function validatePrediction(
        uint256 recordId,
        uint256 validationScore,
        string memory validationMethod,
        string memory validationEvidenceURI
    ) 
        external 
        notStopped 
        nonReentrant
    {
        require(recordId < _nextRecordId, "Invalid record ID");
        require(!auditRecords[recordId].validated, "Already validated");
        require(validationScore <= MAX_VALIDATION_SCORE, "Invalid score");
        
        // Update record
        auditRecords[recordId].validated = true;
        auditRecords[recordId].validationScore = validationScore;
        
        // Find agent ID from registeredBy address
        address predictor = auditRecords[recordId].registeredBy;
        
        // Update agent reputation (simplified - in production use more sophisticated algorithm)
        for (uint256 i = 1; i < _nextAgentId; i++) {
            if (ownerOf(i) == predictor && agents[i].active) {
                if (validationScore >= 80) {
                    agents[i].successfulValidations++;
                }
                agents[i].reputationScore = (agents[i].reputationScore * 9 + validationScore) / 10;
                break;
            }
        }
        
        emit PredictionValidated(
            recordId,
            // Agent ID would be passed or derived in production
            0, // Placeholder - would be actual agentId
            validationScore,
            msg.sender,
            validationMethod
        );
    }
    
    // ============ EMERGENCY STOP FUNCTIONS ============
    
    /**
     * @dev Activate emergency stop with reason
     * @param reason Reason for emergency stop
     */
    function activateEmergencyStop(string memory reason) external onlyOwner {
        _activateStop();
        emit EmergencyStopActivated(msg.sender, reason);
    }
    
    /**
     * @dev Deactivate emergency stop
     */
    function deactivateEmergencyStop() external onlyOwner {
        _deactivateStop();
        emit EmergencyStopDeactivated(msg.sender);
    }
    
    // ============ VIEW FUNCTIONS ============
    
    /**
     * @dev Get audit record by ID
     */
    function getAuditRecord(uint256 recordId) 
        external 
        view 
        returns (AIAuditRecord memory) 
    {
        require(recordId < _nextRecordId, "Invalid record ID");
        return auditRecords[recordId];
    }
    
    /**
     * @dev Get agent registration data
     */
    function getAgentRegistration(uint256 agentId) 
        external 
        view 
        returns (AgentRegistration memory) 
    {
        require(agentId < _nextAgentId, "Invalid agent ID");
        return agents[agentId];
    }
    
    /**
     * @dev Get predictions by agent owner
     */
    function getAgentPredictions(address agentOwner) 
        external 
        view 
        returns (uint256[] memory) 
    {
        return agentPredictions[agentOwner];
    }
    
    /**
     * @dev Check if input hash is already registered
     */
    function isInputRegistered(bytes32 inputHash) external view returns (bool) {
        return inputHashToRecordId[inputHash] != 0;
    }
    
    /**
     * @dev Get total predictions count
     */
    function totalPredictions() external view returns (uint256) {
        return _nextRecordId - 1;
    }
    
    /**
     * @dev Get total agents count
     */
    function totalAgents() external view returns (uint256) {
        return _nextAgentId - 1;
    }
    
    // ============ AGENT MANAGEMENT ============
    
    /**
     * @dev Update agent status
     */
    function setAgentStatus(uint256 agentId, bool active) 
        external 
        onlyAgentOwner(agentId)
        notStopped
    {
        agents[agentId].active = active;
    }
    
    /**
     * @dev Update agent endpoints
     */
    function updateAgentEndpoints(
        uint256 agentId, 
        string[] memory newEndpoints
    ) 
        external 
        onlyAgentOwner(agentId)
        notStopped
    {
        agents[agentId].endpoints = newEndpoints;
    }
    
    // ============ OVERRIDES ============
    
    function _update(
        address to,
        uint256 tokenId,
        address auth
    ) internal override(ERC721) returns (address) {
        require(!stopped(), "Contract stopped");
        return super._update(to, tokenId, auth);
    }
    
    function tokenURI(uint256 tokenId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (string memory)
    {
        return super.tokenURI(tokenId);
    }
    
    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (bool)
    {
        return 
            interfaceId == type(IERC8004).interfaceId ||
            super.supportsInterface(interfaceId);
    }
}