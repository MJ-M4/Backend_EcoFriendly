from DataLayer.db import db
from Models.User import User  # Import User model

class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Link to Users
    identity = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    location = db.Column(db.String(100), nullable=True)
    joining_date = db.Column(db.Date, nullable=True)
    worker_type = db.Column(db.Enum('Driver', 'Cleaner', 'Maintenance Worker'), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "identity": self.identity,
            "name": self.name,
            "phone": self.phone,
            "location": self.location,
            "joining_date": self.joining_date.isoformat() if self.joining_date else None,
            "worker_type": self.worker_type
        }

    @classmethod
    def create(cls, identity, name, phone, location, joining_date, worker_type, password):
        # Create a User entry with identity as username, role as 'worker'
        user = User.create(
            username=identity,  # Use identity as username
            role='worker',
            password=password,
            worker_type=worker_type
        )
        
        # Create the Employee entry linked to the User
        employee = cls(
            user_id=user.id,
            identity=identity,
            name=name,
            phone=phone,
            location=location,
            joining_date=joining_date,
            worker_type=worker_type
        )
        db.session.add(employee)
        db.session.commit()
        return employee

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)

    def update(self, identity=None, name=None, phone=None, location=None, joining_date=None, worker_type=None):
        if identity is not None:
            self.identity = identity
        if name is not None:
            self.name = name
        if phone is not None:
            self.phone = phone
        if location is not None:
            self.location = location
        if joining_date is not None:
            self.joining_date = joining_date
        if worker_type is not None:
            self.worker_type = worker_type
        db.session.commit()

    def delete(self):
        # Optionally delete the linked User entry as well (cascade delete could handle this)
        user = User.query.get(self.user_id)
        if user:
            db.session.delete(user)
        db.session.delete(self)
        db.session.commit()