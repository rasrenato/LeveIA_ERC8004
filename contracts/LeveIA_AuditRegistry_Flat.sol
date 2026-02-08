// Sources flattened with hardhat v2.28.4 https://hardhat.org

// SPDX-License-Identifier: MIT

// File @openzeppelin/contracts/utils/Context.sol@v5.4.0

// Original license: SPDX_License_Identifier: MIT
// OpenZeppelin Contracts (last updated v5.0.1) (utils/Context.sol)

pragma solidity ^0.8.20;

/**
 * @dev Provides information about the current execution context, including the
 * sender of the transaction and its data. While these are generally available
 * via msg.sender and msg.data, they should not be accessed in such a direct
 * manner, since when dealing with meta-transactions the account sending and
 * paying for execution may not be the actual sender (as far as an application
 * is concerned).
 *
 * This contract is only required for intermediate, library-like contracts.
 */
abstract contract Context {
    function _msgSender() internal view virtual returns (address) {
        return msg.sender;
    }

    function _msgData() internal view virtual returns (bytes calldata) {
        return msg.data;
    }

    function _contextSuffixLength() internal view virtual returns (uint256) {
        return 0;
    }
}


// File @openzeppelin/contracts/access/Ownable.sol@v5.4.0

// Original license: SPDX_License_Identifier: MIT
// OpenZeppelin Contracts (last updated v5.0.0) (access/Ownable.sol)

pragma solidity ^0.8.20;

/**
 * @dev Contract module which provides a basic access control mechanism, where
 * there is an account (an owner) that can be granted exclusive access to
 * specific functions.
 *
 * The initial owner is set to the address provided by the deployer. This can
 * later be changed with {transferOwnership}.
 *
 * This module is used through inheritance. It will make available the modifier
 * `onlyOwner`, which can be applied to your functions to restrict their use to
 * the owner.
 */
abstract contract Ownable is Context {
    address private _owner;

    /**
     * @dev The caller account is not authorized to perform an operation.
     */
    error OwnableUnauthorizedAccount(address account);

    /**
     * @dev The owner is not a valid owner account. (eg. `address(0)`)
     */
    error OwnableInvalidOwner(address owner);

    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);

    /**
     * @dev Initializes the contract setting the address provided by the deployer as the initial owner.
     */
    constructor(address initialOwner) {
        if (initialOwner == address(0)) {
            revert OwnableInvalidOwner(address(0));
        }
        _transferOwnership(initialOwner);
    }

    /**
     * @dev Throws if called by any account other than the owner.
     */
    modifier onlyOwner() {
        _checkOwner();
        _;
    }

    /**
     * @dev Returns the address of the current owner.
     */
    function owner() public view virtual returns (address) {
        return _owner;
    }

    /**
     * @dev Throws if the sender is not the owner.
     */
    function _checkOwner() internal view virtual {
        if (owner() != _msgSender()) {
            revert OwnableUnauthorizedAccount(_msgSender());
        }
    }

    /**
     * @dev Leaves the contract without owner. It will not be possible to call
     * `onlyOwner` functions. Can only be called by the current owner.
     *
     * NOTE: Renouncing ownership will leave the contract without an owner,
     * thereby disabling any functionality that is only available to the owner.
     */
    function renounceOwnership() public virtual onlyOwner {
        _transferOwnership(address(0));
    }

    /**
     * @dev Transfers ownership of the contract to a new account (`newOwner`).
     * Can only be called by the current owner.
     */
    function transferOwnership(address newOwner) public virtual onlyOwner {
        if (newOwner == address(0)) {
            revert OwnableInvalidOwner(address(0));
        }
        _transferOwnership(newOwner);
    }

    /**
     * @dev Transfers ownership of the contract to a new account (`newOwner`).
     * Internal function without access restriction.
     */
    function _transferOwnership(address newOwner) internal virtual {
        address oldOwner = _owner;
        _owner = newOwner;
        emit OwnershipTransferred(oldOwner, newOwner);
    }
}


// File @openzeppelin/contracts/utils/Pausable.sol@v5.4.0

// Original license: SPDX_License_Identifier: MIT
// OpenZeppelin Contracts (last updated v5.3.0) (utils/Pausable.sol)

pragma solidity ^0.8.20;

/**
 * @dev Contract module which allows children to implement an emergency stop
 * mechanism that can be triggered by an authorized account.
 *
 * This module is used through inheritance. It will make available the
 * modifiers `whenNotPaused` and `whenPaused`, which can be applied to
 * the functions of your contract. Note that they will not be pausable by
 * simply including this module, only once the modifiers are put in place.
 */
