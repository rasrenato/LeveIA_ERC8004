const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("ERC8183 Agentic Commerce Protocol", function () {
  let acp, token, client, provider, evaluator, treasury;
  const PLATFORM_FEE_BPS = 10; // 0.1%

  beforeEach(async function () {
    [client, provider, evaluator, treasury] = await ethers.getSigners();

    // Deploy mock token
    const Token = await ethers.getContractFactory("MockERC20");
    token = await Token.deploy("Mock USDT", "USDT", 1000000n * 10n ** 18n);
    await token.waitForDeployment();

    // Deploy ERC8183
    const ERC8183 = await ethers.getContractFactory("ERC8183");
    acp = await ERC8183.deploy(treasury.address, PLATFORM_FEE_BPS);
    await acp.waitForDeployment();
  });

  describe("Create Job", function () {
    it("Should create job in Open state", async function () {
      const expiredAt = Math.floor(Date.now() / 1000) + 86400 * 7; // 7 days
      
      const tx = await acp.createJob(
        provider.address,
        evaluator.address,
        expiredAt,
        "Test job",
        ethers.ZeroAddress,
        await token.getAddress()
      );
      await tx.wait();

      const job = await acp.getJob(1);
      expect(job.client).to.equal(client.address);
      expect(job.provider).to.equal(provider.address);
      expect(job.evaluator).to.equal(evaluator.address);
      expect(job.status).to.equal(0); // Open
      expect(job.budget).to.equal(0);
    });

    it("Should revert if evaluator is zero", async function () {
      await expect(
        acp.createJob(
          provider.address,
          ethers.ZeroAddress,
          Math.floor(Date.now() / 1000) + 86400,
          "Test",
          ethers.ZeroAddress,
          await token.getAddress()
        )
      ).to.be.revertedWith("Evaluator cannot be zero");
    });
  });

  describe("Fund Job", function () {
    it("Should fund job and move to Funded state", async function () {
      const expiredAt = Math.floor(Date.now() / 1000) + 86400 * 7;
      const budget = 100n * 10n ** 6n; // 100 USDT (6 decimals)

      await acp.createJob(
        provider.address,
        evaluator.address,
        expiredAt,
        "Test job",
        ethers.ZeroAddress,
        await token.getAddress()
      );

      await acp.setBudget(1, budget, "0x");
      
      await token.approve(await acp.getAddress(), budget);
      await acp.fund(1, budget, "0x");

      const job = await acp.getJob(1);
      expect(job.status).to.equal(1); // Funded
      expect(job.budget).to.equal(budget);
    });
  });

  describe("Submit Work", function () {
    it("Should submit work and move to Submitted state", async function () {
      const expiredAt = Math.floor(Date.now() / 1000) + 86400 * 7;
      const budget = 100n * 10n ** 6n;
      const deliverable = ethers.keccak256(ethers.toUtf8Bytes("work"));

      await acp.createJob(
        provider.address,
        evaluator.address,
        expiredAt,
        "Test job",
        ethers.ZeroAddress,
        await token.getAddress()
      );

      await acp.setBudget(1, budget, "0x");
      await token.approve(await acp.getAddress(), budget);
      await acp.fund(1, budget, "0x");

      // Provider submits
      await acp.connect(provider).submit(1, deliverable, "0x");

      const job = await acp.getJob(1);
      expect(job.status).to.equal(2); // Submitted
    });
  });

  describe("Complete Job", function () {
    it("Should complete job and pay provider", async function () {
      const expiredAt = Math.floor(Date.now() / 1000) + 86400 * 7;
      const budget = 100n * 10n ** 6n;
      const deliverable = ethers.keccak256(ethers.toUtf8Bytes("work"));
      const reason = ethers.keccak256(ethers.toUtf8Bytes("approved"));

      await acp.createJob(
        provider.address,
        evaluator.address,
        expiredAt,
        "Test job",
        ethers.ZeroAddress,
        await token.getAddress()
      );

      await acp.setBudget(1, budget, "0x");
      await token.approve(await acp.getAddress(), budget);
      await acp.fund(1, budget, "0x");

      await acp.connect(provider).submit(1, deliverable, "0x");

      // Check provider balance before
      const providerBalanceBefore = await token.balanceOf(provider.address);

      // Evaluator completes
      await acp.connect(evaluator).complete(1, reason, "0x");

      // Check provider balance after (should receive budget - fee)
      const fee = (budget * BigInt(PLATFORM_FEE_BPS)) / 10000n;
      const expectedPayment = budget - fee;
      const providerBalanceAfter = await token.balanceOf(provider.address);
      
      expect(providerBalanceAfter - providerBalanceBefore).to.equal(expectedPayment);
      
      const job = await acp.getJob(1);
      expect(job.status).to.equal(3); // Completed
    });
  });

  describe("Reject Job", function () {
    it("Should reject job and refund client", async function () {
      const expiredAt = Math.floor(Date.now() / 1000) + 86400 * 7;
      const budget = 100n * 10n ** 6n;
      const reason = ethers.keccak256(ethers.toUtf8Bytes("rejected"));

      await acp.createJob(
        provider.address,
        evaluator.address,
        expiredAt,
        "Test job",
        ethers.ZeroAddress,
        await token.getAddress()
      );

      await acp.setBudget(1, budget, "0x");
      await token.approve(await acp.getAddress(), budget);
      await acp.fund(1, budget, "0x");

      // Check client balance before
      const clientBalanceBefore = await token.balanceOf(client.address);

      // Evaluator rejects
      await acp.connect(evaluator).reject(1, reason, "0x");

      // Check client balance after (should get full refund)
      const clientBalanceAfter = await token.balanceOf(client.address);
      expect(clientBalanceAfter - clientBalanceBefore).to.equal(budget);
      
      const job = await acp.getJob(1);
      expect(job.status).to.equal(4); // Rejected
    });
  });

  describe("Claim Refund (Expired)", function () {
    it("Should refund client after expiry", async function () {
      const expiredAt = Math.floor(Date.now() / 1000) + 3600; // 1 hour in future
      const budget = 100n * 10n ** 6n;

      await acp.createJob(
        provider.address,
        evaluator.address,
        expiredAt,
        "Test job",
        ethers.ZeroAddress,
        await token.getAddress()
      );

      await acp.setBudget(1, budget, "0x");
      await token.approve(await acp.getAddress(), budget);
      await acp.fund(1, budget, "0x");

      // Advance time to expire (1 hour + buffer)
      await ethers.provider.send("evm_increaseTime", [3700]);
      await ethers.provider.send("evm_mine");

      // Anyone can claim refund after expiry
      await acp.claimRefund(1);

      const job = await acp.getJob(1);
      expect(job.status).to.equal(5); // Expired
      
      const clientBalance = await token.balanceOf(client.address);
      expect(clientBalance).to.equal(1000000n * 10n ** 18n); // Full refund
    });
  });
});
