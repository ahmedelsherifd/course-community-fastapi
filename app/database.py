from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from . import config
from sqlalchemy import URL
from sqlalchemy.orm import DeclarativeBase, sessionmaker

settings = config.get_settings()


SQLALCHEMY_DATABASE_URL = "postgresql://{dbuser}:{dbpass}@{dbhost}/{dbname}".format(
    dbuser=settings.DBUSER,
    dbpass=settings.DBPASS,
    dbhost=settings.DBHOST,
    dbname=settings.DBNAME,
)


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    ...