abstract contract Pausable is Context {
    bool private _paused;

    /**
     * @dev Emitted when the pause is triggered by `account`.
     */
    event Paused(address account);

    /**
     * @dev Emitted when the pause is lifted by `account`.
     */
    event Unpaused(address account);

    /**
     * @dev The operation failed because the contract is paused.
     */
    error EnforcedPause();

    /**
     * @dev The operation failed because the contract is not paused.
     */
    error ExpectedPause();

    /**
     * @dev Modifier to make a function callable only when the contract is not paused.
     *
     * Requirements:
     *
     * - The contract must not be paused.
     */
    modifier whenNotPaused() {
        _requireNotPaused();
        _;
    }

    /**
     * @dev Modifier to make a function callable only when the contract is paused.
     *
     * Requirements:
     *
     * - The contract must be paused.
     */
    modifier whenPaused() {
        _requirePaused();
        _;
    }

    /**
     * @dev Returns true if the contract is paused, and false otherwise.
     */
    function paused() public view virtual returns (bool) {
        return _paused;
    }

    /**
     * @dev Throws if the contract is paused.
     */
    function _requireNotPaused() internal view virtual {
        if (paused()) {
            revert EnforcedPause();
        }
    }

    /**
     * @dev Throws if the contract is not paused.
     */
    function _requirePaused() internal view virtual {
        if (!paused()) {
            revert ExpectedPause();
        }
    }

    /**
     * @dev Triggers stopped state.
     *
     * Requirements:
     *
     * - The contract must not be paused.
     */
    function _pause() internal virtual whenNotPaused {
        _paused = true;
        emit Paused(_msgSender());
    }

    /**
     * @dev Returns to normal state.
     *
     * Requirements:
     *
     * - The contract must be paused.
     */
    function _unpause() internal virtual whenPaused {
        _paused = false;
        emit Unpaused(_msgSender());
    }
}


// File @openzeppelin/contracts/utils/cryptography/ECDSA.sol@v5.4.0

// Original license: SPDX_License_Identifier: MIT
// OpenZeppelin Contracts (last updated v5.1.0) (utils/cryptography/ECDSA.sol)

pragma solidity ^0.8.20;

/**
 * @dev Elliptic Curve Digital Signature Algorithm (ECDSA) operations.
 *
 * These functions can be used to verify that a message was signed by the holder
 * of the private keys of a given address.
 */
