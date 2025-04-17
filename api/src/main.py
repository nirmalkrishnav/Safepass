from fastapi import FastAPI
from .app.router import router as app_router

app = FastAPI()

app.include_router(app_router)
