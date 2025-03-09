from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    identity = db.Column(db.BigInteger, unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default='worker')
    worker_type = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(50), nullable=True)
    location = db.Column(db.String(100), nullable=True)

    # NEW columns for your Worker page:
    name = db.Column(db.String(100), nullable=True)
    joining_date = db.Column(db.Date, nullable=True)

    def __repr__(self):
        return f"<User {self.identity} - {self.role}>"

def hash_existing_passwords():
    """Hash any plaintext passwords in the DB if length < 20."""
    users = User.query.all()
    for user in users:
        if len(user.password) < 20:
            user.password = generate_password_hash(user.password)
            db.session.add(user)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error hashing passwords: {e}")
