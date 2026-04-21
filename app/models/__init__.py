from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# 方便套件一次匯入所有 Models 與啟動機制
from .user import User
from .fortune import Fortune, FortuneResult
from .donation import Donation
