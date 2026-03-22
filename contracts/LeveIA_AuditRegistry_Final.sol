// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract LeveIA_AuditRegistry {
    address public owner;
    bool public paused;

    struct AuditLog {
        uint256 timestamp;
        string modelId;
        bytes32 inputHash;
        string output;
        bytes32 proof;
        bytes32 circleAttestation;
        address validator;
    }

    mapping(uint256 => AuditLog) public auditLogs;
    uint256 public nextLogId;

    event PredictionLogged(uint256 indexed logId, string modelId, string output, bytes32 circleAttestation);

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Nao e o dono");
        _;
    }

    modifier whenNotPaused() {
        require(!paused, "Contrato pausado");
        _;
    }

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
        emit PredictionLogged(nextLogId, _modelId, _output, _circleAttestation);
        nextLogId++;
    }

    function setPaused(bool _paused) external onlyOwner {
        paused = _paused;
    }

    function transferOwnership(address _newOwner) external onlyOwner {
        owner = _newOwner;
    }
}