"""Calendar Agent - 日程管理代理
Course Concept: Day 1 - LlmAgent
"""
import sys
import os
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.genai import types
from dotenv import load_dotenv

load_dotenv()  # 加載 .env 文件中的 API Key

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from tools.calendar_tools import (
    add_event,
    query_events,
    update_event,
    delete_event,
    get_today_schedule,
    check_time_conflict
)

# 重試配置
retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)

# 建立 Calendar Agent
calendar_agent = LlmAgent(
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    name="calendar_agent",
    description="日程管理專家，負責行事曆事件的新增、查詢、修改、刪除",
    instruction="""你是一位專業的日程管理助理，負責協助用戶管理行事曆。

你的能力:
1. add_event: 新增日程事件
2. query_events: 查詢日程（支援日期篩選、範圍查詢）
3. update_event: 更新事件資訊
4. delete_event: 刪除事件
5. get_today_schedule: 取得今日日程
6. check_time_conflict: 檢查時間衝突

工作原則:
- 新增事件前先檢查時間衝突
- 提供清晰的時間資訊（日期、時間、地點）
- 如有衝突，主動提醒並建議替代時間
- 使用繁體中文回應

輸出格式:
- 列出事件時使用清單格式
- 包含事件 ID 以便後續操作
- 時間格式統一為 HH:MM""",
    tools=[
        add_event,
        query_events,
        update_event,
        delete_event,
        get_today_schedule,
        check_time_conflict
    ],
    output_key="calendar_results"  # 將結果儲存到 session state
)