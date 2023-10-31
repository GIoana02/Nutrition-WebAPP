from fastapi import FastAPI
from src.api.users import user_router
from src.api.meals import meal_router

app = FastAPI()
app.include_router(user_router)
app.include_router(meal_router)


