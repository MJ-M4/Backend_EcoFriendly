from DataLayer.db import db

class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    worker_id = db.Column(db.Integer, db.ForeignKey('workers.id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.Enum('Paid', 'Pending'), nullable=False)
    notes = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "worker_id": self.worker_id,
            "amount": float(self.amount),
            "payment_date": self.payment_date.isoformat() if self.payment_date else None,
            "status": self.status,
            "notes": self.notes
        }

    @classmethod
    def create(cls, worker_id, amount, payment_date, status, notes=None):
        payment = cls(worker_id=worker_id, amount=amount, payment_date=payment_date, status=status, notes=notes)
        db.session.add(payment)
        db.session.commit()
        return payment

    @classmethod
    def get_all(cls):
        return cls.query.all()