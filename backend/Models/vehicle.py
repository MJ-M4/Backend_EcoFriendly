# backend/Models/vehicle.py

from Models.base_model import BaseModel
from DataLayer.vehicles_datalayer import VehiclesDataLayer

class Vehicle(BaseModel):
    def __init__(self):
        super().__init__()
        self.type = None
        self.license_plate = None
        self.status = None
        self.location = None
        self.last_maintenance = None

        self.dl = VehiclesDataLayer()

    def create_vehicle(self, data):
        # e.g. you could check if data['last_maintenance'] is future date, etc.

        new_id = self.dl.insert_vehicle(data)
        self.id = new_id
        self.type = data['type']
        self.license_plate = data['license_plate']
        self.status = data['status']
        self.location = data['location']
        self.last_maintenance = data['last_maintenance']
        return self

    def get_all_vehicles(self):
        return self.dl.fetch_all_vehicles()

    def delete_vehicle(self, vehicle_id):
        self.dl.delete_vehicle(vehicle_id)

    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'license_plate': self.license_plate,
            'status': self.status,
            'location': self.location,
            'last_maintenance': self.last_maintenance,
        }
