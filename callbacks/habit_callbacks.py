"""習慣學習回調
Course Concept: Day 3 - Callbacks, Memory Service
"""
from datetime import datetime


async def learn_user_habits(callback_context):
    """
    從用戶行為中學習習慣偏好
    
    Course Concept: Day 3 - after_agent_callback
    
    分析用戶的:
    - 常用任務時段
    - 偏好的優先級設定
    - 常見任務類型
    """
    try:
        session = callback_context._invocation_context.session
        state = session.state
        
        # 記錄當前時間（用於分析活躍時段）
        current_hour = datetime.now().hour
        
        # 更新活躍時段統計
        active_hours = state.get("habit:active_hours", {})
        hour_key = str(current_hour)
        active_hours[hour_key] = active_hours.get(hour_key, 0) + 1
        state["habit:active_hours"] = active_hours
        
        # 儲存到長期記憶
        memory_service = callback_context._invocation_context.memory_service
        if memory_service:
            await memory_service.add_session_to_memory(session)
            print(f"[Habit] 已學習用戶習慣並儲存到長期記憶")
            
    except Exception as e:
        print(f"[Habit] 學習失敗: {e}")


def get_personalized_suggestions(state: dict) -> list:
    """
    根據用戶習慣提供個人化建議
    
    Args:
        state: Session state
    
    Returns:
        個人化建議清單
    """
    suggestions = []
    
    # 分析活躍時段
    active_hours = state.get("habit:active_hours", {})
    if active_hours:
        # 找出最活躍的時段
        peak_hour = max(active_hours.keys(), key=lambda k: active_hours[k])
        suggestions.append(f"您通常在 {peak_hour}:00 最活躍，建議在此時段處理重要任務")
    
    return suggestions