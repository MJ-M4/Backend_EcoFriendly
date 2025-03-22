from DataLayer.db import db

class Bin(db.Model):
    __tablename__ = 'bins'
    id = db.Column(db.String(50), primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Enum('Full', 'Empty', 'Near Full'), default='Empty')
    fill_level = db.Column(db.Float, default=0.0)
    last_updated = db.Column(db.DateTime, default=db.func.current_timestamp())
    assigned_worker_id = db.Column(db.Integer, db.ForeignKey('workers.id'), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "location": self.location,
            "status": self.status,
            "fill_level": self.fill_level,
            "last_updated": self.last_updated.isoformat() if self.last_updated else None,
            "assigned_worker_id": self.assigned_worker_id
        }

    @classmethod
    def create(cls, id, location, status="Empty", fill_level=0.0, assigned_worker_id=None):
        bin_instance = cls(id=id, location=location, status=status, fill_level=fill_level, assigned_worker_id=assigned_worker_id)
        db.session.add(bin_instance)
        db.session.commit()
        return bin_instance

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)

    def update(self, location=None, status=None, fill_level=None, assigned_worker_id=None):
        if location is not None:
            self.location = location
        if status is not None:
            self.status = status
        if fill_level is not None:
            self.fill_level = fill_level
        if assigned_worker_id is not None:
            self.assigned_worker_id = assigned_worker_id
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()