library ECDSA {
    enum RecoverError {
        NoError,
        InvalidSignature,
        InvalidSignatureLength,
        InvalidSignatureS
    }

    /**
     * @dev The signature derives the `address(0)`.
     */
    error ECDSAInvalidSignature();

    /**
     * @dev The signature has an invalid length.
     */
    error ECDSAInvalidSignatureLength(uint256 length);

    /**
     * @dev The signature has an S value that is in the upper half order.
     */
    error ECDSAInvalidSignatureS(bytes32 s);

    /**
     * @dev Returns the address that signed a hashed message (`hash`) with `signature` or an error. This will not
     * return address(0) without also returning an error description. Errors are documented using an enum (error type)
     * and a bytes32 providing additional information about the error.
     *
     * If no error is returned, then the address can be used for verification purposes.
     *
     * The `ecrecover` EVM precompile allows for malleable (non-unique) signatures:
     * this function rejects them by requiring the `s` value to be in the lower
     * half order, and the `v` value to be either 27 or 28.
     *
     * IMPORTANT: `hash` _must_ be the result of a hash operation for the
     * verification to be secure: it is possible to craft signatures that
     * recover to arbitrary addresses for non-hashed data. A safe way to ensure
     * this is by receiving a hash of the original message (which may otherwise
     * be too long), and then calling {MessageHashUtils-toEthSignedMessageHash} on it.
     *
     * Documentation for signature generation:
     * - with https://web3js.readthedocs.io/en/v1.3.4/web3-eth-accounts.html#sign[Web3.js]
     * - with https://docs.ethers.io/v5/api/signer/#Signer-signMessage[ethers]
     */
    function tryRecover(
        bytes32 hash,
        bytes memory signature
    ) internal pure returns (address recovered, RecoverError err, bytes32 errArg) {
        if (signature.length == 65) {
            bytes32 r;
            bytes32 s;
            uint8 v;
            // ecrecover takes the signature parameters, and the only way to get them
            // currently is to use assembly.
            assembly ("memory-safe") {
                r := mload(add(signature, 0x20))
                s := mload(add(signature, 0x40))
                v := byte(0, mload(add(signature, 0x60)))
            }
            return tryRecover(hash, v, r, s);
        } else {
            return (address(0), RecoverError.InvalidSignatureLength, bytes32(signature.length));
        }
    }

    /**
     * @dev Returns the address that signed a hashed message (`hash`) with
     * `signature`. This address can then be used for verification purposes.
     *
     * The `ecrecover` EVM precompile allows for malleable (non-unique) signatures:
     * this function rejects them by requiring the `s` value to be in the lower
     * half order, and the `v` value to be either 27 or 28.
     *
     * IMPORTANT: `hash` _must_ be the result of a hash operation for the
     * verification to be secure: it is possible to craft signatures that
     * recover to arbitrary addresses for non-hashed data. A safe way to ensure
     * this is by receiving a hash of the original message (which may otherwise
     * be too long), and then calling {MessageHashUtils-toEthSignedMessageHash} on it.
     */
    function recover(bytes32 hash, bytes memory signature) internal pure returns (address) {
        (address recovered, RecoverError error, bytes32 errorArg) = tryRecover(hash, signature);
        _throwError(error, errorArg);
        return recovered;
    }

    /**
     * @dev Overload of {ECDSA-tryRecover} that receives the `r` and `vs` short-signature fields separately.
     *
     * See https://eips.ethereum.org/EIPS/eip-2098[ERC-2098 short signatures]
     */
    function tryRecover(
        bytes32 hash,
        bytes32 r,
        bytes32 vs
    ) internal pure returns (address recovered, RecoverError err, bytes32 errArg) {
        unchecked {
            bytes32 s = vs & bytes32(0x7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff);
            // We do not check for an overflow here since the shift operation results in 0 or 1.
            uint8 v = uint8((uint256(vs) >> 255) + 27);
            return tryRecover(hash, v, r, s);
        }
    }

    /**
     * @dev Overload of {ECDSA-recover} that receives the `r and `vs` short-signature fields separately.
     */
    function recover(bytes32 hash, bytes32 r, bytes32 vs) internal pure returns (address) {
        (address recovered, RecoverError error, bytes32 errorArg) = tryRecover(hash, r, vs);
        _throwError(error, errorArg);
        return recovered;
    }

    /**
     * @dev Overload of {ECDSA-tryRecover} that receives the `v`,
     * `r` and `s` signature fields separately.
     */
    function tryRecover(
        bytes32 hash,
        uint8 v,
        bytes32 r,
        bytes32 s
    ) internal pure returns (address recovered, RecoverError err, bytes32 errArg) {
        // EIP-2 still allows signature malleability for ecrecover(). Remove this possibility and make the signature
        // unique. Appendix F in the Ethereum Yellow paper (https://ethereum.github.io/yellowpaper/paper.pdf), defines
        // the valid range for s in (301): 0 < s < secp256k1n ÷ 2 + 1, and for v in (302): v ∈ {27, 28}. Most
        // signatures from current libraries generate a unique signature with an s-value in the lower half order.
        //
        // If your library generates malleable signatures, such as s-values in the upper range, calculate a new s-value
        // with 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141 - s1 and flip v from 27 to 28 or
        // vice versa. If your library also generates signatures with 0/1 for v instead 27/28, add 27 to v to accept
        // these malleable signatures as well.
        if (uint256(s) > 0x7FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF5D576E7357A4501DDFE92F46681B20A0) {
            return (address(0), RecoverError.InvalidSignatureS, s);
        }

        // If the signature is valid (and not malleable), return the signer address
        address signer = ecrecover(hash, v, r, s);
        if (signer == address(0)) {
            return (address(0), RecoverError.InvalidSignature, bytes32(0));
        }

        return (signer, RecoverError.NoError, bytes32(0));
    }

    /**
     * @dev Overload of {ECDSA-recover} that receives the `v`,
     * `r` and `s` signature fields separately.
     */
    function recover(bytes32 hash, uint8 v, bytes32 r, bytes32 s) internal pure returns (address) {
        (address recovered, RecoverError error, bytes32 errorArg) = tryRecover(hash, v, r, s);
        _throwError(error, errorArg);
        return recovered;
    }

    /**
     * @dev Optionally reverts with the corresponding custom error according to the `error` argument provided.
     */
    function _throwError(RecoverError error, bytes32 errorArg) private pure {
        if (error == RecoverError.NoError) {
            return; // no error: do nothing
        } else if (error == RecoverError.InvalidSignature) {
            revert ECDSAInvalidSignature();
        } else if (error == RecoverError.InvalidSignatureLength) {
            revert ECDSAInvalidSignatureLength(uint256(errorArg));
        } else if (error == RecoverError.InvalidSignatureS) {
            revert ECDSAInvalidSignatureS(errorArg);
        }
    }
}


// File contracts/LeveIA_AuditRegistry.sol

// Original license: SPDX_License_Identifier: MIT
pragma solidity ^0.8.20;



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
