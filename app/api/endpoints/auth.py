from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.security import create_access_token, verify_password
from app.crud.user import create_user, get_user_by_email
from app.schemas.user import LoginRequest, UserCreate, UserRead

router = APIRouter()


@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED
)
async def register(
    user_data: UserCreate, session: AsyncSession = Depends(get_async_session)
):
    """
    Регистрирует нового пользователя.

    - Проверяет, что пароль не короче 3 символов (иначе 400).
    - Проверяет, что email ещё не занят.
    - Возвращает данные пользователя с кодом 201.
    """
    if len(user_data.password) < 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password too short",
        )
    existing = await get_user_by_email(session, user_data.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    new_user = await create_user(session, user_data)
    return new_user


@router.post("/jwt/login")
async def login(
    login_data: LoginRequest,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Аутентифицирует пользователя и выдаёт JWT-токен.

    При неверных данных – 400.
    """
    user = await get_user_by_email(session, login_data.email)
    if not user or not verify_password(
        login_data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=timedelta(minutes=30)
    )
    return {"access_token": access_token, "token_type": "bearer"}
