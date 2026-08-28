from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base import InvestmentBase


class Donation(InvestmentBase):
    """
    Модель пожертвования.

    Хранит информацию о пожертвовании: сумма, комментарий,
    распределённая сумма, статус, даты создания и закрытия,
    а также идентификатор пользователя, сделавшего пожертвование.
    """

    __tablename__ = "donation"

    comment = Column(Text, nullable=True)
    full_amount = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=True
    )
