"""Schedule Manager Coordinator - 智慧日程管理協調代理
Course Concepts:
- Day 1: SequentialAgent, ParallelAgent, LoopAgent, AgentTool
- Day 2: BuiltInCodeExecutor
- Day 3: Session State, Memory Service, preload_memory, Context Compaction
- Day 4: LoggingPlugin, Callbacks
"""
import asyncio
import os
import uuid
import sys
from dotenv import load_dotenv

from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.memory import InMemoryMemoryService
from google.adk.tools.preload_memory_tool import preload_memory_tool
from google.adk.tools.agent_tool import AgentTool
from google.adk.plugins.logging_plugin import LoggingPlugin
from google.adk.apps.app import App, EventsCompactionConfig
from google.genai import types
#from google.adk.core.events_compaction_config import EventsCompactionConfig

from workflows.query_workflow import query_parallel
from workflows.optimize_workflow import optimization_loop
from agents.task_agent import task_agent
from callbacks.habit_callbacks import learn_user_habits

# 載入環境變數
load_dotenv()

# 重試配置
retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)


analysis_agent = LlmAgent(
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    name="analysis_agent",
    description="分析日程和任務資料，生成每日摘要和建議",
    instruction="""你是一位分析專家，負責整合日程、任務、提醒資訊並提供建議。

輸入 (從 session state 讀取):
- calendar_results: 日程資料
- task_results: 任務資料
- reminder_results: 提醒資料

分析內容:
1. 今日行程摘要
2. 待辦任務清單（按優先級排序）
3. 即將到來的提醒
4. 時間衝突警告
5. 今日行動建議

輸出格式:
```
今日行程摘要
- [時間] 事件名稱

待辦任務 (按優先級)
1. [urgent] 任務名稱 - 截止: MM/DD
2. [high] 任務名稱 - 截止: MM/DD
...

即將到來的提醒
- [時間] 提醒內容

注意事項
- 衝突/風險提醒

今日建議
- 建議1
- 建議2
```""",
    output_key="daily_summary"
)


daily_planning_pipeline = SequentialAgent(
    name="daily_planning_pipeline",
    description="每日規劃流水線: 查詢 → 分析 → 優化",
    sub_agents=[
        query_parallel,      # Step 1: ParallelAgent 並行查詢
        analysis_agent,      # Step 2: 分析整合
        optimization_loop    # Step 3: LoopAgent 迭代優化
    ]
)


coordinator = LlmAgent(
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    name="schedule_coordinator",
    description="智慧日程管理協調中心，整合日程、任務、提醒管理功能",
    instruction="""你是智慧日程管理助手，負責協助用戶管理時間和任務。

你的能力:
1. 【每日規劃】使用 daily_planning_pipeline 取得完整的每日規劃
   - 並行查詢日程、任務、提醒
   - 分析整合資訊
   - 迭代優化排程

2. 【記憶功能】使用 preload_memory 回憶用戶習慣偏好

3. 【任務分析】使用 task_agent 進行任務統計分析

路由規則:
- "今日行程" / "今天要做什麼" → daily_planning_pipeline
- "分析任務" / "任務統計" → task_agent (CodeExecutor)
- "我的習慣" / "偏好設定" → preload_memory

互動原則:
- 首次對話時詢問用戶姓名
- 提供簡潔清晰的資訊
- 主動提醒重要事項
- 使用繁體中文回應

記憶功能:
- 系統會自動學習你的使用習慣
- 可以根據習慣提供個人化建議""",
    sub_agents=[
        daily_planning_pipeline,  
    ],
    tools=[
        preload_memory_tool,               
        AgentTool(agent=task_agent)        
    ],
    after_agent_callback=learn_user_habits  
)


session_service = InMemorySessionService()
memory_service = InMemoryMemoryService()


logging_plugin = LoggingPlugin()


app = App(
    name="smart_schedule_manager",
    root_agent=coordinator,
    plugins=[logging_plugin],  
    events_compaction_config=EventsCompactionConfig(
        compaction_interval=int(os.getenv("COMPACTION_INTERVAL", 5)),
        overlap_size=int(os.getenv("OVERLAP_SIZE", 2))
    )
)

# 建立 Runner
runner = Runner(
    app=app,
    session_service=session_service,
    memory_service=memory_service
)


async def main():
    """主程式執行流程"""
    print("=" * 60)
    print("智慧日程與任務管理助手")
    print("   Smart Schedule Manager")
    print("=" * 60)
    print("\n您可以說:")
    print("   - '今天有什麼行程？'")
    print("   - '幫我新增一個會議'")
    print("   - '列出所有待辦任務'")
    print("   - '分析我的任務統計'")
    print("   - '設定明天早上的提醒'")
    print("   - '進行今日規劃'")
    print("\n輸入 'exit' 或 'quit' 結束對話\n")
    
    # 建立唯一的 session ID
    session_id = f"schedule_session_{uuid.uuid4().hex[:8]}"
    user_id = "default_user"
    
    # 建立會話
    await session_service.create_session(
        app_name="smart_schedule_manager",
        user_id=user_id,
        session_id=session_id
    )
    
    print(f"[System] 會話已建立: {session_id}\n")
    
    while True:
        try:
            user_input = input("\n您: ").strip()
            
            if user_input.lower() in ['exit', 'quit', '結束', '離開']:
                print("\n感謝使用智慧日程管理助手，祝您有充實的一天！")
                break
            
            if not user_input:
                continue
            
            # 建立訊息
            message = types.Content(
                role="user",
                parts=[types.Part(text=user_input)]
            )
            
            print("\n助手處理中...\n")
            
            # 執行對話
            response_received = False
            event_count = 0
            async for event in runner.run_async(
                user_id=user_id,
                session_id=session_id,
                new_message=message
            ):
                event_count += 1
                
               
                # 顯示所有包含文字內容的事件
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if hasattr(part, 'text') and part.text:
                            print(part.text, end="", flush=True)
                            response_received = True
                
                # 如果是最終回應，也顯示
                if event.is_final_response() and event.content:
                    for part in event.content.parts:
                        if hasattr(part, "text") and part.text:
                            print(part.text, end="", flush=True)
                            response_received = True
            
            # 如果沒有收到回應，顯示提示
            if not response_received:
                print(f"未收到回應（處理了 {event_count} 個事件），請檢查日誌或重試")
            else:
                print()  # 換行
            
        except KeyboardInterrupt:
            print("\n\n系統已中斷，再見！")
            break
        except Exception as e:
            print(f"\n發生錯誤: {e}")


if __name__ == "__main__":
    asyncio.run(main())