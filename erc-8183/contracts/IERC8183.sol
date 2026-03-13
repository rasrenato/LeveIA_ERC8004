// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title IERC8183 - Agentic Commerce Protocol Interface
 * @dev Interface para pagamentos condicionais com escrow entre agentes
 * 
 * Estados do Job:
 * - Open: Criado, budget não definido ou não fundado
 * - Funded: Budget em escrow, provider pode submeter
 * - Submitted: Provider submeteu trabalho, evaluator pode completar/rejeitar
 * - Completed: Terminal, pagamento liberado ao provider
 * - Rejected: Terminal, reembolso ao client
 * - Expired: Terminal, reembolso após expiry
 */
interface IERC8183 {
    
    // Estrutura do Job
    struct Job {
        uint256 jobId;
        address client;
        address provider;
        address evaluator;
        string description;
        uint256 budget;
        uint256 expiredAt;
        Status status;
        address hook;
        address token;
    }
    
    // Estados do Job
    enum Status {
        Open,
        Funded,
        Submitted,
        Completed,
        Rejected,
        Expired
    }
    
    // Eventos
    event JobCreated(
        uint256 indexed jobId,
        address indexed client,
        address indexed provider,
        address evaluator,
        uint256 expiredAt,
        string description
    );
    
    event ProviderSet(uint256 indexed jobId, address indexed provider);
    event BudgetSet(uint256 indexed jobId, uint256 amount);
    event JobFunded(uint256 indexed jobId, address indexed client, uint256 amount);
    event JobSubmitted(uint256 indexed jobId, address indexed provider, bytes32 deliverable);
    event JobCompleted(uint256 indexed jobId, address indexed evaluator, bytes32 reason);
    event JobRejected(uint256 indexed jobId, address indexed rejector, bytes32 reason);
    event JobExpired(uint256 indexed jobId);
    event PaymentReleased(uint256 indexed jobId, address indexed provider, uint256 amount);
    event Refunded(uint256 indexed jobId, address indexed client, uint256 amount);
    
    // Funções Core
    function createJob(
        address provider,
        address evaluator,
        uint256 expiredAt,
        string calldata description,
        address hook,
        address token
    ) external returns (uint256 jobId);
    
    function setProvider(uint256 jobId, address provider, bytes calldata optParams) external;
    function setBudget(uint256 jobId, uint256 amount, bytes calldata optParams) external;
    function fund(uint256 jobId, uint256 expectedBudget, bytes calldata optParams) external;
    function submit(uint256 jobId, bytes32 deliverable, bytes calldata optParams) external;
    function complete(uint256 jobId, bytes32 reason, bytes calldata optParams) external;
    function reject(uint256 jobId, bytes32 reason, bytes calldata optParams) external;
    function claimRefund(uint256 jobId) external;
    
    // Views
    function getJob(uint256 jobId) external view returns (Job memory);
    function getJobStatus(uint256 jobId) external view returns (Status);
    function jobCount() external view returns (uint256);
}
