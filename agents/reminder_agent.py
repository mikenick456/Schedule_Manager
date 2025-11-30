"""Reminder Agent - 提醒管理代理
Course Concept: Day 1 - LlmAgent
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.genai import types

from tools.reminder_tools import (
    set_reminder,
    list_reminders,
    cancel_reminder,
    get_upcoming_reminders,
    complete_reminder
)

# 重試配置
retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)

# 建立 Reminder Agent
reminder_agent = LlmAgent(
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    name="reminder_agent",
    description="提醒管理專家，負責設定、查詢、管理各種提醒通知",
    instruction="""你是一位專業的提醒助理，負責協助用戶管理提醒通知。

你的能力:
1. set_reminder: 設定新提醒
2. list_reminders: 列出提醒清單
3. cancel_reminder: 取消提醒
4. get_upcoming_reminders: 取得即將到來的提醒
5. complete_reminder: 標記提醒完成

工作原則:
- 提醒時間要比事件/截止日期早（建議提前 30 分鐘或 1 天）
- 可以為事件或任務設定關聯提醒
- 主動提醒即將到期的項目
- 使用繁體中文回應

智能建議:
- 重要會議：建議設定多個提醒（前一天 + 前 30 分鐘）
- 任務截止：建議設定完成前一天提醒
- 可以根據用戶習慣調整提醒時間""",
    tools=[
        set_reminder,
        list_reminders,
        cancel_reminder,
        get_upcoming_reminders,
        complete_reminder
    ],
    output_key="reminder_results"
)