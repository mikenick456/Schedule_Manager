#!/bin/bash

echo "============================================"
echo "  Smart Schedule Manager"
echo "  智慧日程與任務管理助手 啟動中..."
echo "============================================"

# 檢查 .env 檔案是否存在
if [ ! -f ".env" ]; then
    echo ""
    echo "[警告] 找不到 .env 檔案！"
    echo "請複製 env.template 為 .env 並填入 GOOGLE_API_KEY"
    echo ""
    exit 1
fi

# 檢查 Python 環境
if ! command -v python3 &> /dev/null; then
    echo ""
    echo "[錯誤] 找不到 Python！請先安裝 Python 3.10+"
    echo ""
    exit 1
fi

echo ""
echo "[1/2] 安裝相依套件..."
pip install -r requirements.txt -q

echo ""
echo "[2/2] 啟動主程式..."
echo ""
echo "============================================"
echo "  服務已啟動！"
echo "============================================"
echo ""

python3 main.py

