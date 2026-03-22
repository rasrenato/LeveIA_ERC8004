// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title PaymentSplitter - Leve IA
 * @dev Contrato para divisão automática de pagamentos de sinais
 * 
 * Split: 70% Treasury, 30% Referrer
 * Suporta USDT e LEVE (BEP-20 na BSC)
 * 
 * Segurança:
 * - ReentrancyGuard
 * - Ownable (apenas owner pode sacar tokens presos)
 * - Eventos para auditoria on-chain
 */
contract PaymentSplitter is ReentrancyGuard, Ownable {
    using SafeERC20 for IERC20;
    
    // Endereços oficiais
    address public treasury;
    
    // Tokens suportados
    address public immutable USDT = 0x55d398326f99059fF775485246999027B3197955;
    address public immutable LEVE = 0x67e463AcC3B35406B0f35C8Ed531da89f9670861;
    
    // Split percentages (em basis points: 10000 = 100%)
    uint256 public constant TREASURY_SHARE = 7000; // 70%
    uint256 public constant REFERRER_SHARE = 3000; // 30%
    uint256 public constant BASIS_POINTS = 10000;
    
    // Estatísticas
    uint256 public totalPayments;
    uint256 public totalVolume;
    mapping(address => uint256) public referrerEarnings;
    
    // Eventos
    event PaymentSplit(
        address indexed payer,
        address indexed referrer,
        address token,
        uint256 amount,
        uint256 treasuryAmount,
        uint256 referrerAmount
    );
    
    event TreasuryUpdated(address oldTreasury, address newTreasury);
    event TokensWithdrawn(address indexed token, uint256 amount);
    
    /**
     * @dev Constructor
     * @param _treasury Endereço do Cofre da Leve IA
     */
    constructor(address _treasury) Ownable(msg.sender) {
        require(_treasury != address(0), "Treasury cannot be zero");
        treasury = _treasury;
    }
    
    /**
     * @dev Paga por um sinal com divisão automática
     * @param token Endereço do token (USDT ou LEVE)
     * @param amount Quantidade de tokens (em wei)
     * @param referrer Endereço de quem indicou (ou address(0) se não tiver)
     * @param signalId ID do sinal (para auditoria)
     * 
     * Requisitos:
     * - Token deve ser USDT ou LEVE
     * - Payer deve dar approve() antes neste contrato
     * - Amount > 0
     */
    function payForSignal(
        address token,
        uint256 amount,
        address referrer,
        string calldata signalId
    ) external nonReentrant returns (bool) {
        // Validações
        require(token == USDT || token == LEVE, "Token not supported");
        require(amount > 0, "Amount must be > 0");
        require(referrer != msg.sender, "Referrer cannot be payer");
        
        // Atualizar estatísticas
        totalPayments++;
        totalVolume += amount;
        
        // Calcular split
        uint256 treasuryAmount = (amount * TREASURY_SHARE) / BASIS_POINTS;
        uint256 referrerAmount = (amount * REFERRER_SHARE) / BASIS_POINTS;
        
        // Se não tem referrer, treasury ganha tudo
        if (referrer == address(0)) {
            treasuryAmount = amount;
            referrerAmount = 0;
        }
        
        // Transferir tokens do payer para este contrato
        IERC20(token).safeTransferFrom(msg.sender, address(this), amount);
        
        // Enviar para o Treasury
        if (treasuryAmount > 0) {
            IERC20(token).safeTransfer(treasury, treasuryAmount);
        }
        
        // Enviar para o Referrer (se existir)
        if (referrer != address(0) && referrerAmount > 0) {
            IERC20(token).safeTransfer(referrer, referrerAmount);
            referrerEarnings[referrer] += referrerAmount;
        }
        
        // Emitir evento para auditoria
        emit PaymentSplit(
            msg.sender,
            referrer,
            token,
            amount,
            treasuryAmount,
            referrerAmount
        );
        
        return true;
    }
    
    /**
     * @dev Owner pode sacar tokens presos (emergência)
     */
    function withdrawStuckTokens(
        address token,
        uint256 amount
    ) external onlyOwner {
        require(token != address(0), "Token cannot be zero");
        IERC20(token).safeTransfer(owner(), amount);
        
        emit TokensWithdrawn(token, amount);
    }
    
    /**
     * @dev Atualizar endereço do treasury
     */
    function setTreasury(address _treasury) external onlyOwner {
        require(_treasury != address(0), "Treasury cannot be zero");
        address oldTreasury = treasury;
        treasury = _treasury;
        
        emit TreasuryUpdated(oldTreasury, _treasury);
    }
    
    /**
     * @dev View functions para o frontend
     */
    function getSplitAmounts(
        uint256 amount,
        address referrer
    ) external view returns (uint256 treasuryAmount, uint256 referrerAmount) {
        if (referrer == address(0)) {
            return (amount, 0);
        }
        
        treasuryAmount = (amount * TREASURY_SHARE) / BASIS_POINTS;
        referrerAmount = (amount * REFERRER_SHARE) / BASIS_POINTS;
    }
    
    function getReferrerEarnings(address referrer) external view returns (uint256) {
        return referrerEarnings[referrer];
    }
    
    // Receive ETH (caso alguém envie por engano)
    receive() external payable {}
}
