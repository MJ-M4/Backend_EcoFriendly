from DataLayer.db import db
from datetime import datetime

class Shift(db.Model):
    __tablename__ = 'shifts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    worker_id = db.Column(db.Integer, db.ForeignKey('workers.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
<<<<<<< HEAD
    location = db.Column(db.String(100))
    worker = db.relationship('Worker', backref='shifts')

    
=======
    location = db.Column(db.String(100), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "worker_id": self.worker_id,
            "date": self.date.isoformat() if self.date else None,
            "start_time": self.start_time.strftime("%H:%M:%S") if self.start_time else None,
            "end_time": self.end_time.strftime("%H:%M:%S") if self.end_time else None,
            "location": self.location
        }

    @classmethod
    def create(cls, worker_id, date, start_time, end_time, location):
        shift = cls(
            worker_id=worker_id,
            date=datetime.fromisoformat(date).date(),
            start_time=datetime.strptime(start_time, "%H:%M").time(),
            end_time=datetime.strptime(end_time, "%H:%M").time(),
            location=location
        )
        db.session.add(shift)
        db.session.commit()
        return shift

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)

    def update(self, worker_id=None, date=None, start_time=None, end_time=None, location=None):
        if worker_id is not None:
            self.worker_id = worker_id
        if date is not None:
            self.date = datetime.fromisoformat(date).date()
        if start_time is not None:
            self.start_time = datetime.strptime(start_time, "%H:%M").time()
        if end_time is not None:
            self.end_time = datetime.strptime(end_time, "%H:%M").time()
        if location is not None:
            self.location = location
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
>>>>>>> ab7f7c8ba7f410c413fa04b99c8c91ca90267f03
