from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_name_duplicate, check_project_before_edit
from app.core.constants import (ERROR_FULL_AMOUNT_LESS_THAN_INVESTED,
                                ERROR_PROJECT_HAS_INVESTMENTS,
                                HTTP_400_BAD_REQUEST)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.investment import invest

router = APIRouter()


@router.post("/", response_model=CharityProjectDB)
async def create_project(
    project_in: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
    _user=Depends(current_superuser),
):
    await check_name_duplicate(project_in.name, session)
    new_project = await charity_project_crud.create(project_in, session)
    await invest(session)
    await session.commit()
    await session.refresh(new_project)
    return CharityProjectDB.model_validate(new_project)


@router.get("/", response_model=list[CharityProjectDB])
async def get_all_projects(
    session: AsyncSession = Depends(get_async_session),
):
    projects = await charity_project_crud.get_multi(session)
    return [CharityProjectDB.model_validate(project) for project in projects]


@router.patch("/{project_id}", response_model=CharityProjectDB)
async def update_project(
    project_id: int,
    project_update: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
    _user=Depends(current_superuser),
):
    project = await check_project_before_edit(project_id, session)
    if project_update.name is not None:
        await check_name_duplicate(project_update.name, session)
    if (
        project_update.full_amount is not None
        and project_update.full_amount < project.invested_amount
    ):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=ERROR_FULL_AMOUNT_LESS_THAN_INVESTED,
        )
    updated = await charity_project_crud.update(
        project,
        project_update,
        session,
    )
    if updated.invested_amount >= updated.full_amount:
        updated.fully_invested = True
        updated.close_date = datetime.now()
        session.add(updated)
    await session.commit()
    await session.refresh(updated)
    return CharityProjectDB.model_validate(updated)


@router.delete("/{project_id}", response_model=CharityProjectDB)
async def delete_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
    _user=Depends(current_superuser),
):
    project = await check_project_before_edit(project_id, session)
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=ERROR_PROJECT_HAS_INVESTMENTS,
        )
    deleted = await charity_project_crud.remove(project, session)
    return CharityProjectDB.model_validate(deleted)
