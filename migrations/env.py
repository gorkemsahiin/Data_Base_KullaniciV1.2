from __future__ import with_statement
import os
from alembic import context
from sqlalchemy import engine_from_config, create_engine
from sqlalchemy import engine_from_config, pool

from sqlalchemy.ext.declarative import DeclarativeMeta
from logging.config import fileConfig

from sqlalchemy.orm import scoped_session, sessionmaker
from kullanici_modeli_test import db  # Flask uygulamanızın ve db nesnenizin import edildiği yer

# This is the Alembic Config object, which provides
# access to the configuration options and is used to
# run migration commands.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers for alembic.
fileConfig(config.config_file_name)

# Add your model's MetaData object here
# for 'autogenerate' support
target_metadata = db.metadata  # Flask-SQLAlchemy'nin metadata'sını ekleyin

# Other setup code
def run_migrations_offline():
    """Run migrations in 'offline' mode.
    This mode is used when you want to run migrations without connecting to a database.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, dialect_opts={"paramstyle": "named"}
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode.
    In this mode, Alembic connects to the database to run migrations.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
