# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
# from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@db/testdb"

# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base: DeclarativeMeta = declarative_base()

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeMeta, DeclarativeBase

# Асинхронный URL подключения с asyncpg
SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://user:password@db/testdb"

# Создаем асинхронный движок
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Создаем сессию, асинхронную
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

# Базовый класс — оставляем как есть, но лучше перейти на DeclarativeBase в дальнейшем
Base: DeclarativeMeta = DeclarativeBase()

# Асинхронный генератор сессий
async def get_db():
    async with SessionLocal() as db:
        yield db
