from DataLayer.db import db

class Vehicle(db.Model):
    __tablename__ = 'vehicles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(50), nullable=False)
    license_plate = db.Column(db.String(10), unique=True, nullable=False)
    status = db.Column(db.Enum('Available', 'In Use', 'Under Maintenance'), default='Available')
    last_maintenance = db.Column(db.Date, nullable=True)
    location = db.Column(db.String(100), nullable=True)  

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "license_plate": self.license_plate,
            "status": self.status,
            "last_maintenance": self.last_maintenance.isoformat() if self.last_maintenance else None,
            "location": self.location 
        }

    @classmethod
    def create(cls, type, license_plate, status="Available", last_maintenance=None, location=None):
        vehicle = cls(type=type, license_plate=license_plate, status=status, last_maintenance=last_maintenance, location=location)
        db.session.add(vehicle)
        db.session.commit()
        return vehicle

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)

    def update(self, type=None, license_plate=None, status=None, last_maintenance=None, location=None):
        if type is not None:
            self.type = type
        if license_plate is not None:
            self.license_plate = license_plate
        if status is not None:
            self.status = status
        if last_maintenance is not None:
            self.last_maintenance = last_maintenance
        if location is not None:
            self.location = location
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()