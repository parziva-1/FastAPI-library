from fastapi import FastAPI, APIRouter

from .database import *

from .routers import users_router


app = FastAPI(title="Libray created with FastAPI",
             description="Library... system",
             version="0.1"
            )

api_v1 = APIRouter(prefix="/api/v1")

api_v1.include_router(users_router)


app.include_router(api_v1)

Base.metadata.create_all(bind=engine)
