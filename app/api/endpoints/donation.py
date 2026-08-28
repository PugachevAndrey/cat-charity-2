from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.crud.donation import donation_crud
from app.schemas.donation import (
    DonationCreate,
    DonationCreateResponse,
    DonationDB,
    DonationUser,
)
from app.services.investment import invest

router = APIRouter()


@router.post("/", response_model=DonationCreateResponse)
async def create_donation(
    donation_create: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user=Depends(current_user),
):
    donation_data = donation_create.model_dump()
    donation_data["user_id"] = user.id
    new_donation = await donation_crud.create(donation_data, session)
    await invest(session)
    await session.commit()
    await session.refresh(new_donation)
    return DonationCreateResponse.model_validate(new_donation)


@router.get("/", response_model=list[DonationDB])
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
    _user=Depends(current_superuser),
):
    donations = await donation_crud.get_multi(session)
    return [DonationDB.model_validate(donation) for donation in donations]


@router.get("/my", response_model=list[DonationUser])
async def get_my_donations(
    session: AsyncSession = Depends(get_async_session),
    user=Depends(current_user),
):
    donations = await donation_crud.get_by_user(
        user_id=user.id, session=session
    )
    return [DonationUser.model_validate(donation) for donation in donations]
