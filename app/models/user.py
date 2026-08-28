from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Boolean, Column, Integer, String

from app.core.db import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    """
    Модель пользователя для аутентификации.

    Наследуется от SQLAlchemyBaseUserTable и Base.
    Содержит: id, email, hashed_password, is_active, is_superuser, is_verified.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(length=320), unique=True, index=True, nullable=False)
    hashed_password = Column(String(length=1024), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
