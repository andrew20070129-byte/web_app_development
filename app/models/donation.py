from datetime import datetime
from . import db

class Donation(db.Model):
    __tablename__ = 'donations'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String, nullable=False, default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def create(cls, user_id, amount, status='pending'):
        """
        新增一筆香油錢捐獻紀錄。
        :param user_id: 捐獻的使用者 ID
        :param amount: 捐款金額
        :param status: 訂單狀態 (預設 pending)
        :return: Donation 物件或 None
        """
        try:
            new_donation = cls(user_id=user_id, amount=amount, status=status)
            db.session.add(new_donation)
            db.session.commit()
            return new_donation
        except Exception as e:
            db.session.rollback()
            print(f"Error creating donation: {e}")
            return None

    @classmethod
    def get_all(cls):
        """
        取得所有的捐獻明細紀錄。
        """
        try:
            return cls.query.all()
        except Exception as e:
            print(f"Error getting all donations: {e}")
            return []

    @classmethod
    def get_by_id(cls, donation_id):
        """
        依據 id 取得特定捐獻紀錄。
        """
        try:
            return cls.query.get(donation_id)
        except Exception as e:
            print(f"Error getting donation by id: {e}")
            return None
        
    @classmethod
    def get_by_user_id(cls, user_id):
        """
        取得某位特定使用者過去所有的捐獻紀錄，依照時間從新到舊排序。
        :param user_id: 該名使用者 ID
        """
        try:
            return cls.query.filter_by(user_id=user_id).order_by(cls.created_at.desc()).all()
        except Exception as e:
            print(f"Error getting user donations: {e}")
            return []

    def update(self, **kwargs):
        """
        更新此筆捐款紀錄 (例如變更為 status='completed')。
        """
        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
            db.session.commit()
            return self
        except Exception as e:
            db.session.rollback()
            print(f"Error updating donation: {e}")
            return None

    def delete(self):
        """
        刪除此筆捐款紀錄。
        """
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting donation: {e}")
            return False
