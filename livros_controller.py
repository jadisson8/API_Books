from fastapi import APIRouter, status, HTTPException

from .database import get_engine
from .models import Livro, RequestLivro
from sqlmodel import Session, select, update


router = APIRouter()


@router.get("", status_code=status.HTTP_200_OK)
def lista_livros(genero: str | None = None):
    session = Session(get_engine())

    if not genero:
        statement = select(Livro)

    else:
        statement = select(Livro).where(Livro.genero == genero)

    livros = session.exec(statement).all()

    return livros


@router.get("/{livro_id}")
def detalhar_livro(livro_id: int):
    session = Session(get_engine())

    statement = select(Livro).where(Livro.id == livro_id)

    livro = session.exec(statement).first()

    if livro is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Livro não localizado com id = {livro_id}")

    return livro


@router.post("", status_code=status.HTTP_201_CREATED)
def criar_livro(request_livro: RequestLivro):
    livro = Livro(
        titulo=request_livro.titulo,
        genero=request_livro.genero,
        autor=request_livro.autor,
        pais=request_livro.pais,
        ano=request_livro.ano,
        paginas=request_livro.paginas
    )

    session = Session(get_engine())
    session.add(livro)
    session.commit()
    session.refresh(livro)

    return livro


@router.put("/{livro_id}")
def alterar_livro(livro_id: int, dados: RequestLivro):
    session = Session(get_engine())

    statement = update(Livro).where(Livro.id == livro_id).values(titulo=dados.titulo,
                                                                 genero=dados.genero,
                                                                 autor=dados.autor,
                                                                 pais=dados.pais,
                                                                 ano=dados.ano,
                                                                 paginas=dados.paginas)

    result = session.exec(statement).rowcount

    if result == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Livro não localizado com id = {livro_id}")

    session.commit()

    return f"Livro de id = {livro_id} alterado com sucesso!"


@router.delete("/{livro_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_livro(livro_id: int):
    session = Session(get_engine())

    statement = select(Livro).where(Livro.id == livro_id)

    livro = session.exec(statement).first()

    if livro is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Livro não localizado com id = {livro_id}")

    session.delete(livro)
    session.commit()

    return livro
