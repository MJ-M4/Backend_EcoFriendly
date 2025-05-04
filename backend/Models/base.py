from abc import ABC, abstractmethod

class BaseModel(ABC):
    """Simple base so every model returns dict."""
    @abstractmethod
    def to_dict(self) -> dict: ...