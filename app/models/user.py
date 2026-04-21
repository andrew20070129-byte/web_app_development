from datetime import datetime
from . import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 關聯設定
    fortune_results = db.relationship('FortuneResult', backref='user', lazy=True)
    donations = db.relationship('Donation', backref='user', lazy=True)

    @classmethod
    def create(cls, username, email, password_hash):
        """
        新增一名使用者。
        :param username: 使用者名稱
        :param email: 電子信箱
        :param password_hash: 加密後的密碼
        :return: 建立的 User 物件，若失敗則回傳 None
        """
        try:
            new_user = cls(username=username, email=email, password_hash=password_hash)
            db.session.add(new_user)
            db.session.commit()
            return new_user
        except Exception as e:
            db.session.rollback()
            print(f"Error creating user: {e}")
            return None

    @classmethod
    def get_all(cls):
        """
        取得所有使用者紀錄。
        :return: User 物件列表
        """
        try:
            return cls.query.all()
        except Exception as e:
            print(f"Error getting all users: {e}")
            return []

    @classmethod
    def get_by_id(cls, user_id):
        """
        依據 id 取得單筆使用者紀錄。
        :param user_id: 使用者 ID
        :return: User 物件 或 None
        """
        try:
            return cls.query.get(user_id)
        except Exception as e:
            print(f"Error getting user by id: {e}")
            return None
        
    @classmethod
    def get_by_username(cls, username):
        """
        依據 username 取得使用者。
        :param username: 使用者名稱
        :return: User 物件 或 None
        """
        try:
            return cls.query.filter_by(username=username).first()
        except Exception as e:
            print(f"Error getting user by username: {e}")
            return None
        
    @classmethod
    def get_by_email(cls, email):
        """
        依據 email 取得使用者。
        :param email: 電子信箱
        :return: User 物件 或 None
        """
        try:
            return cls.query.filter_by(email=email).first()
        except Exception as e:
            print(f"Error getting user by email: {e}")
            return None

    def update(self, **kwargs):
        """
        更新此使用者紀錄。
        :param kwargs: 欲更新的欄位與值
        :return: 更新後的 User 物件，失敗回傳 None
        """
        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
            db.session.commit()
            return self
        except Exception as e:
            db.session.rollback()
            print(f"Error updating user {self.id}: {e}")
            return None

    def delete(self):
        """
        刪除此使用者。
        :return: True 若成功，否則 False
        """
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting user {self.id}: {e}")
            return False
