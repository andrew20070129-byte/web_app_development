import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # 預設開發環境密鑰，如果沒有設定環境變數就會用這個
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev_secret_key_here'
    
    # SQLite 資料庫設定，預設放在 instance 目錄下
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'database.db')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
