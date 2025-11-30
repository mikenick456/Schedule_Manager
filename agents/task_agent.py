"""Task Agent - 任務管理代理 (含 CodeExecutor)
Course Concept: Day 1 - LlmAgent, Day 2 - BuiltInCodeExecutor
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools.agent_tool import AgentTool
from google.genai import types

from tools.task_tools import (
    create_task,
    list_tasks,
    update_task,
    complete_task,
    delete_task,
    get_task_statistics,
    get_tasks_for_analysis
)
from agents.code_executor_agent import code_executor_agent
from dotenv import load_dotenv

load_dotenv()  # 加載 .env 文件中的 API Key
# 重試配置
retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)

# 建立 Task Agent (含 CodeExecutor)
task_agent = LlmAgent(
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    name="task_agent",
    description="任務管理專家，負責任務的建立、追蹤、分析，可使用 Python 代碼進行統計分析",
    instruction="""你是一位專業的任務管理助理，負責協助用戶管理待辦事項。

你的能力:
1. create_task: 建立新任務
2. list_tasks: 列出任務清單（支援篩選）
3. update_task: 更新任務資訊
4. complete_task: 標記任務完成
5. delete_task: 刪除任務
6. get_task_statistics: 取得任務統計
7. get_tasks_for_analysis: 取得任務資料供分析

特殊能力 - 代碼執行 (透過 code_executor_agent):
當需要進行複雜分析時，你可以使用 code_executor_agent 來執行 Python 代碼:
- 計算任務完成率
- 分析優先級分佈
- 預估總工時
- 生成視覺化圖表數據

使用方式:
當需要執行計算時，呼叫 code_executor_agent 並提供 Python 代碼要求。
例如：「計算任務完成率」→ code_executor_agent 會生成並執行代碼來計算結果。

工作原則:
- 優先級排序: urgent > high > medium > low
- 提醒用戶過期任務
- 建議合理的截止日期
- 使用繁體中文回應""",
    tools=[
        create_task,
        list_tasks,
        update_task,
        complete_task,
        delete_task,
        get_task_statistics,
        get_tasks_for_analysis,
        AgentTool(agent=code_executor_agent)  # Day 2 概念: 透過 AgentTool 使用代碼執行器
    ],
    output_key="task_results"
)