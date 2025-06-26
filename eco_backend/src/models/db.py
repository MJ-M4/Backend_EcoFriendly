from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.config_loader import load_config

config = load_config()["mysql"]
DB_URL = f"mysql+mysqlconnector://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"

engine = create_engine(
    DB_URL,
    pool_pre_ping=True,
    pool_size=10,       # Increased pool size for simulators + handlers
    max_overflow=5,     # Allow extra overflow if needed
    pool_timeout=10     # Fail fast if connections are stuck
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()