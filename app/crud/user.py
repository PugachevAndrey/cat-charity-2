from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash


async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    """Возвращает пользователя по email или None."""
    result = await session.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def create_user(session: AsyncSession, user_data: UserCreate) -> User:
    """Создаёт нового пользователя в базе данных."""
    hashed = get_password_hash(user_data.password)
    db_user = User(email=user_data.email, hashed_password=hashed)
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user
