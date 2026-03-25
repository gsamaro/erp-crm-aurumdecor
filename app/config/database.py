from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import sessionmaker

from app.config.settings import settings

database_url = settings.database_url
connect_args = {}

if make_url(database_url).drivername.startswith("postgresql"):
    connect_args["sslmode"] = "require"

engine = create_engine(database_url, pool_pre_ping=True, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
