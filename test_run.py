import sys
import traceback
from app import create_app

if __name__ == '__main__':
    print("=== 初始化測試開始 ===")
    try:
        app = create_app()
        print("[Pass] Flask app 建立成功並初始化了資料庫")
        
        client = app.test_client()
        print("[Test] 試圖訪問首頁 / ...")
        response = client.get('/')
        print(f"Status Code: {response.status_code}")
        
    except Exception as e:
        print("\n[Failed] 發生錯誤：")
        print(f"{type(e).__name__}: {e}")
        # traceback.print_exc()
