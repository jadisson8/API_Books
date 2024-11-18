from fastapi import APIRouter, status, HTTPException

from .database import get_engine
from .models import Livro, RequestLivro
from sqlmodel import Session, select, update


router = APIRouter()


@router.get('', status_code=status.HTTP_200_OK)
def lista_livros(genero: str | None = None):
    with Session(get_engine()) as session:
        if not genero:
            livros = session.exec(select(Livro)).all()
        else:
            livros = session.exec(select(Livro).where(Livro.genero == genero)).all()
        return livros


@router.get('/{livro_id}')
def detalhar_livro(livro_id: int):
    with Session(get_engine()) as session:
        livro = session.get(Livro, livro_id)
        if livro:
            return livro
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Livro não localizado com id = {livro_id}')


@router.post('', status_code=status.HTTP_201_CREATED)
def criar_livro(request_livro: RequestLivro):
    livro = Livro(
        titulo=request_livro.titulo,
        genero=request_livro.genero,
        autor=request_livro.autor,
        pais=request_livro.pais,
        ano=request_livro.ano,
        paginas=request_livro.paginas
    )

    with Session(get_engine()) as session:
        session.add(livro)
        session.commit()
        session.refresh(livro)
        return livro


@router.put('/{livro_id}')
def alterar_livro(livro_id: int, dados: RequestLivro):
    with Session(get_engine()) as session:
        livro = session.get(Livro, livro_id)
        if livro:
            session.exec(update(Livro).where(Livro.id == livro_id).values(titulo=dados.titulo,
                                                                         genero=dados.genero,
                                                                         autor=dados.autor,
                                                                         pais=dados.pais,
                                                                         ano=dados.ano,
                                                                         paginas=dados.paginas))
            session.commit()
            return f'Livro de id = {livro_id} alterado com sucesso!'
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Livro não localizado com id = {livro_id}')


@router.delete('/{livro_id}', status_code=status.HTTP_204_NO_CONTENT)
def deletar_livro(livro_id: int):
    with Session(get_engine()) as session:
        livro = session.get(Livro, livro_id)
        if livro:
            session.delete(livro)
            session.commit()
            return
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Livro não localizado com id = {livro_id}')