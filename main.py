from fastapi import FastAPI
from sqlmodel import SQLModel
from .livros_controller import router as livros_router
from .database import get_engine


app = FastAPI()


# Registrar os Router (controllers)
app.include_router(livros_router,
                   prefix='/livros')

# Criar DB
SQLModel.metadata.create_all(get_engine())
