from DataLayer.db import db

class Bin(db.Model):
    __tablename__ = 'bins'
    id = db.Column(db.String(50), primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "location": self.location,
            "address": self.address
        }

    @classmethod
    def create(cls, id, location, address):
        bin_instance = cls(id=id, location=location, address=address)
        db.session.add(bin_instance)
        db.session.commit()
        return bin_instance

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)

    def update(self, location=None, address=None):
        if location is not None:
            self.location = location
        if address is not None:
            self.address = address
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()