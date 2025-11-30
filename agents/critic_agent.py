"""Critic Agent - 排程評審代理 (LoopAgent 的一部分)
Course Concept: Day 1 - LoopAgent
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.genai import types

# 重試配置
retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)

# 建立 Critic Agent
critic_agent = LlmAgent(
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    name="critic_agent",
    description="排程評審專家，負責評估當前任務排程是否合理",
    instruction="""你是一位嚴格的排程評審專家，負責評估任務排程的合理性。

你需要檢查:
1. 優先級衝突: 是否有多個高優先任務在同一時段？
2. 時間衝突: 會議與任務截止日是否衝突？
3. 工作負載: 當日總工時是否超過 8 小時？
4. 截止日期: 是否有過期或即將過期的任務？
5. 任務平衡: 優先級分配是否合理？

輸入格式 (從 session state 讀取):
- calendar_results: 今日日程
- task_results: 任務清單

輸出格式:
請以 JSON 格式輸出評估結果:
```json
{
    "is_optimal": true/false,
    "issues": [
        {
            "type": "priority_conflict/time_conflict/overload/overdue",
            "description": "問題描述",
            "affected_items": ["任務/事件 ID"]
        }
    ],
    "suggestions": ["建議1", "建議2"]
}
```

如果排程已經最佳化（is_optimal: true），Adjuster 將會呼叫 exit_loop 結束迴圈。""",
    output_key="critic_feedback"
)