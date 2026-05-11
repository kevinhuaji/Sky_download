import os
import json
import requests
from datetime import datetime

# 強制從環境變數 (GitHub Secrets) 獲取敏感/配置資訊
API_URL = os.environ.get('API_URL')
PKG_NAME = os.environ.get('PKG_NAME')

def fetch_data():
    if not API_URL or not PKG_NAME:
        print("錯誤：未設置 API_URL 或 PKG_NAME 環境變數。")
        return

    # 模擬抓取 JSON 的 API 請求標頭
    headers = {
        "User-Agent": "ProxyPin/1.2.1",
        "Accept": "*/*",
        "Content-Type": "application/json"
    }
    
    payload = {
        "pkgName": PKG_NAME,
        "zone": "",
        "locale": "zh"
    }
    
    try:
        print("正在請求華為商店 API 獲取最新資訊...")
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        
        # 解析需要的資料
        app_info = data.get('appInfo', {})
        down_url = app_info.get('downUrl')
        version = app_info.get('version')
        
        if down_url:
            update_history(version, down_url)
        else:
            print("未能取得 downUrl 欄位。")
            
    except Exception as e:
        print(f"請求 API 發生錯誤: {e}")

def update_history(version, down_url):
    history_file = 'history.json'
    history = []
    
    # 讀取現有歷史紀錄
    if os.path.exists(history_file):
        with open(history_file, 'r', encoding='utf-8') as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError:
                history = []
                
    # 準備新紀錄
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_record = {
        "timestamp": timestamp,
        "version": version,
        "downUrl": down_url
    }
    
    # 檢查最後一筆紀錄是否與當前取得的相同，不同才寫入
    if not history or history[-1].get('downUrl') != down_url:
        history.append(new_record)
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=4, ensure_ascii=False)
        print(f"成功更新 JSON，寫入版本: {version}")
        print(f"提取到的下載連結: {down_url}")
    else:
        print("下載連結未更新，略過寫入。")

if __name__ == "__main__":
    fetch_data()
      
