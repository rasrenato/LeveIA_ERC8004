// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./IACPHook.sol";
import "./ERC8183.sol";

/**
 * @title ReputationHook - Hook para integração com ERC-8004 (Reputação)
 * @dev Emite eventos de reputação quando jobs são completados/rejeitados
 */
contract ReputationHook is BaseACPHook {
    // Eventos de reputação
    event ReputationSignal(
        uint256 indexed jobId,
        address indexed agent,
        string signalType,
        bytes32 reason
    );
    
    // Configurações
    address public erc8004Registry;
    mapping(address => bool) public authorizedCallers;
    
    constructor(address _erc8004Registry) {
        erc8004Registry = _erc8004Registry;
        authorizedCallers[msg.sender] = true;
    }
    
    /**
     * @dev Após completar job - sinal positivo para provider
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
        
        // Aqui poderia chamar ERC-8004 registry se implementado
        // IERC8004(erc8004Registry).emitAttestation(...)
    }
    
    /**
     * @dev Após rejeitar job - sinal negativo/neutro
     */
    function _postReject(
        uint256 jobId,
        bytes32 reason,
        bytes memory
    ) internal override {
        // Sinal para evaluator
        emit ReputationSignal(
            jobId,
            msg.sender,
            "EVALUATION_REJECTED",
            reason
        );
    }
    
    /**
     * @dev Após submeter trabalho
     */
    function _postSubmit(
        uint256 jobId,
        bytes32 deliverable,
        bytes memory
    ) internal override {
        emit ReputationSignal(
            jobId,
            ERC8183(msg.sender).getJob(jobId).provider,
            "WORK_SUBMITTED",
            deliverable
        );
    }
}
