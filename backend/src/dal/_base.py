# src/dal/_base.py (tiny internal util)
from pydantic import BaseModel
from sqlalchemy.engine import Row

def _row_to_model(row: Row, model_cls: type[BaseModel]) -> BaseModel:
    """Convert SQLAlchemy Core Row → Pydantic model."""
    return model_cls.model_validate(row._mapping)
