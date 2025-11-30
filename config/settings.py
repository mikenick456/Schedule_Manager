"""專案配置設定
Course Concept: 集中管理環境變數和配置
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """應用程式配置類"""
    
    # API Keys
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    
    # Model Configuration
    DEFAULT_MODEL = "gemini-2.5-flash-lite"
    
    # Context Compaction 設定
    COMPACTION_INTERVAL = int(os.getenv("COMPACTION_INTERVAL", 5))
    OVERLAP_SIZE = int(os.getenv("OVERLAP_SIZE", 2))
    
    # 工作時間設定
    WORK_START_HOUR = int(os.getenv("WORK_START_HOUR", 9))
    WORK_END_HOUR = int(os.getenv("WORK_END_HOUR", 18))
    
    # LoopAgent 設定
    MAX_OPTIMIZATION_ITERATIONS = int(os.getenv("MAX_OPTIMIZATION_ITERATIONS", 3))
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()

