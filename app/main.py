from fastapi import FastAPI
from app.api.endpoints.charity_project import router as charity_router
from app.api.endpoints.donation import router as donation_router
from app.api.endpoints.auth import router as auth_router  # кастомный auth

app = FastAPI(title="QRKot")

# Подключаем кастомный auth роутер
app.include_router(auth_router, prefix="/auth", tags=["auth"])

# Основные роутеры
app.include_router(charity_router, prefix="/charity_project", tags=["Проекты"])
app.include_router(donation_router, prefix="/donation", tags=["Пожертвования"])


@app.get("/")
async def root():
    return {"message": "QRKot API"}
