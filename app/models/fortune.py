from datetime import datetime
from . import db

class Fortune(db.Model):
    __tablename__ = 'fortunes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    poem = db.Column(db.Text, nullable=False)
    interpretation = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 關聯設定
    results = db.relationship('FortuneResult', backref='fortune', lazy=True)

    @classmethod
    def create(cls, title, poem, interpretation):
        """
        新增一首籤詩。
        :param title: 籤詩標題
        :param poem: 籤詩內文
        :param interpretation: 籤詩解釋
        :return: Fortune 物件或 None
        """
        try:
            new_fortune = cls(title=title, poem=poem, interpretation=interpretation)
            db.session.add(new_fortune)
            db.session.commit()
            return new_fortune
        except Exception as e:
            db.session.rollback()
            print(f"Error creating fortune: {e}")
            return None

    @classmethod
    def get_all(cls):
        """
        取得資料庫內所有籤詩。
        :return: Fortune 串列列表
        """
        try:
            return cls.query.all()
        except Exception as e:
            print(f"Error getting all fortunes: {e}")
            return []

    @classmethod
    def get_by_id(cls, fortune_id):
        """
        依據 ID 取得特定籤詩。
        :param fortune_id: 籤詩 ID
        :return: Fortune 物件或 None
        """
        try:
            return cls.query.get(fortune_id)
        except Exception as e:
            print(f"Error getting fortune by id: {e}")
            return None

    def update(self, **kwargs):
        """
        更新特定籤詩內容。
        """
        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
            db.session.commit()
            return self
        except Exception as e:
            db.session.rollback()
            print(f"Error updating fortune: {e}")
            return None

    def delete(self):
        """
        刪除該首籤詩。
        """
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting fortune: {e}")
            return False


class FortuneResult(db.Model):
    __tablename__ = 'fortune_results'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    fortune_id = db.Column(db.Integer, db.ForeignKey('fortunes.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def create(cls, user_id, fortune_id):
        """
        新增一筆使用者的抽籤紀錄。
        :param user_id: 使用者 ID
        :param fortune_id: 抽中的籤詩 ID
        :return: FortuneResult 物件或 None
        """
        try:
            new_result = cls(user_id=user_id, fortune_id=fortune_id)
            db.session.add(new_result)
            db.session.commit()
            return new_result
        except Exception as e:
            db.session.rollback()
            print(f"Error creating fortune result: {e}")
            return None

    @classmethod
    def get_all(cls):
        """
        取得所有的歷史抽籤紀錄。
        """
        try:
            return cls.query.all()
        except Exception as e:
            print(f"Error getting all fortune results: {e}")
            return []

    @classmethod
    def get_by_id(cls, result_id):
        """
        依據 ID 取得特定的歷史抽籤紀錄。
        """
        try:
            return cls.query.get(result_id)
        except Exception as e:
            print(f"Error getting fortune result by id: {e}")
            return None
        
    @classmethod
    def get_by_user_id(cls, user_id):
        """
        取得某特定使用者的所有儲存抽籤紀錄 (時間由新到舊)。
        """
        try:
            return cls.query.filter_by(user_id=user_id).order_by(cls.created_at.desc()).all()
        except Exception as e:
            print(f"Error getting user fortune results: {e}")
            return []

    def update(self, **kwargs):
        """
        更新該筆抽籤紀錄屬性。
        """
        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
            db.session.commit()
            return self
        except Exception as e:
            db.session.rollback()
            print(f"Error updating fortune result: {e}")
            return None

    def delete(self):
        """
        刪除該筆抽籤紀錄。
        """
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting fortune result: {e}")
            return False
