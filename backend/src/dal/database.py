"""
Creates the SQLAlchemy engine & session factory.

• Reads the stage (local / test / prod) from env.STAGE.
• No numeric status codes anywhere.
"""
from contextlib import contextmanager
from configparser import ConfigParser
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

_cfg = ConfigParser()
_cfg.read(os.getenv("CONFIG_PATH", "config.ini"))
_STAGE = os.getenv("STAGE", "local")
DB_URL = _cfg.get(_STAGE, "DB_URL")

# single engine for the whole process
ENGINE = create_engine(DB_URL, pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(bind=ENGINE, autoflush=False, autocommit=False, future=True)


@contextmanager
def get_session() -> Session:
    """Yield a DB session and ensure close/rollback."""
    session: Session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
