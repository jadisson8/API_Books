from fastapi import FastAPI
from sqlmodel import SQLModel
from .livros_controller import router as livros_router
from .database import get_engine


app = FastAPI()


app.include_router(livros_router,
                   prefix='/livros')

SQLModel.metadata.create_all(get_engine())