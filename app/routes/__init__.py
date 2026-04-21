from flask import Blueprint

# 定義藍圖 (Blueprint)，方便依照模組拆分路由邏輯
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
main_bp = Blueprint('main', __name__)
profile_bp = Blueprint('profile', __name__)

# 延遲匯入路由處理函式以避免循環依賴
from . import auth, main, profile

def register_routes(app):
    """
    提供給內部工廠函式呼叫，將所有的 Blueprint 註冊進 Flask 應用程式
    """
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(profile_bp)
