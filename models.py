import datetime
from sqlmodel import SQLModel, Field


class LivroBase(SQLModel):
    titulo: str
    genero: str = Field(default='Desconhecido')
    autor: str
    pais: str = Field(min_length=3)
    ano: int = Field(le=datetime.datetime.now().year)
    paginas: int


class Livro(LivroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class RequestLivro(LivroBase):
    pass


class Autor(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    ano_nascimento: int