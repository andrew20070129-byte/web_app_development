import os
from flask import Flask
from app.models import db
from app.routes import register_routes
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 確保 instance 資料夾存在，用於存放 SQLite database.db
    os.makedirs(app.instance_path, exist_ok=True)

    # 初始化資料庫
    db.init_app(app)

    # 建立所有資料表 (若尚未建立的話)
    with app.app_context():
        db.create_all()

    # 註冊所有的 Blueprint 路由
    register_routes(app)

    return app
