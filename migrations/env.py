from logging.config import fileConfig

import os
from urllib.parse import quote

from dotenv import load_dotenv
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

load_dotenv()


def _normalize_database_url(raw_url: str | None) -> str | None:
    if not raw_url:
        return raw_url

    raw_url = raw_url.strip().strip('"').strip("'")
    if "://" not in raw_url:
        return raw_url

    scheme, rest = raw_url.split("://", 1)
    if "@" not in rest:
        return raw_url

    creds_part, host_part = rest.rsplit("@", 1)
    if ":" not in creds_part:
        return raw_url

    username, password = creds_part.split(":", 1)
    safe_password = quote(password, safe="")
    return f"{scheme}://{username}:{safe_password}@{host_part}"


# add your model's MetaData object here
# for 'autogenerate' support
from app.domain.base import Base
from app.domain import client, user  # noqa: F401

target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = os.getenv("DATABASE_URL", config.get_main_option("sqlalchemy.url"))
    url = _normalize_database_url(url)
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    configuration = config.get_section(config.config_ini_section, {})
    configuration["sqlalchemy.url"] = _normalize_database_url(
        os.getenv("DATABASE_URL", configuration.get("sqlalchemy.url"))
    )
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
