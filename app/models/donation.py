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
        new_donation = cls(user_id=user_id, amount=amount, status=status)
        db.session.add(new_donation)
        db.session.commit()
        return new_donation

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, donation_id):
        return cls.query.get(donation_id)
        
    @classmethod
    def get_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).order_by(cls.created_at.desc()).all()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
