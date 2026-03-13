// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
import "./IERC8183.sol";
import "./IACPHook.sol";

/**
 * @title ERC8183 - Agentic Commerce Protocol (BSC Version)
 * @dev Implementação do padrão ERC-8183 para pagamentos condicionais com escrow
 * 
 * Deploy na Binance Smart Chain (BSC)
 * 
 * Features:
 * - Job escrow com 6 estados (Open, Funded, Submitted, Completed, Rejected, Expired)
 * - Hooks extensíveis para customização
 * - Compatível com ERC-8004 (reputação)
 * - Gas otimizado para BSC (~$0.10-0.50 por transação)
 * - Integrado com token LEVE (BEP-20)
 */
contract ERC8183 is IERC8183, ReentrancyGuard {
    using SafeERC20 for IERC20;
    
    // Mapeamentos
    mapping(uint256 => Job) public jobs;
    mapping(address => uint256[]) public clientJobs;
    mapping(address => uint256[]) public providerJobs;
    mapping(address => uint256[]) public evaluatorJobs;
    
    // Contadores
    uint256 public override jobCount;
    
    // Configurações
    address public treasury;
    uint256 public platformFeeBps; // Basis points (100 = 1%)
    
    // Selectors para hooks
    bytes4 internal constant SETPROVIDER_SELECTOR = bytes4(keccak256("setProvider(uint256,address,bytes)"));
    bytes4 internal constant SETBUDGET_SELECTOR = bytes4(keccak256("setBudget(uint256,uint256,bytes)"));
    bytes4 internal constant FUND_SELECTOR = bytes4(keccak256("fund(uint256,uint256,bytes)"));
    bytes4 internal constant SUBMIT_SELECTOR = bytes4(keccak256("submit(uint256,bytes32,bytes)"));
    bytes4 internal constant COMPLETE_SELECTOR = bytes4(keccak256("complete(uint256,bytes32,bytes)"));
    bytes4 internal constant REJECT_SELECTOR = bytes4(keccak256("reject(uint256,bytes32,bytes)"));
    
    constructor(address _treasury, uint256 _platformFeeBps) {
        treasury = _treasury;
        platformFeeBps = _platformFeeBps;
    }
    
    /**
     * @dev Cria novo job
     */
    function createJob(
        address provider,
        address evaluator,
        uint256 expiredAt,
        string calldata description,
        address hook,
        address token
    ) external override returns (uint256 jobId) {
        require(evaluator != address(0), "Evaluator cannot be zero");
        require(expiredAt > block.timestamp, "expiredAt must be in future");
        
        jobCount++;
        jobId = jobCount;
        
        Job storage job = jobs[jobId];
        job.jobId = jobId;
        job.client = msg.sender;
        job.provider = provider;
        job.evaluator = evaluator;
        job.description = description;
        job.budget = 0;
        job.expiredAt = expiredAt;
        job.status = Status.Open;
        job.hook = hook;
        job.token = token;
        
        // Indexar para busca
        clientJobs[msg.sender].push(jobId);
        if (provider != address(0)) {
            providerJobs[provider].push(jobId);
        }
        evaluatorJobs[evaluator].push(jobId);
        
        emit JobCreated(jobId, msg.sender, provider, evaluator, expiredAt, description);
    }
    
    /**
     * @dev Define provider (apenas se job criado sem provider)
     */
    function setProvider(
        uint256 jobId,
        address provider,
        bytes calldata optParams
    ) external override nonReentrant {
        Job storage job = jobs[jobId];
        
        require(job.status == Status.Open, "Job not Open");
        require(job.provider == address(0), "Provider already set");
        require(provider != address(0), "Provider cannot be zero");
        require(msg.sender == job.client, "Only client can set provider");
        
        // Hook before
        _callHook(jobId, SETPROVIDER_SELECTOR, abi.encode(provider, optParams), true);
        
        job.provider = provider;
        providerJobs[provider].push(jobId);
        
        // Hook after
        _callHook(jobId, SETPROVIDER_SELECTOR, abi.encode(provider, optParams), false);
        
        emit ProviderSet(jobId, provider);
    }
    
    /**
     * @dev Define budget do job
     */
    function setBudget(
        uint256 jobId,
        uint256 amount,
        bytes calldata optParams
    ) external override nonReentrant {
        Job storage job = jobs[jobId];
        
        require(job.status == Status.Open, "Job not Open");
        require(
            msg.sender == job.client || msg.sender == job.provider,
            "Only client or provider"
        );
        require(amount > 0, "Budget must be > 0");
        
        // Hook before
        _callHook(jobId, SETBUDGET_SELECTOR, abi.encode(amount, optParams), true);
        
        job.budget = amount;
        
        // Hook after
        _callHook(jobId, SETBUDGET_SELECTOR, abi.encode(amount, optParams), false);
        
        emit BudgetSet(jobId, amount);
    }
    
    /**
     * @dev Fundeia job (client transfere tokens para escrow)
     */
    function fund(
        uint256 jobId,
        uint256 expectedBudget,
        bytes calldata optParams
    ) external override nonReentrant {
        Job storage job = jobs[jobId];
        
        require(job.status == Status.Open, "Job not Open");
        require(msg.sender == job.client, "Only client can fund");
        require(job.provider != address(0), "Provider must be set");
        require(job.budget > 0, "Budget must be set");
        require(job.budget == expectedBudget, "Budget mismatch");
        
        // Hook before
        _callHook(jobId, FUND_SELECTOR, optParams, true);
        
        // Transferir tokens do client para escrow
        IERC20(job.token).safeTransferFrom(msg.sender, address(this), job.budget);
        
        job.status = Status.Funded;
        
        // Hook after
        _callHook(jobId, FUND_SELECTOR, optParams, false);
        
        emit JobFunded(jobId, msg.sender, job.budget);
    }
    
    /**
     * @dev Provider submete trabalho
     */
    function submit(
        uint256 jobId,
        bytes32 deliverable,
        bytes calldata optParams
    ) external override nonReentrant {
        Job storage job = jobs[jobId];
        
        require(job.status == Status.Funded, "Job not Funded");
        require(msg.sender == job.provider, "Only provider can submit");
        
        // Hook before
        _callHook(jobId, SUBMIT_SELECTOR, abi.encode(deliverable, optParams), true);
        
        job.status = Status.Submitted;
        
        // Hook after
        _callHook(jobId, SUBMIT_SELECTOR, abi.encode(deliverable, optParams), false);
        
        emit JobSubmitted(jobId, msg.sender, deliverable);
    }
    
    /**
     * @dev Evaluator completa job (libera pagamento)
     */
    function complete(
        uint256 jobId,
        bytes32 reason,
        bytes calldata optParams
    ) external override nonReentrant {
        Job storage job = jobs[jobId];
        
        require(job.status == Status.Submitted, "Job not Submitted");
        require(msg.sender == job.evaluator, "Only evaluator can complete");
        
        // Hook before
        _callHook(jobId, COMPLETE_SELECTOR, abi.encode(reason, optParams), true);
        
        job.status = Status.Completed;
        
        // Calcular pagamento (budget - platform fee)
        uint256 fee = (job.budget * platformFeeBps) / 10000;
        uint256 payment = job.budget - fee;
        
        // Liberar pagamento ao provider
        IERC20(job.token).safeTransfer(job.provider, payment);
        
        // Liberar fee para treasury (se > 0)
        if (fee > 0) {
            IERC20(job.token).safeTransfer(treasury, fee);
        }
        
        // Hook after
        _callHook(jobId, COMPLETE_SELECTOR, abi.encode(reason, optParams), false);
        
        emit JobCompleted(jobId, msg.sender, reason);
        emit PaymentReleased(jobId, job.provider, payment);
    }
    
    /**
     * @dev Rejeita job (reembolsa client)
     */
    function reject(
        uint256 jobId,
        bytes32 reason,
        bytes calldata optParams
    ) external override nonReentrant {
        Job storage job = jobs[jobId];
        
        require(
            job.status == Status.Open ||
            job.status == Status.Funded ||
            job.status == Status.Submitted,
            "Invalid status"
        );
        require(
            (job.status == Status.Open && msg.sender == job.client) ||
            (
                (job.status == Status.Funded || job.status == Status.Submitted) &&
                msg.sender == job.evaluator
            ),
            "Unauthorized rejector"
        );
        
        // Hook before
        _callHook(jobId, REJECT_SELECTOR, abi.encode(reason, optParams), true);
        
        job.status = Status.Rejected;
        
        // Reembolsar tokens ao client
        if (job.budget > 0) {
            IERC20(job.token).safeTransfer(job.client, job.budget);
        }
        
        // Hook after
        _callHook(jobId, REJECT_SELECTOR, abi.encode(reason, optParams), false);
        
        emit JobRejected(jobId, msg.sender, reason);
        emit Refunded(jobId, job.client, job.budget);
    }
    
    /**
     * @dev Claim refund após expiry
     */
    function claimRefund(uint256 jobId) external override nonReentrant {
        Job storage job = jobs[jobId];
        
        require(
            job.status == Status.Funded || job.status == Status.Submitted,
            "Invalid status"
        );
        require(block.timestamp >= job.expiredAt, "Not expired yet");
        
        job.status = Status.Expired;
        
        // Reembolsar tokens ao client
        uint256 refundAmount = job.budget;
        IERC20(job.token).safeTransfer(job.client, refundAmount);
        
        emit JobExpired(jobId);
        emit Refunded(jobId, job.client, refundAmount);
    }
    
    /**
     * @dev Retorna detalhes do job
     */
    function getJob(uint256 jobId) external view override returns (Job memory) {
        require(jobId <= jobCount && jobId > 0, "Invalid jobId");
        return jobs[jobId];
    }
    
    /**
     * @dev Retorna status do job
     */
    function getJobStatus(uint256 jobId) external view override returns (Status) {
        require(jobId <= jobCount && jobId > 0, "Invalid jobId");
        return jobs[jobId].status;
    }
    
    /**
     * @dev Retorna jobs de um client
     */
    function getClientJobs(address client) external view returns (uint256[] memory) {
        return clientJobs[client];
    }
    
    /**
     * @dev Retorna jobs de um provider
     */
    function getProviderJobs(address provider) external view returns (uint256[] memory) {
        return providerJobs[provider];
    }
    
    /**
     * @dev Chama hook se configurado
     */
    function _callHook(
        uint256 jobId,
        bytes4 selector,
        bytes memory data,
        bool isBefore
    ) internal {
        Job storage job = jobs[jobId];
        if (job.hook == address(0)) {
            return;
        }
        
        try IACPHook(job.hook).beforeOrAfterAction(jobId, selector, data, isBefore) {
            // Hook executado com sucesso
        } catch {
            // Hook falhou - ignora (não reverte o core)
        }
    }
}
