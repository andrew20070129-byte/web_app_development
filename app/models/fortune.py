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
        new_fortune = cls(title=title, poem=poem, interpretation=interpretation)
        db.session.add(new_fortune)
        db.session.commit()
        return new_fortune

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, fortune_id):
        return cls.query.get(fortune_id)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class FortuneResult(db.Model):
    __tablename__ = 'fortune_results'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    fortune_id = db.Column(db.Integer, db.ForeignKey('fortunes.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def create(cls, user_id, fortune_id):
        new_result = cls(user_id=user_id, fortune_id=fortune_id)
        db.session.add(new_result)
        db.session.commit()
        return new_result

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, result_id):
        return cls.query.get(result_id)
        
    @classmethod
    def get_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
