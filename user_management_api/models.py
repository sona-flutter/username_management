from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), nullable=False)
    user_nick_name = db.Column(db.String(50))
    phone_no = db.Column(db.String(20))
    user_address = db.Column(db.Text)
    user_email = db.Column(db.String(255), unique=True, nullable=False)
    user_bio = db.Column(db.Text)
    user_date_of_birth = db.Column(db.Date)
    user_age = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
