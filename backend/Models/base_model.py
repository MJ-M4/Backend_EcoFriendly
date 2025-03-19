# backend/Models/base_model.py
from abc import ABC, abstractmethod

class BaseModel(ABC):
    def __init__(self):
        self._id = None

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @abstractmethod
    def to_dict(self):
        """Convert the model to a dictionary for JSON serialization."""
        pass