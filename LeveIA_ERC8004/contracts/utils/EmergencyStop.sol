// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title EmergencyStop - Circuit Breaker Pattern Implementation
 * @dev Security mechanism for pausing contract operations in emergencies
 * @notice Following best practices from OpenZeppelin and Ethereum security guidelines
 */
abstract contract EmergencyStop {
    
    // ============ STATE VARIABLES ============
    
    bool private _stopped;
    address private _owner;
    uint256 private _stopTimestamp;
    string private _stopReason;
    
    // Multi-signature requirements for critical operations
    address[] private _guardians;
    mapping(address => bool) private _isGuardian;
    uint256 private _requiredGuardians;
    
    // Time-lock for emergency stop deactivation
    uint256 public constant STOP_COOLDOWN = 24 hours;
    uint256 public constant MAX_STOP_DURATION = 30 days;
    
    // ============ EVENTS ============
    
    event EmergencyStopActivated(address indexed by, string reason, uint256 timestamp);
    event EmergencyStopDeactivated(address indexed by, uint256 timestamp);
    event GuardianAdded(address indexed guardian);
    event GuardianRemoved(address indexed guardian);
    event RequiredGuardiansUpdated(uint256 oldRequired, uint256 newRequired);
    
    // ============ MODIFIERS ============
    
    modifier onlyOwner() {
        require(msg.sender == _owner, "EmergencyStop: caller is not owner");
        _;
    }
    
    modifier onlyGuardian() {
        require(_isGuardian[msg.sender], "EmergencyStop: caller is not guardian");
        _;
    }
    
    modifier notStopped() {
        require(!_stopped, "EmergencyStop: contract is stopped");
        _;
    }
    
    modifier onlyWhenStopped() {
        require(_stopped, "EmergencyStop: contract is not stopped");
        _;
    }
    
    // ============ CONSTRUCTOR ============
    
    constructor(address owner_) {
        _owner = owner_;
        _guardians.push(owner_);
        _isGuardian[owner_] = true;
        _requiredGuardians = 1;
    }
    
    // ============ EMERGENCY STOP FUNCTIONS ============
    
    /**
     * @dev Activate emergency stop (single owner or multi-sig)
     * @param reason Reason for emergency stop
     */
    function _activateStop(string memory reason) internal {
        require(!_stopped, "EmergencyStop: already stopped");
        
        // Check if multi-sig is required
        if (_guardians.length > 1 && _requiredGuardians > 1) {
            // In production, would implement multi-sig logic
            // For now, owner can activate immediately
            require(msg.sender == _owner, "EmergencyStop: multi-sig required");
        }
        
        _stopped = true;
        _stopTimestamp = block.timestamp;
        _stopReason = reason;
        
        emit EmergencyStopActivated(msg.sender, reason, block.timestamp);
    }
    
    /**
     * @dev Deactivate emergency stop (with cooldown and multi-sig)
     */
    function _deactivateStop() internal {
        require(_stopped, "EmergencyStop: not stopped");
        require(block.timestamp >= _stopTimestamp + STOP_COOLDOWN, 
            "EmergencyStop: cooldown not passed");
        require(block.timestamp <= _stopTimestamp + MAX_STOP_DURATION,
            "EmergencyStop: stop duration exceeded");
        
        // Check if multi-sig is required for deactivation
        if (_guardians.length > 1 && _requiredGuardians > 1) {
            // In production, would implement multi-sig logic
            // For now, owner can deactivate after cooldown
            require(msg.sender == _owner, "EmergencyStop: multi-sig required");
        }
        
        _stopped = false;
        _stopTimestamp = 0;
        _stopReason = "";
        
        emit EmergencyStopDeactivated(msg.sender, block.timestamp);
    }
    
    /**
     * @dev Force deactivate emergency stop (owner only, bypasses cooldown)
     * @notice Use only in extreme circumstances
     */
    function _forceDeactivateStop() internal onlyOwner {
        require(_stopped, "EmergencyStop: not stopped");
        
        _stopped = false;
        _stopTimestamp = 0;
        _stopReason = "";
        
        emit EmergencyStopDeactivated(msg.sender, block.timestamp);
    }
    
    // ============ GUARDIAN MANAGEMENT ============
    
    /**
     * @dev Add a guardian
     * @param guardian Address to add as guardian
     */
    function addGuardian(address guardian) external onlyOwner {
        require(!_isGuardian[guardian], "EmergencyStop: already guardian");
        require(guardian != address(0), "EmergencyStop: zero address");
        
        _guardians.push(guardian);
        _isGuardian[guardian] = true;
        
        emit GuardianAdded(guardian);
    }
    
    /**
     * @dev Remove a guardian
     * @param guardian Address to remove from guardians
     */
    function removeGuardian(address guardian) external onlyOwner {
        require(_isGuardian[guardian], "EmergencyStop: not guardian");
        require(guardian != _owner, "EmergencyStop: cannot remove owner");
        require(_guardians.length > 1, "EmergencyStop: need at least one guardian");
        
        // Remove from array
        for (uint256 i = 0; i < _guardians.length; i++) {
            if (_guardians[i] == guardian) {
                _guardians[i] = _guardians[_guardians.length - 1];
                _guardians.pop();
                break;
            }
        }
        
        _isGuardian[guardian] = false;
        
        emit GuardianRemoved(guardian);
    }
    
    /**
     * @dev Update required number of guardians for multi-sig
     * @param newRequired New required number of guardians
     */
    function updateRequiredGuardians(uint256 newRequired) external onlyOwner {
        require(newRequired > 0, "EmergencyStop: required must be > 0");
        require(newRequired <= _guardians.length, 
            "EmergencyStop: required exceeds guardians");
        
        uint256 oldRequired = _requiredGuardians;
        _requiredGuardians = newRequired;
        
        emit RequiredGuardiansUpdated(oldRequired, newRequired);
    }
    
    // ============ VIEW FUNCTIONS ============
    
    /**
     * @dev Check if contract is stopped
     * @return bool Whether contract is in emergency stop state
     */
    function stopped() public view returns (bool) {
        return _stopped;
    }
    
    /**
     * @dev Get stop information
     * @return isStopped Whether contract is stopped
     * @return timestamp When stop was activated
     * @return reason Reason for stop
     * @return cooldownRemaining Time remaining until deactivation allowed
     */
    function getStopInfo() external view returns (
        bool isStopped,
        uint256 timestamp,
        string memory reason,
        uint256 cooldownRemaining
    ) {
        isStopped = _stopped;
        timestamp = _stopTimestamp;
        reason = _stopReason;
        
        if (_stopped) {
            if (block.timestamp < _stopTimestamp + STOP_COOLDOWN) {
                cooldownRemaining = (_stopTimestamp + STOP_COOLDOWN) - block.timestamp;
            } else {
                cooldownRemaining = 0;
            }
        } else {
            cooldownRemaining = 0;
        }
    }
    
    /**
     * @dev Get list of guardians
     * @return Array of guardian addresses
     */
    function getGuardians() external view returns (address[] memory) {
        return _guardians;
    }
    
    /**
     * @dev Get required number of guardians
     * @return Number of guardians required for multi-sig
     */
    function getRequiredGuardians() external view returns (uint256) {
        return _requiredGuardians;
    }
    
    /**
     * @dev Check if address is guardian
     * @param addr Address to check
     * @return bool Whether address is guardian
     */
    function isGuardian(address addr) external view returns (bool) {
        return _isGuardian[addr];
    }
    
    /**
     * @dev Get owner address
     * @return Owner address
     */
    function getOwner() external view returns (address) {
        return _owner;
    }
    
    // ============ SECURITY CHECKS ============
    
    /**
     * @dev Validate stop state before critical operations
     * @notice Should be called by inheriting contracts before sensitive operations
     */
    function _validateNotStopped() internal view {
        require(!_stopped, "EmergencyStop: contract is stopped");
    }
    
    /**
     * @dev Check if stop duration is within limits
     * @return bool Whether stop duration is within maximum allowed
     */
    function _isStopDurationValid() internal view returns (bool) {
        if (!_stopped) return true;
        return block.timestamp <= _stopTimestamp + MAX_STOP_DURATION;
    }
    
    /**
     * @dev Get time until deactivation allowed
     * @return Time in seconds until deactivation allowed (0 if ready or not stopped)
     */
    function _getCooldownRemaining() internal view returns (uint256) {
        if (!_stopped) return 0;
        if (block.timestamp >= _stopTimestamp + STOP_COOLDOWN) return 0;
        return (_stopTimestamp + STOP_COOLDOWN) - block.timestamp;
    }
}