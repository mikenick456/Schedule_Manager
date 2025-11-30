import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google.adk.agents import ParallelAgent

from agents.calendar_agent import calendar_agent
from agents.task_agent import task_agent
from agents.reminder_agent import reminder_agent

# 建立 ParallelAgent 並行查詢
query_parallel = ParallelAgent(
    name="parallel_query",
    description="同時查詢日程、任務、提醒，提升查詢效率",
    sub_agents=[calendar_agent, task_agent, reminder_agent]
)

"""
ParallelAgent 執行流程:

並行執行:
    ┌─────────────────┐
    │                 │
    ▼                 ▼
calendar_agent   task_agent   reminder_agent
    │                 │              │
    ▼                 ▼              ▼
calendar_results task_results reminder_results
    │                 │              │
    └────────┬────────┴──────────────┘
             ▼
      合併所有結果到 session state

優點:
- 3 個查詢同時執行，而非依序執行
- 總耗時 = max(各 agent 耗時)，而非 sum(各 agent 耗時)
"""