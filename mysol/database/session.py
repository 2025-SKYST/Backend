from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from mysol.database.settings import DB_SETTINGS

# 데이터베이스 연결 URL 생성
DATABASE_URL = (
    f"{DB_SETTINGS.dialect}+{DB_SETTINGS.driver}://"
    f"{DB_SETTINGS.user}:{DB_SETTINGS.password}@"
    f"{DB_SETTINGS.host}:{DB_SETTINGS.port}/{DB_SETTINGS.database}"
)

# 데이터베이스 엔진 생성
engine = create_async_engine(DATABASE_URL, echo=True)

# 비동기 세션 생성
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
