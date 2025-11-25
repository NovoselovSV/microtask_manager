from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from configs.settings import Settings

settings = Settings()

DIALECT = settings.db.dialect
DRIVER = settings.db.driver
DB_NAME = settings.db.name
DB_USERNAME = settings.db.username
DB_PASSWORD = settings.db.password
DB_HOST = settings.db.host
DB_PORT = settings.db.port
SQLALCHEMY_DATABASE_URL = settings.db.dsn

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False)

Base = declarative_base()


async def get_db() -> AsyncSession:  # type: ignore
    async with SessionLocal() as session:
        yield session
