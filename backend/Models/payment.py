# backend/Models/payment.py
from Models.base_model import BaseModel
from DataLayer.payments_datalayer import PaymentsDataLayer

class Payment(BaseModel):
    def __init__(self):
        super().__init__()
        self.worker_id = None
        self.worker_name = None
        self.amount = None
        self.payment_date = None
        self.status = None
        self.notes = None

        self.dl = PaymentsDataLayer()

    def create_payment(self, data):
        """
        data keys: worker_id, worker_name, amount, payment_date, status, notes
        """
        new_id = self.dl.insert_payment(data)
        self.id = new_id
        self.worker_id = data['worker_id']
        self.worker_name = data['worker_name']
        self.amount = data['amount']
        self.payment_date = data['payment_date']
        self.status = data['status']
        self.notes = data['notes']
        return self

    def mark_as_paid(self, payment_id, new_date=None):
        """
        Mark payment as 'Paid'. Optionally update the payment_date to new_date.
        """
        self.dl.update_payment_status(payment_id, 'Paid', new_date)

    def get_all_payments(self):
        return self.dl.fetch_all_payments()

    def delete_payment(self, payment_id):
        self.dl.delete_payment(payment_id)

    def to_dict(self):
        return {
            'id': self.id,
            'worker_id': self.worker_id,
            'worker_name': self.worker_name,
            'amount': self.amount,
            'payment_date': self.payment_date,
            'status': self.status,
            'notes': self.notes
        }
