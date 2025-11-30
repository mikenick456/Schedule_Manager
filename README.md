# 智慧日程管理系統

這是一個使用 Google ADK (Agent Development Kit) 框架開發的 AI 代理展示專案，旨在協助用戶管理日程、任務和提醒事項，提供智慧化的時間管理與規劃建議。

## 專案架構

本專案採用多代理 (Multi-Agent) 架構，由一個主要協調代理整合多個功能性代理來完成任務：

1.  **協調專員 (Schedule Coordinator)**:
    *   使用者直接互動的主要代理。
    *   負責理解使用者需求，並將其分派給對應的專業代理。
    *   整合每日規劃流水線，提供完整的日程管理服務。
    *   由 `main.py` 啟動。

2.  **日程專員 (Calendar Agent)**:
    *   專門處理日程相關的查詢與管理。
    *   負責查詢、建立、更新和刪除日程事件。
    *   由 `agents/calendar_agent.py` 實現。

3.  **任務專員 (Task Agent)**:
    *   專門處理任務管理相關功能。
    *   負責任務的建立、追蹤、更新、完成和統計分析。
    *   整合 CodeExecutor 代理，可執行 Python 代碼進行複雜的任務分析。
    *   由 `agents/task_agent.py` 實現。

4.  **提醒專員 (Reminder Agent)**:
    *   專門處理提醒事項的管理。
    *   負責建立、查詢、更新和刪除提醒。
    *   由 `agents/reminder_agent.py` 實現。

5.  **分析專員 (Analysis Agent)**:
    *   整合日程、任務、提醒資訊並提供每日摘要和建議。
    *   分析時間衝突、優先級排序等。
    *   由 `main.py` 中的 `analysis_agent` 實現。

6.  **優化專員 (Optimization Loop)**:
    *   使用 LoopAgent 迭代優化每日排程。
    *   根據用戶反饋持續改進規劃建議。
    *   由 `workflows/optimize_workflow.py` 實現。

## 技術棧

*   **AI 代理框架**: `google-adk`
*   **語言模型**: `google-genai` (Gemini)
*   **環境變數管理**: `python-dotenv`
*   **日誌記錄**: `LoggingPlugin`
*   **記憶服務**: `InMemoryMemoryService` (支援用戶習慣學習)
*   **會話管理**: `InMemorySessionService`

## 核心功能

*   **並行查詢**: 使用 ParallelAgent 同時查詢日程、任務、提醒，提升查詢效率。
*   **每日規劃流水線**: SequentialAgent 整合查詢 → 分析 → 優化流程。
*   **任務統計分析**: 透過 CodeExecutor 執行 Python 代碼進行複雜的數據分析。
*   **用戶習慣學習**: 使用 Callbacks 自動學習用戶偏好，提供個人化建議。
*   **上下文壓縮**: 支援 EventsCompactionConfig，優化長期對話的記憶管理。

## 如何運行

請遵循以下步驟來啟動系統。

### 1. 前置作業

*   確認您已安裝 Python 3.9 或更高版本。
*   建議建立並啟用虛擬環境：
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # on Windows, use `.venv\Scripts\activate`
    ```

### 2. 安裝依賴

在專案根目錄下，執行以下指令：

```bash
pip install -r requirements.txt
```

### 3. 設定環境變數

複製範例環境變數檔案，並填寫您的 Google Gemini API 金鑰。

```bash
# 在 Linux 或 macOS 上
cp env.template .env

# 在 Windows 上
copy env.template .env
```

接著，編輯 `.env` 檔案，將 `your_gemini_api_key_here` 替換成您自己的金鑰。

```
GOOGLE_API_KEY=your_gemini_api_key_here
COMPACTION_INTERVAL=5
OVERLAP_SIZE=2
WORK_START_HOUR=9
WORK_END_HOUR=18
MAX_OPTIMIZATION_ITERATIONS=3
LOG_LEVEL=INFO
```

### 4. 啟動系統

您可以使用以下兩種方式之一來啟動系統：

**方式一：使用啟動腳本**

*   **Windows**:
    ```bash
    start.bat
    ```

*   **Linux/macOS**:
    ```bash
    chmod +x start.sh
    ./start.sh
    ```

**方式二：直接執行主程式**

```bash
python main.py
```

### 5. 開始互動

當系統成功啟動後，您可以在終端機中開始與智慧日程管理系統進行對話。

**常用指令範例**:
*   `今天有什麼行程？` - 查詢今日日程
*   `幫我新增一個會議` - 建立新日程
*   `列出所有待辦任務` - 查詢任務清單
*   `分析我的任務統計` - 進行任務數據分析
*   `設定明天早上的提醒` - 建立提醒事項
*   `進行今日規劃` - 取得完整的每日規劃建議

輸入 `exit`、`quit`、`結束` 或 `離開` 來結束對話。
