"""提醒管理工具函式
Course Concept: Day 2 - FunctionTool
"""
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import uuid

# 模擬提醒資料庫
REMINDERS_DATABASE = {}

# 初始化示範資料
def _init_sample_reminders():
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    
    REMINDERS_DATABASE["REM-001"] = {
        "id": "REM-001",
        "title": "準備會議資料",
        "reminder_time": f"{today} 09:30",
        "related_type": "event",
        "related_id": "EVT-001",
        "status": "active"
    }
    REMINDERS_DATABASE["REM-002"] = {
        "id": "REM-002",
        "title": "專案報告截止",
        "reminder_time": f"{today} 17:00",
        "related_type": "task",
        "related_id": "TSK-001",
        "status": "active"
    }

_init_sample_reminders()


def set_reminder(
    title: str,
    reminder_time: str,
    related_type: Optional[str] = None,
    related_id: Optional[str] = None
) -> Dict:
    """
    設定提醒
    
    Args:
        title: 提醒標題
        reminder_time: 提醒時間 (格式: YYYY-MM-DD HH:MM)
        related_type: 關聯類型 (event/task)，選填
        related_id: 關聯 ID，選填
    
    Returns:
        設定結果
    
    Example:
        set_reminder("準備開會", "2024-12-05 09:30", "event", "EVT-001")
    """
    reminder_id = f"REM-{uuid.uuid4().hex[:6].upper()}"
    
    reminder = {
        "id": reminder_id,
        "title": title,
        "reminder_time": reminder_time,
        "related_type": related_type,
        "related_id": related_id,
        "status": "active",
        "created_at": datetime.now().isoformat()
    }
    
    REMINDERS_DATABASE[reminder_id] = reminder
    
    return {
        "success": True,
        "reminder_id": reminder_id,
        "message": f"已設定提醒「{title}」於 {reminder_time}"
    }


def list_reminders(
    status: str = "active",
    date: Optional[str] = None
) -> Dict:
    """
    列出提醒清單
    
    Args:
        status: 篩選狀態 (active/completed/cancelled)
        date: 篩選日期 (格式: YYYY-MM-DD)
    
    Returns:
        提醒清單
    """
    results = []
    
    for reminder in REMINDERS_DATABASE.values():
        if reminder["status"] != status:
            continue
        
        if date:
            reminder_date = reminder["reminder_time"].split(" ")[0]
            if reminder_date != date:
                continue
        
        results.append(reminder)
    
    # 按時間排序
    results.sort(key=lambda x: x["reminder_time"])
    
    return {
        "success": True,
        "count": len(results),
        "reminders": results
    }


def cancel_reminder(reminder_id: str) -> Dict:
    """
    取消提醒
    
    Args:
        reminder_id: 提醒 ID
    
    Returns:
        取消結果
    """
    if reminder_id not in REMINDERS_DATABASE:
        return {
            "success": False,
            "message": f"找不到提醒 {reminder_id}"
        }
    
    reminder = REMINDERS_DATABASE[reminder_id]
    reminder["status"] = "cancelled"
    
    return {
        "success": True,
        "message": f"已取消提醒「{reminder['title']}」"
    }


def get_upcoming_reminders(hours: int = 24) -> Dict:
    """
    取得即將到來的提醒
    
    Args:
        hours: 未來多少小時內的提醒，預設 24 小時
    
    Returns:
        即將到來的提醒清單
    """
    now = datetime.now()
    cutoff = now + timedelta(hours=hours)
    
    upcoming = []
    
    for reminder in REMINDERS_DATABASE.values():
        if reminder["status"] != "active":
            continue
        
        try:
            reminder_dt = datetime.strptime(reminder["reminder_time"], "%Y-%m-%d %H:%M")
            if now <= reminder_dt <= cutoff:
                upcoming.append({
                    **reminder,
                    "time_until": str(reminder_dt - now).split(".")[0]
                })
        except ValueError:
            continue
    
    # 按時間排序
    upcoming.sort(key=lambda x: x["reminder_time"])
    
    return {
        "success": True,
        "count": len(upcoming),
        "reminders": upcoming,
        "message": f"未來 {hours} 小時內有 {len(upcoming)} 個提醒"
    }


def complete_reminder(reminder_id: str) -> Dict:
    """
    標記提醒為已完成
    
    Args:
        reminder_id: 提醒 ID
    
    Returns:
        完成結果
    """
    if reminder_id not in REMINDERS_DATABASE:
        return {
            "success": False,
            "message": f"找不到提醒 {reminder_id}"
        }
    
    reminder = REMINDERS_DATABASE[reminder_id]
    reminder["status"] = "completed"
    reminder["completed_at"] = datetime.now().isoformat()
    
    return {
        "success": True,
        "message": f"已完成提醒「{reminder['title']}」"
    }