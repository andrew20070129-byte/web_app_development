from app import create_app

app = create_app()

if __name__ == '__main__':
    # 啟動 Flask 開發伺服器，預設開啟 debug 模式
    app.run(debug=True)
