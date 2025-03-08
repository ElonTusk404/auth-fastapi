from src.api import health_router
from fastapi import FastAPI
from src.api.v1.routers.user import router as v1_user_router

app = FastAPI()

app.include_router(health_router)
app.include_router(v1_user_router, prefix='/v1')





