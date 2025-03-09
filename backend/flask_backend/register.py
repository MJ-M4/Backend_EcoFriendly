from werkzeug.security import generate_password_hash
from flask_backend.model import User, db
from datetime import datetime

class Register:
    def __init__(self, identity, password, role='worker', worker_type=None, phone=None, location=None, name=None, joining_date=None):
        self.identity = identity
        self.password = password
        self.role = role
        self.worker_type = worker_type
        self.phone = phone
        self.location = location
        self.name = name
        self.joining_date = joining_date

    def validate_input(self):
        if not self.identity or not self.password:
            return {"error": "ID and password are required"}, 400
        return None

    def check_existing_user(self):
        existing_user = User.query.filter_by(identity=self.identity).first()
        if existing_user:
            return {"error": "User ID already exists"}, 400
        return None

    def register_user(self):
        validation_error = self.validate_input()
        if validation_error:
            return validation_error

        existing_user_error = self.check_existing_user()
        if existing_user_error:
            return existing_user_error

        try:
            hashed_password = generate_password_hash(self.password)
            # Parse joining_date if provided
            joining_date_obj = None
            if self.joining_date:
                try:
                    joining_date_obj = datetime.strptime(self.joining_date, "%Y-%m-%d").date()
                except ValueError:
                    return {"error": "Invalid date format, use YYYY-MM-DD"}, 400

            new_user = User(
                identity=self.identity,
                password=hashed_password,
                role=self.role,
                worker_type=self.worker_type,
                phone=self.phone,
                location=self.location,
                name=self.name,
                joining_date=joining_date_obj
            )
            db.session.add(new_user)
            db.session.commit()
            return {"message": "Registration successful!"}, 201
        except Exception as e:
            db.session.rollback()
            return {"error": "Error during registration", "details": str(e)}, 500