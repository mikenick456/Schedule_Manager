"""任務管理工具函式
Course Concept: Day 2 - FunctionTool
"""
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from enum import Enum
import uuid

# 任務優先級
class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

# 任務狀態
class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

# 模擬任務資料庫
TASKS_DATABASE = {}

# 初始化示範資料
def _init_sample_tasks():
    today = datetime.now().strftime("%Y-%m-%d")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    next_week = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    
    TASKS_DATABASE["TSK-001"] = {
        "id": "TSK-001",
        "title": "完成專案報告",
        "description": "撰寫 Q4 專案進度報告",
        "priority": "high",
        "status": "in_progress",
        "due_date": today,
        "estimated_hours": 3,
        "tags": ["工作", "報告"]
    }
    TASKS_DATABASE["TSK-002"] = {
        "id": "TSK-002",
        "title": "回覆客戶郵件",
        "description": "回覆客戶關於產品功能的詢問",
        "priority": "medium",
        "status": "todo",
        "due_date": today,
        "estimated_hours": 1,
        "tags": ["工作", "溝通"]
    }
    TASKS_DATABASE["TSK-003"] = {
        "id": "TSK-003",
        "title": "準備簡報資料",
        "description": "準備下週客戶拜訪的簡報",
        "priority": "high",
        "status": "todo",
        "due_date": tomorrow,
        "estimated_hours": 4,
        "tags": ["工作", "簡報"]
    }
    TASKS_DATABASE["TSK-004"] = {
        "id": "TSK-004",
        "title": "學習新技術",
        "description": "研究 AI Agent 開發框架",
        "priority": "low",
        "status": "todo",
        "due_date": next_week,
        "estimated_hours": 8,
        "tags": ["學習", "技術"]
    }

_init_sample_tasks()


def create_task(
    title: str,
    description: str = "",
    priority: str = "medium",
    due_date: Optional[str] = None,
    estimated_hours: float = 1.0,
    tags: List[str] = None
) -> Dict:
    """
    建立新任務
    
    Args:
        title: 任務標題
        description: 任務描述 (選填)
        priority: 優先級 (low/medium/high/urgent)，預設 medium
        due_date: 截止日期 (格式: YYYY-MM-DD)
        estimated_hours: 預估工時，預設 1 小時
        tags: 標籤列表
    
    Returns:
        新建立的任務資訊
    """
    task_id = f"TSK-{uuid.uuid4().hex[:6].upper()}"
    
    task = {
        "id": task_id,
        "title": title,
        "description": description,
        "priority": priority,
        "status": "todo",
        "due_date": due_date,
        "estimated_hours": estimated_hours,
        "tags": tags or [],
        "created_at": datetime.now().isoformat()
    }
    
    TASKS_DATABASE[task_id] = task
    
    priority_emoji = {"low": "🟢", "medium": "🟡", "high": "🟠", "urgent": "🔴"}
    
    return {
        "success": True,
        "task_id": task_id,
        "message": f"已建立任務 {priority_emoji.get(priority, '')}「{title}」"
    }


def list_tasks(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    due_date: Optional[str] = None,
    include_completed: bool = False
) -> Dict:
    """
    列出任務清單
    
    Args:
        status: 篩選狀態 (todo/in_progress/completed/cancelled)
        priority: 篩選優先級 (low/medium/high/urgent)
        due_date: 篩選截止日期
        include_completed: 是否包含已完成任務，預設 False
    
    Returns:
        任務清單
    """
    results = []
    
    for task in TASKS_DATABASE.values():
        # 預設不顯示已完成和已取消的任務
        if not include_completed and task["status"] in ["completed", "cancelled"]:
            continue
        
        if status and task["status"] != status:
            continue
        if priority and task["priority"] != priority:
            continue
        if due_date and task["due_date"] != due_date:
            continue
        
        results.append(task)
    
    # 按優先級和截止日期排序
    priority_order = {"urgent": 0, "high": 1, "medium": 2, "low": 3}
    results.sort(key=lambda x: (
        priority_order.get(x["priority"], 4),
        x["due_date"] or "9999-99-99"
    ))
    
    return {
        "success": True,
        "count": len(results),
        "tasks": results
    }


def update_task(
    task_id: str,
    title: Optional[str] = None,
    description: Optional[str] = None,
    priority: Optional[str] = None,
    status: Optional[str] = None,
    due_date: Optional[str] = None,
    estimated_hours: Optional[float] = None
) -> Dict:
    """
    更新任務
    
    Args:
        task_id: 任務 ID
        title: 新標題 (選填)
        description: 新描述 (選填)
        priority: 新優先級 (選填)
        status: 新狀態 (選填)
        due_date: 新截止日期 (選填)
        estimated_hours: 新預估工時 (選填)
    
    Returns:
        更新結果
    """
    if task_id not in TASKS_DATABASE:
        return {
            "success": False,
            "message": f"找不到任務 {task_id}"
        }
    
    task = TASKS_DATABASE[task_id]
    
    if title:
        task["title"] = title
    if description is not None:
        task["description"] = description
    if priority:
        task["priority"] = priority
    if status:
        task["status"] = status
        if status == "completed":
            task["completed_at"] = datetime.now().isoformat()
    if due_date:
        task["due_date"] = due_date
    if estimated_hours is not None:
        task["estimated_hours"] = estimated_hours
    
    task["updated_at"] = datetime.now().isoformat()
    
    return {
        "success": True,
        "task_id": task_id,
        "message": f"已更新任務「{task['title']}」"
    }


def complete_task(task_id: str) -> Dict:
    """
    標記任務為已完成
    
    Args:
        task_id: 任務 ID
    
    Returns:
        完成結果
    """
    return update_task(task_id, status="completed")


def delete_task(task_id: str) -> Dict:
    """
    刪除任務
    
    Args:
        task_id: 任務 ID
    
    Returns:
        刪除結果
    """
    if task_id not in TASKS_DATABASE:
        return {
            "success": False,
            "message": f"找不到任務 {task_id}"
        }
    
    task = TASKS_DATABASE.pop(task_id)
    
    return {
        "success": True,
        "message": f"已刪除任務「{task['title']}」"
    }


def get_task_statistics() -> Dict:
    """
    取得任務統計資訊
    
    Returns:
        任務統計資料 (供 CodeExecutor 分析使用)
    """
    stats = {
        "total": len(TASKS_DATABASE),
        "by_status": {"todo": 0, "in_progress": 0, "completed": 0, "cancelled": 0},
        "by_priority": {"low": 0, "medium": 0, "high": 0, "urgent": 0},
        "total_estimated_hours": 0,
        "overdue_count": 0
    }
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    for task in TASKS_DATABASE.values():
        stats["by_status"][task["status"]] = stats["by_status"].get(task["status"], 0) + 1
        stats["by_priority"][task["priority"]] = stats["by_priority"].get(task["priority"], 0) + 1
        stats["total_estimated_hours"] += task.get("estimated_hours", 0)
        
        # 檢查是否過期
        if task["due_date"] and task["due_date"] < today and task["status"] not in ["completed", "cancelled"]:
            stats["overdue_count"] += 1
    
    return stats


def get_tasks_for_analysis() -> List[Dict]:
    """
    取得任務清單供分析使用
    
    Returns:
        簡化的任務清單
    """
    return [
        {
            "id": t["id"],
            "title": t["title"],
            "priority": t["priority"],
            "status": t["status"],
            "due_date": t["due_date"],
            "estimated_hours": t.get("estimated_hours", 0)
        }
        for t in TASKS_DATABASE.values()
    ]