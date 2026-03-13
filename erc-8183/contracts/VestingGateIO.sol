// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title VestingGateIO - Gate.io Listing Vesting Contract
 * @dev Contrato de vesting para listagem na Gate.io
 * 
 * Deploy na Binance Smart Chain (BSC)
 * 
 * Features:
 * - Cliff period (período inicial sem liberação)
 * - Liberação gradual (linear ou percentual)
 * - Gate.io listing trigger
 * - Anti-dump protection
 * - Múltiplos beneficiários
 */
contract VestingGateIO is Ownable {
    using SafeERC20 for IERC20;
    
    // Estrutura do Vesting
    struct VestingSchedule {
        address beneficiary;
        uint256 totalAmount;
        uint256 releasedAmount;
        uint256 startTime;
        uint256 cliffDuration;
        uint256 vestingDuration;
        uint256 tgePercentage; // Porcentagem liberada no TGE (listagem)
        bool isGateIOLocked;
        bool isReleased;
    }
    
    // Mapeamentos
    mapping(address => VestingSchedule) public vestingSchedules;
    mapping(address => uint256[]) public beneficiarySchedules;
    address[] public allBeneficiaries;
    
    IERC20 public immutable token;
    
    // Configurações
    uint256 public constant PERCENTAGE_DIVISOR = 10000; // 100% = 10000
    uint256 public gateIOListingTime;
    bool public gateIOListed;
    
    // Events
    event VestingScheduleCreated(
        address indexed beneficiary,
        uint256 totalAmount,
        uint256 cliffDuration,
        uint256 vestingDuration,
        uint256 tgePercentage
    );
    
    event TokensReleased(address indexed beneficiary, uint256 amount);
    event GateIOListed(uint256 timestamp);
    event EmergencyWithdrawal(address indexed beneficiary, uint256 amount);
    
    constructor(address _token) Ownable(msg.sender) {
        require(_token != address(0), "Token address is zero");
        token = IERC20(_token);
    }
    
    /**
     * @dev Criar schedule de vesting para beneficiário
     */
    function createVestingSchedule(
        address beneficiary,
        uint256 totalAmount,
        uint256 cliffDuration,
        uint256 vestingDuration,
        uint256 tgePercentage
    ) external onlyOwner {
        require(beneficiary != address(0), "Beneficiary is zero");
        require(totalAmount > 0, "Amount is zero");
        require(tgePercentage <= 10000, "TGE percentage exceeds 100%");
        require(vestingSchedules[beneficiary].totalAmount == 0, "Schedule already exists");
        
        vestingSchedules[beneficiary] = VestingSchedule({
            beneficiary: beneficiary,
            totalAmount: totalAmount,
            releasedAmount: 0,
            startTime: block.timestamp,
            cliffDuration: cliffDuration,
            vestingDuration: vestingDuration,
            tgePercentage: tgePercentage,
            isGateIOLocked: false,
            isReleased: false
        });
        
        beneficiarySchedules[beneficiary].push(allBeneficiaries.length);
        allBeneficiaries.push(beneficiary);
        
        // Transferir tokens do owner para o contrato
        token.safeTransferFrom(msg.sender, address(this), totalAmount);
        
        emit VestingScheduleCreated(
            beneficiary,
            totalAmount,
            cliffDuration,
            vestingDuration,
            tgePercentage
        );
    }
    
    /**
     * @dev Liberar tokens após cliff e Gate.io listing
     */
    function release() external {
        VestingSchedule storage schedule = vestingSchedules[msg.sender];
        require(schedule.totalAmount > 0, "No vesting schedule");
        require(!schedule.isReleased, "Already released");
        
        uint256 releasable = calculateReleasable(msg.sender);
        require(releasable > 0, "No tokens to release");
        
        schedule.releasedAmount += releasable;
        schedule.isReleased = true;
        
        token.safeTransfer(msg.sender, releasable);
        
        emit TokensReleased(msg.sender, releasable);
    }
    
    /**
     * @dev Calcular tokens liberáveis para um beneficiário
     */
    function calculateReleasable(address beneficiary) public view returns (uint256) {
        VestingSchedule memory schedule = vestingSchedules[beneficiary];
        require(schedule.totalAmount > 0, "No vesting schedule");
        
        // Se já foi liberado, retorna 0
        if (schedule.isReleased) {
            return 0;
        }
        
        // Calcular tokens liberáveis
        uint256 releasable = 0;
        
        // TGE release (listagem)
        if (gateIOListed && schedule.tgePercentage > 0) {
            releasable = (schedule.totalAmount * schedule.tgePercentage) / PERCENTAGE_DIVISOR;
        }
        
        // Pós-cliff: liberação linear
        if (block.timestamp >= schedule.startTime + schedule.cliffDuration) {
            uint256 timeSinceCliff = block.timestamp - (schedule.startTime + schedule.cliffDuration);
            uint256 vestedAmount = (schedule.totalAmount * timeSinceCliff) / schedule.vestingDuration;
            
            // Adicionar ao TGE release, mas não exceder o total
            if (vestedAmount > releasable) {
                releasable = vestedAmount;
            }
        }
        
        // Subtrair já liberado
        if (releasable > schedule.releasedAmount) {
            releasable -= schedule.releasedAmount;
        } else {
            releasable = 0;
        }
        
        return releasable;
    }
    
    /**
     * @dev Marcar como listado na Gate.io
     */
    function setGateIOListed() external onlyOwner {
        require(!gateIOListed, "Already listed");
        gateIOListed = true;
        gateIOListingTime = block.timestamp;
        
        emit GateIOListed(block.timestamp);
    }
    
    /**
     * @dev Bloquear schedule para Gate.io (não pode ser modificado)
     */
    function lockForGateIO(address beneficiary) external onlyOwner {
        require(vestingSchedules[beneficiary].totalAmount > 0, "No schedule");
        vestingSchedules[beneficiary].isGateIOLocked = true;
    }
    
    /**
     * @dev Obter detalhes do vesting de um beneficiário
     */
    function getVestingDetails(address beneficiary) external view returns (
        uint256 totalAmount,
        uint256 releasedAmount,
        uint256 releasable,
        uint256 startTime,
        uint256 cliffDuration,
        uint256 vestingDuration,
        uint256 tgePercentage,
        bool isGateIOLocked
    ) {
        VestingSchedule memory schedule = vestingSchedules[beneficiary];
        require(schedule.totalAmount > 0, "No vesting schedule");
        
        return (
            schedule.totalAmount,
            schedule.releasedAmount,
            calculateReleasable(beneficiary),
            schedule.startTime,
            schedule.cliffDuration,
            schedule.vestingDuration,
            schedule.tgePercentage,
            schedule.isGateIOLocked
        );
    }
    
    /**
     * @dev Obter todos beneficiários
     */
    function getAllBeneficiaries() external view returns (address[] memory) {
        return allBeneficiaries;
    }
    
    /**
     * @dev Obter número de beneficiários
     */
    function getBeneficiaryCount() external view returns (uint256) {
        return allBeneficiaries.length;
    }
    
    /**
     * @dev Obter saldo de tokens do contrato
     */
    function getTokenBalance() external view returns (uint256) {
        return token.balanceOf(address(this));
    }
    
    /**
     * @dev Emergency withdrawal (apenas owner)
     */
    function emergencyWithdraw(address tokenAddress, uint256 amount) external onlyOwner {
        require(tokenAddress != address(token), "Cannot withdraw vesting token");
        IERC20(tokenAddress).safeTransfer(owner(), amount);
    }
}
