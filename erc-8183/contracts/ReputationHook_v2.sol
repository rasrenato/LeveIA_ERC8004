// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./IACPHook.sol";
import "./ERC8183.sol";

/**
 * @title ReputationHook v2 - Hook para integração com ERC-8004 (Reputação)
 * @dev Agora INTEGRADO com LeveIA_AuditRegistry para emitir attestations on-chain
 * 
 * Melhorias na v2:
 * - Integração com AuditRegistry (ERC-8004)
 * - Emite eventos de reputação quando jobs são completados/rejeitados
 * - Compatível com Agent0 SDK
 */
contract ReputationHook_v2 is BaseACPHook {
    // Eventos de reputação
    event ReputationSignal(
        uint256 indexed jobId,
        address indexed agent,
        string signalType,
        bytes32 reason
    );
    
    event AuditLogCreated(
        uint256 indexed logId,
        uint256 indexed jobId,
        address indexed agent,
        string signalType
    );
    
    // Configurações
    address public erc8004Registry;  // LeveIA_AuditRegistry
    address public erc8183;          // ERC-8183 Commercial Layer
    mapping(address => bool) public authorizedCallers;
    
    constructor(address _erc8004Registry, address _erc8183) {
        require(_erc8004Registry != address(0), "Registry cannot be zero");
        require(_erc8183 != address(0), "ERC8183 cannot be zero");
        
        erc8004Registry = _erc8004Registry;
        erc8183 = _erc8183;
        authorizedCallers[msg.sender] = true;
    }
    
    /**
     * @dev Após completar job - sinal POSITIVO para provider
     */
    function _postComplete(
        uint256 jobId,
        bytes32 reason,
        bytes memory
    ) internal override {
        ERC8183 acp = ERC8183(msg.sender);
        ERC8183.Job memory job = acp.getJob(jobId);
        
        // Sinal positivo para provider
        emit ReputationSignal(
            jobId,
            job.provider,
            "JOB_COMPLETED_POSITIVE",
            reason
        );
        
        // Sinal neutro/positivo para evaluator
        emit ReputationSignal(
            jobId,
            job.evaluator,
            "EVALUATION_COMPLETED",
            reason
        );
        
        // NOVO NA V2: Chamar AuditRegistry para logar on-chain
        if (erc8004Registry != address(0)) {
            try IERC8004(erc8004Registry).emitAttestation({
                agent: job.provider,
                signalType: "JOB_COMPLETED",
                data: abi.encode(jobId, reason)
            }) {
                emit AuditLogCreated(
                    block.number, // Usar block.number como logId temporário
                    jobId,
                    job.provider,
                    "JOB_COMPLETED"
                );
            } catch {
                // Se falhar, continua mas emite warning
                emit ReputationSignal(
                    jobId,
                    job.provider,
                    "AUDIT_LOG_FAILED",
                    reason
                );
            }
        }
    }
    
    /**
     * @dev Após rejeitar job - sinal NEGATIVO para provider
     */
    function _postReject(
        uint256 jobId,
        bytes32 reason,
        bytes memory
    ) internal override {
        ERC8183 acp = ERC8183(msg.sender);
        ERC8183.Job memory job = acp.getJob(jobId);
        
        // Sinal negativo para provider
        emit ReputationSignal(
            jobId,
            job.provider,
            "JOB_REJECTED_NEGATIVE",
            reason
        );
        
        // Sinal para evaluator
        emit ReputationSignal(
            jobId,
            job.evaluator,
            "EVALUATION_REJECTED",
            reason
        );
        
        // NOVO NA V2: Logar rejection no AuditRegistry
        if (erc8004Registry != address(0)) {
            try IERC8004(erc8004Registry).emitAttestation({
                agent: job.provider,
                signalType: "JOB_REJECTED",
                data: abi.encode(jobId, reason)
            }) {
                emit AuditLogCreated(
                    block.number,
                    jobId,
                    job.provider,
                    "JOB_REJECTED"
                );
            } catch {
                // Ignora erro, mas emite evento
            }
        }
    }
    
    /**
     * @dev Após submeter trabalho
     */
    function _postSubmit(
        uint256 jobId,
        bytes32 deliverable,
        bytes memory
    ) internal override {
        ERC8183 acp = ERC8183(msg.sender);
        ERC8183.Job memory job = acp.getJob(jobId);
        
        emit ReputationSignal(
            jobId,
            job.provider,
            "WORK_SUBMITTED",
            deliverable
        );
    }
    
    /**
     * @dev Atualizar endereço do registry (apenas owner)
     */
    function updateRegistry(address _newRegistry) external {
        require(authorizedCallers[msg.sender], "Not authorized");
        require(_newRegistry != address(0), "Registry cannot be zero");
        
        address oldRegistry = erc8004Registry;
        erc8004Registry = _newRegistry;
        
        emit ReputationSignal(
            0,
            msg.sender,
            "REGISTRY_UPDATED",
            bytes32(uint256(uint160(_newRegistry)))
        );
    }
}

/**
 * @dev Interface mínima do ERC-8004 para attestations
 */
interface IERC8004 {
    function emitAttestation(
        address agent,
        string memory signalType,
        bytes memory data
    ) external returns (uint256);
}
