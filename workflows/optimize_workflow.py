import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google.adk.agents import LoopAgent

from agents.critic_agent import critic_agent
from agents.adjuster_agent import adjuster_agent

# 建立 LoopAgent 迭代優化迴圈
optimization_loop = LoopAgent(
    name="schedule_optimization_loop",
    description="迭代優化任務排程，直到排程最佳化或達到最大迭代次數",
    sub_agents=[critic_agent, adjuster_agent],
    max_iterations=3  # 最多迭代 3 次
)

"""
LoopAgent 執行流程:

Iteration 1:
    1. critic_agent 評估當前排程
    2. adjuster_agent 根據評估結果調整
    3. 如果 adjuster_agent 呼叫 exit_loop() → 結束
    4. 否則 → 繼續 Iteration 2

Iteration 2:
    ... (同上)

Iteration 3 (max_iterations):
    ... 強制結束

每次迭代都會：
- 讀取上一輪的 session state
- 輸出新的調整結果到 session state
"""