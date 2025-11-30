"""Code Executor Agent - 代碼執行代理
Course Concept: Day 2 - BuiltInCodeExecutor
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.code_executors import BuiltInCodeExecutor
from google.genai import types
from dotenv import load_dotenv

# 導入任務工具函數，讓代碼執行時可以訪問
from tools.task_tools import (
    get_task_statistics,
    get_tasks_for_analysis
)

load_dotenv()

# 重試配置
retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)

# 建立 Code Executor Agent (僅用於代碼執行，不使用 tools)
code_executor_agent = LlmAgent(
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    name="code_executor_agent",
    description="專業的 Python 代碼執行代理，負責執行複雜的計算和分析代碼",
    instruction="""你是一位專業的 Python 代碼執行專家。你的唯一職責是生成並執行 Python 代碼來完成計算和分析任務。

**重要規則：**
1. 你必須 ONLY 回應 Python 代碼塊，不要提供任何文字說明或對話
2. 不要在代碼塊前後寫任何文字
3. Python 代碼必須計算結果
4. Python 代碼必須將最終結果輸出到 stdout（使用 print）
5. 禁止自己進行計算，你的工作只是生成代碼，讓代碼執行器來執行

**使用情境：**
- 計算任務完成率、統計數據
- 分析優先級分佈
- 預估總工時
- 生成視覺化圖表數據
- 任何需要精確計算的任務

**範例：**
當用戶要求「計算任務完成率」時，你應該生成類似這樣的代碼：
```python
stats = get_task_statistics()
completion_rate = stats['by_status']['completed'] / stats['total'] * 100
print(f"任務完成率: {completion_rate:.1f}%")
```

記住：只生成代碼，不要執行計算！""",
    code_executor=BuiltInCodeExecutor(),  # Day 2 概念: 代碼執行器
)

