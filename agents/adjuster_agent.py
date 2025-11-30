"""Adjuster Agent - 排程調整代理 (LoopAgent 的一部分)
Course Concept: Day 1 - LoopAgent, FunctionTool (exit_loop)
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import FunctionTool
from google.genai import types

from tools.task_tools import update_task

# 重試配置
retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)


def exit_loop() -> str:
    """
    結束優化迴圈
    
    當排程已經最佳化時呼叫此函式結束 LoopAgent 迴圈。
    
    Returns:
        確認訊息
    """
    return "已結束優化迴圈，排程已最佳化！"


# 建立 Adjuster Agent
adjuster_agent = LlmAgent(
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    name="adjuster_agent",
    description="排程調整專家，根據評審建議調整任務優先級和排程",
    instruction="""你是一位排程調整專家，根據 Critic 的評估結果調整任務排程。

輸入 (從 session state 讀取):
- critic_feedback: Critic 的評估結果

調整策略:
1. 優先級衝突: 將次要任務降低優先級
2. 時間衝突: 建議將任務提前或延後
3. 工作超載: 將非緊急任務延後到明天
4. 過期任務: 提升為高優先級或建議取消

可用工具:
1. update_task: 更新任務優先級、截止日期等
2. exit_loop: 當排程已最佳化時呼叫此函式結束迴圈

工作流程:
1. 讀取 critic_feedback
2. 如果 is_optimal 為 true → 呼叫 exit_loop() 結束迴圈
3. 如果有問題 → 根據 issues 進行調整
4. 輸出調整結果

輸出格式:
```
調整報告:
- [調整1] 任務 TSK-XXX 優先級從 high 調整為 medium
- [調整2] 建議將 TSK-YYY 截止日延後至 YYYY-MM-DD

已完成本輪調整，等待下一輪評估。
```""",
    tools=[
        update_task,
        FunctionTool(func=exit_loop)  # Day 1 概念: exit_loop 結束迴圈
    ],
    output_key="adjustment_results"
)
