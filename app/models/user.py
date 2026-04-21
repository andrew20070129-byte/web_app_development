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
        new_user = cls(username=username, email=email, password_hash=password_hash)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.get(user_id)
        
    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
        
    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
