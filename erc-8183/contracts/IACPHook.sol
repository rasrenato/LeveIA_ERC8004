// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title IACPHook - Interface para hooks do Agentic Commerce Protocol
 * @dev Hooks permitem estender o protocolo sem modificar o core
 */
interface IACPHook {
    /**
     * @dev Callback chamado antes e depois de cada ação core
     * @param jobId ID do job
     * @param selector Seletor da função sendo chamada
     * @param data Dados codificados da função
     * @param isBefore true = before hook, false = after hook
     */
    function beforeOrAfterAction(
        uint256 jobId,
        bytes4 selector,
        bytes calldata data,
        bool isBefore
    ) external;
}

/**
 * @title BaseACPHook - Implementação base para hooks
 * @dev Fornece routing automático para métodos específicos
 */
abstract contract BaseACPHook is IACPHook {
    bytes4 internal constant SETPROVIDER_SELECTOR = bytes4(keccak256("setProvider(uint256,address,bytes)"));
    bytes4 internal constant SETBUDGET_SELECTOR = bytes4(keccak256("setBudget(uint256,uint256,bytes)"));
    bytes4 internal constant FUND_SELECTOR = bytes4(keccak256("fund(uint256,uint256,bytes)"));
    bytes4 internal constant SUBMIT_SELECTOR = bytes4(keccak256("submit(uint256,bytes32,bytes)"));
    bytes4 internal constant COMPLETE_SELECTOR = bytes4(keccak256("complete(uint256,bytes32,bytes)"));
    bytes4 internal constant REJECT_SELECTOR = bytes4(keccak256("reject(uint256,bytes32,bytes)"));
    
    function beforeOrAfterAction(
        uint256 jobId,
        bytes4 selector,
        bytes calldata data,
        bool isBefore
    ) external override {
        if (isBefore) {
            _beforeAction(jobId, selector, data);
        } else {
            _afterAction(jobId, selector, data);
        }
    }
    
    function _beforeAction(
        uint256 jobId,
        bytes4 selector,
        bytes calldata data
    ) internal virtual {
        if (selector == SETPROVIDER_SELECTOR) {
            (address provider, bytes memory optParams) = abi.decode(data, (address, bytes));
            _preSetProvider(jobId, provider, optParams);
        } else if (selector == SETBUDGET_SELECTOR) {
            (uint256 amount, bytes memory optParams) = abi.decode(data, (uint256, bytes));
            _preSetBudget(jobId, amount, optParams);
        } else if (selector == FUND_SELECTOR) {
            _preFund(jobId, data);
        } else if (selector == SUBMIT_SELECTOR) {
            (bytes32 deliverable, bytes memory optParams) = abi.decode(data, (bytes32, bytes));
            _preSubmit(jobId, deliverable, optParams);
        } else if (selector == COMPLETE_SELECTOR) {
            (bytes32 reason, bytes memory optParams) = abi.decode(data, (bytes32, bytes));
            _preComplete(jobId, reason, optParams);
        } else if (selector == REJECT_SELECTOR) {
            (bytes32 reason, bytes memory optParams) = abi.decode(data, (bytes32, bytes));
            _preReject(jobId, reason, optParams);
        }
    }
    
    function _afterAction(
        uint256 jobId,
        bytes4 selector,
        bytes calldata data
    ) internal virtual {
        if (selector == SETPROVIDER_SELECTOR) {
            (address provider, bytes memory optParams) = abi.decode(data, (address, bytes));
            _postSetProvider(jobId, provider, optParams);
        } else if (selector == SETBUDGET_SELECTOR) {
            (uint256 amount, bytes memory optParams) = abi.decode(data, (uint256, bytes));
            _postSetBudget(jobId, amount, optParams);
        } else if (selector == FUND_SELECTOR) {
            _postFund(jobId, data);
        } else if (selector == SUBMIT_SELECTOR) {
            (bytes32 deliverable, bytes memory optParams) = abi.decode(data, (bytes32, bytes));
            _postSubmit(jobId, deliverable, optParams);
        } else if (selector == COMPLETE_SELECTOR) {
            (bytes32 reason, bytes memory optParams) = abi.decode(data, (bytes32, bytes));
            _postComplete(jobId, reason, optParams);
        } else if (selector == REJECT_SELECTOR) {
            (bytes32 reason, bytes memory optParams) = abi.decode(data, (bytes32, bytes));
            _postReject(jobId, reason, optParams);
        }
    }
    
    // Override these in your hook implementation
    function _preSetProvider(uint256, address, bytes memory) internal virtual {}
    function _postSetProvider(uint256, address, bytes memory) internal virtual {}
    function _preSetBudget(uint256, uint256, bytes memory) internal virtual {}
    function _postSetBudget(uint256, uint256, bytes memory) internal virtual {}
    function _preFund(uint256, bytes memory) internal virtual {}
    function _postFund(uint256, bytes memory) internal virtual {}
    function _preSubmit(uint256, bytes32, bytes memory) internal virtual {}
    function _postSubmit(uint256, bytes32, bytes memory) internal virtual {}
    function _preComplete(uint256, bytes32, bytes memory) internal virtual {}
    function _postComplete(uint256, bytes32, bytes memory) internal virtual {}
    function _preReject(uint256, bytes32, bytes memory) internal virtual {}
    function _postReject(uint256, bytes32, bytes memory) internal virtual {}
}
