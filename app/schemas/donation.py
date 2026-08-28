from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class DonationBase(BaseModel):
    """
    Базовая схема пожертвования.

    Содержит обязательное поле full_amount и опциональное comment.
    Используется как основа для создания и отображения.
    """

    model_config = ConfigDict(extra="forbid")
    full_amount: int = Field(..., gt=0)
    comment: str | None = None


class DonationCreate(DonationBase):
    """Схема для создания нового пожертвования."""


class DonationCreateResponse(BaseModel):
    """
    Схема для ответа при создании пожертвования.

    Возвращает только пользовательские поля, без служебных
    (invested_amount, fully_invested, close_date, user_id).
    """

    full_amount: int
    comment: str | None = None
    id: int
    create_date: datetime

    model_config = ConfigDict(from_attributes=True)


class DonationDB(DonationBase):
    """
    Полная схема для чтения пожертвований (только для суперпользователя).

    Включает все поля модели, включая служебные:
    id, user_id, invested_amount, fully_invested, create_date, close_date.
    """

    id: int
    user_id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: datetime | None

    model_config = ConfigDict(from_attributes=True)


class DonationUser(BaseModel):
    """
    Схема для отображения пожертвований обычному пользователю.

    Доступны только поля: id, full_amount, comment, create_date.
    """

    id: int
    full_amount: int
    comment: str | None = None
    create_date: datetime

    model_config = ConfigDict(from_attributes=True)
