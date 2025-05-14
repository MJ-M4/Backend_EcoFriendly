from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from pathlib import Path
import sys, os

# add backend/src to path so models can be imported
sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))

from models import role, user, bin, bin_reading, vehicle, shift, payroll  # noqa

config = context.config
fileConfig(config.config_file_name)

target_metadata = None  # using raw SQL in migration

def run_migrations_offline():
    context.configure(url=config.get_main_option("sqlalchemy.url"), literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()