"""日程管理工具函式
Course Concept: Day 2 - FunctionTool
"""
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import uuid

# 模擬日程資料庫
CALENDAR_DATABASE = {}

# 初始化一些示範資料
def _init_sample_data():
    today = datetime.now().strftime("%Y-%m-%d")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    
    CALENDAR_DATABASE["EVT-001"] = {
        "id": "EVT-001",
        "title": "團隊週會",
        "date": today,
        "start_time": "10:00",
        "end_time": "11:00",
        "location": "會議室 A",
        "description": "討論本週進度與下週規劃"
    }
    CALENDAR_DATABASE["EVT-002"] = {
        "id": "EVT-002",
        "title": "專案評審會議",
        "date": today,
        "start_time": "14:00",
        "end_time": "16:00",
        "location": "會議室 B",
        "description": "Q4 專案進度評審"
    }
    CALENDAR_DATABASE["EVT-003"] = {
        "id": "EVT-003",
        "title": "客戶拜訪",
        "date": tomorrow,
        "start_time": "09:30",
        "end_time": "11:30",
        "location": "客戶公司",
        "description": "新產品展示"
    }

_init_sample_data()


def add_event(
    title: str,
    date: str,
    start_time: str,
    end_time: str,
    location: str = "",
    description: str = ""
) -> Dict:
    """
    新增日程事件
    
    Args:
        title: 事件標題
        date: 日期 (格式: YYYY-MM-DD)
        start_time: 開始時間 (格式: HH:MM)
        end_time: 結束時間 (格式: HH:MM)
        location: 地點 (選填)
        description: 描述 (選填)
    
    Returns:
        新增的事件資訊
    
    Example:
        add_event("部門會議", "2024-12-05", "14:00", "15:00", "會議室A")
    """
    event_id = f"EVT-{uuid.uuid4().hex[:6].upper()}"
    
    event = {
        "id": event_id,
        "title": title,
        "date": date,
        "start_time": start_time,
        "end_time": end_time,
        "location": location,
        "description": description,
        "created_at": datetime.now().isoformat()
    }
    
    CALENDAR_DATABASE[event_id] = event
    
    return {
        "success": True,
        "event_id": event_id,
        "message": f"已新增事件「{title}」於 {date} {start_time}-{end_time}"
    }


def query_events(
    date: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> Dict:
    """
    查詢日程事件
    
    Args:
        date: 特定日期 (格式: YYYY-MM-DD)
        start_date: 起始日期 (用於範圍查詢)
        end_date: 結束日期 (用於範圍查詢)
    
    Returns:
        符合條件的事件清單
    
    Example:
        query_events(date="2024-12-05")  # 查詢特定日期
        query_events(start_date="2024-12-01", end_date="2024-12-07")  # 範圍查詢
    """
    results = []
    
    for event in CALENDAR_DATABASE.values():
        event_date = event["date"]
        
        if date and event_date == date:
            results.append(event)
        elif start_date and end_date:
            if start_date <= event_date <= end_date:
                results.append(event)
        elif not date and not start_date and not end_date:
            results.append(event)
    
    # 按日期和時間排序
    results.sort(key=lambda x: (x["date"], x["start_time"]))
    
    if not results:
        return {
            "success": True,
            "count": 0,
            "events": [],
            "message": "沒有找到符合條件的事件"
        }
    
    return {
        "success": True,
        "count": len(results),
        "events": results
    }


def update_event(
    event_id: str,
    title: Optional[str] = None,
    date: Optional[str] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    location: Optional[str] = None,
    description: Optional[str] = None
) -> Dict:
    """
    更新日程事件
    
    Args:
        event_id: 事件 ID
        title: 新標題 (選填)
        date: 新日期 (選填)
        start_time: 新開始時間 (選填)
        end_time: 新結束時間 (選填)
        location: 新地點 (選填)
        description: 新描述 (選填)
    
    Returns:
        更新結果
    """
    if event_id not in CALENDAR_DATABASE:
        return {
            "success": False,
            "message": f"找不到事件 {event_id}"
        }
    
    event = CALENDAR_DATABASE[event_id]
    
    if title:
        event["title"] = title
    if date:
        event["date"] = date
    if start_time:
        event["start_time"] = start_time
    if end_time:
        event["end_time"] = end_time
    if location is not None:
        event["location"] = location
    if description is not None:
        event["description"] = description
    
    event["updated_at"] = datetime.now().isoformat()
    
    return {
        "success": True,
        "event_id": event_id,
        "message": f"已更新事件「{event['title']}」"
    }


def delete_event(event_id: str) -> Dict:
    """
    刪除日程事件
    
    Args:
        event_id: 事件 ID
    
    Returns:
        刪除結果
    """
    if event_id not in CALENDAR_DATABASE:
        return {
            "success": False,
            "message": f"找不到事件 {event_id}"
        }
    
    event = CALENDAR_DATABASE.pop(event_id)
    
    return {
        "success": True,
        "message": f"已刪除事件「{event['title']}」"
    }


def get_today_schedule() -> Dict:
    """
    取得今日日程
    
    Returns:
        今日所有事件
    """
    today = datetime.now().strftime("%Y-%m-%d")
    return query_events(date=today)


def check_time_conflict(date: str, start_time: str, end_time: str) -> Dict:
    """
    檢查時間衝突
    
    Args:
        date: 日期
        start_time: 開始時間
        end_time: 結束時間
    
    Returns:
        衝突檢查結果
    """
    conflicts = []
    
    for event in CALENDAR_DATABASE.values():
        if event["date"] != date:
            continue
        
        # 檢查時間重疊
        evt_start = event["start_time"]
        evt_end = event["end_time"]
        
        if not (end_time <= evt_start or start_time >= evt_end):
            conflicts.append({
                "event_id": event["id"],
                "title": event["title"],
                "time": f"{evt_start}-{evt_end}"
            })
    
    return {
        "has_conflict": len(conflicts) > 0,
        "conflicts": conflicts
    }