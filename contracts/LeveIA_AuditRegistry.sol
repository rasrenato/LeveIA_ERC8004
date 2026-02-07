// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Pausable.sol";
import "@openzeppelin/contracts/utils/cryptography/ECDSA.sol";

/**
 * @title LeveIA_AuditRegistry
 * @dev Implementation of ERC-8004 for Trustless AI Agent logging with Agent0 SDK compatibility.
 * This contract records market predictions from Leve IA for transparency and provides
 * attestations for 10TB data processing proofs compatible with Circle Protocol.
 */
contract LeveIA_AuditRegistry is Ownable, Pausable {
    using ECDSA for bytes32;
    
    struct AuditLog {
        uint256 timestamp;
        string modelId;
        bytes32 inputHash;           // Hash of the 10TB data slice processed
        string output;              // Prediction summary (e.g., "BTC_LONG_78K")
        bytes32 proof;              // Cryptographic proof/attestation
        bytes32 circleAttestation;  // Circle Protocol attestation for data processing
        address validator;          // Address that validated the attestation
    }

    struct AgentRegistration {
        address agentAddress;
        string agentId;
        string capabilities;
        uint256 registrationTime;
        bool isActive;
        bytes32 attestationRoot;    // Merkle root for batch attestations
    }

    // Mapping from Log ID to AuditLog
    mapping(uint256 => AuditLog) public auditLogs;
    
    // Mapping from agent address to registration
    mapping(address => AgentRegistration) public agentRegistrations;
    
    // Mapping from agent ID to address
    mapping(string => address) public agentIdToAddress;
    
    // Merkle roots for batch attestations (for Circle Protocol compatibility)
    mapping(uint256 => bytes32) public attestationRoots;
    
    uint256 public nextLogId;
    uint256 public nextAttestationBatchId;
    
    // Agent0 SDK Compatible Events
    event PredictionLogged(
        uint256 indexed logId,
        string modelId,
        string output,
        bytes32 inputHash,
        bytes32 proof,
        bytes32 circleAttestation
    );
    
    event AgentRegistered(
        address indexed agentAddress,
        string agentId,
        string capabilities,
        uint256 registrationTime,
        bytes32 attestationRoot
    );
    
    event AttestationBatchCreated(
        uint256 indexed batchId,
        bytes32 root,
        uint256 timestamp,
        uint256 dataVolumeTB  // 10TB per batch
    );
    
    event ValidationAttested(
        uint256 indexed logId,
        address validator,
        bytes32 attestationHash,
        uint256 timestamp
    );

    constructor() Ownable(msg.sender) {}

    /**
     * @dev Register an AI agent with Agent0 SDK compatibility
     * @param _agentId Unique identifier for the agent
     * @param _capabilities JSON string describing agent capabilities
     * @param _initialAttestationRoot Merkle root for initial attestations
     */
    function registerAgent(
        string memory _agentId,
        string memory _capabilities,
        bytes32 _initialAttestationRoot
    ) external whenNotPaused {
        require(bytes(_agentId).length > 0, "Agent ID cannot be empty");
        require(agentIdToAddress[_agentId] == address(0), "Agent ID already registered");
        
        agentRegistrations[msg.sender] = AgentRegistration({
            agentAddress: msg.sender,
            agentId: _agentId,
            capabilities: _capabilities,
            registrationTime: block.timestamp,
            isActive: true,
            attestationRoot: _initialAttestationRoot
        });
        
        agentIdToAddress[_agentId] = msg.sender;
        
        emit AgentRegistered(
            msg.sender,
            _agentId,
            _capabilities,
            block.timestamp,
            _initialAttestationRoot
        );
    }

    /**
     * @dev Logs a new AI prediction with Circle Protocol attestation
     * @param _modelId Identifier for the AI model (e.g., "Gemini-3-LeveV2")
     * @param _inputHash Keccak256 hash of the 10TB input data
     * @param _output Textual result of the prediction
     * @param _proof ZK proof or cryptographic attestation
     * @param _circleAttestation Circle Protocol attestation for data processing
     */
    function logPrediction(
        string memory _modelId,
        bytes32 _inputHash,
        string memory _output,
        bytes32 _proof,
        bytes32 _circleAttestation
    ) external onlyOwner whenNotPaused {
        auditLogs[nextLogId] = AuditLog({
            timestamp: block.timestamp,
            modelId: _modelId,
            inputHash: _inputHash,
            output: _output,
            proof: _proof,
            circleAttestation: _circleAttestation,
            validator: msg.sender
        });

        emit PredictionLogged(
            nextLogId,
            _modelId,
            _output,
            _inputHash,
            _proof,
            _circleAttestation
        );
        
        nextLogId++;
    }

    /**
     * @dev Create a batch attestation root for Circle Protocol compatibility
     * @param _root Merkle root of batch attestations
     * @param _dataVolumeTB Volume of data processed in TB (typically 10)
     */
    function createAttestationBatch(
        bytes32 _root,
        uint256 _dataVolumeTB
    ) external onlyOwner whenNotPaused {
        attestationRoots[nextAttestationBatchId] = _root;
        
        emit AttestationBatchCreated(
            nextAttestationBatchId,
            _root,
            block.timestamp,
            _dataVolumeTB
        );
        
        nextAttestationBatchId++;
    }

    /**
     * @dev Attest a validation for a specific log entry
     * @param _logId ID of the log to validate
     * @param _attestationHash Hash of the validation attestation
     */
    function attestValidation(
        uint256 _logId,
        bytes32 _attestationHash
    ) external whenNotPaused {
        require(_logId < nextLogId, "Invalid log ID");
        require(auditLogs[_logId].validator == address(0), "Already validated");
        
        auditLogs[_logId].validator = msg.sender;
        
        emit ValidationAttested(
            _logId,
            msg.sender,
            _attestationHash,
            block.timestamp
        );
    }

    /**
     * @dev Get agent registration details
     */
    function getAgentRegistration(address _agent) 
        external 
        view 
        returns (AgentRegistration memory) 
    {
        return agentRegistrations[_agent];
    }

    /**
     * @dev Get audit log with full details
     */
    function getAuditLog(uint256 _logId) 
        external 
        view 
        returns (AuditLog memory) 
    {
        return auditLogs[_logId];
    }

    /**
     * @dev Get batch attestation root
     */
    function getAttestationBatch(uint256 _batchId) 
        external 
        view 
        returns (bytes32) 
    {
        return attestationRoots[_batchId];
    }

    /**
     * @dev Verify Merkle proof for attestation inclusion
     * @param _batchId Batch ID containing the attestation
     * @param _leafHash Hash of the attestation leaf
     * @param _proof Merkle proof
     */
    function verifyAttestationInclusion(
        uint256 _batchId,
        bytes32 _leafHash,
        bytes32[] memory _proof
    ) external view returns (bool) {
        bytes32 root = attestationRoots[_batchId];
        require(root != bytes32(0), "Batch does not exist");
        
        bytes32 computedHash = _leafHash;
        for (uint256 i = 0; i < _proof.length; i++) {
            if (computedHash <= _proof[i]) {
                computedHash = keccak256(abi.encodePacked(computedHash, _proof[i]));
            } else {
                computedHash = keccak256(abi.encodePacked(_proof[i], computedHash));
            }
        }
        
        return computedHash == root;
    }

    /**
     * @dev Deactivate an agent registration
     */
    function deactivateAgent(address _agent) external onlyOwner {
        require(agentRegistrations[_agent].isActive, "Agent already inactive");
        agentRegistrations[_agent].isActive = false;
    }

    /**
     * @dev Reactivate an agent registration
     */
    function reactivateAgent(address _agent) external onlyOwner {
        require(!agentRegistrations[_agent].isActive, "Agent already active");
        agentRegistrations[_agent].isActive = true;
    }

    function pause() external onlyOwner {
        _pause();
    }

    function unpause() external onlyOwner {
        _unpause();
    }

    /**
     * @dev Get total number of audit logs
     */
    function totalAuditLogs() external view returns (uint256) {
        return nextLogId;
    }

    /**
     * @dev Get total number of attestation batches
     */
    function totalAttestationBatches() external view returns (uint256) {
        return nextAttestationBatchId;
    }
}
