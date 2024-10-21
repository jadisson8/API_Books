import datetime
from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()


class Livro(BaseModel):
    id: int | None = None
    titulo: str
    genero: str = Field(default="Desconhecido")
    autor: str
    pais: str = Field(min_length=3)
    ano: int = Field(le=datetime.datetime.now().year)
    paginas: int


class AlterarLivro(BaseModel):
    genero: str = Field(default="Desconhecido")
    ano: int = Field(le=datetime.datetime.now().year)


acervo_livros: list[Livro] = []

acervo_livros.append(Livro(id=1, titulo="Crepúsculo 1 (Twilight)", genero="Romance",
                           autor="Stephenie Meyer", pais="EUA", ano=2005, paginas=480))
acervo_livros.append(Livro(id=2, titulo="A depressão é uma borboleta azul", genero="Poesia",
                           autor="Sabrine Cantele", pais="BRA", ano=2022, paginas=94))


@app.get("/livros", status_code=status.HTTP_200_OK)
def lista_livros(genero: str | None = None, ano: int | None = None):

    livros = []

    if not genero and not ano:
        return acervo_livros

    elif genero and not ano:
        for livro in acervo_livros:
            if genero.lower().strip() == livro.genero.lower().strip() and not ano:
                livros.append(livro)

    elif not genero and ano:
        for livro in acervo_livros:
            if not genero and ano == livro.ano:
                livros.append(livro)

    else:
        for livro in acervo_livros:
            if genero.lower().strip() == livro.genero.lower().strip() and ano == livro.ano:
                livros.append(livro)

    return livros


@app.get("/livros/{livro_id}")
def detalhar_livro(livro_id: int):
    for livro in acervo_livros:
        if livro.id == livro_id:
            return livro

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Livro não localizado com id = {livro_id}")


@app.post("/livros", status_code=status.HTTP_201_CREATED)
def criar_livro(novo_livro: Livro):
    acervo_livros.append(novo_livro)
    return novo_livro


@app.put("/livros/{livro_id}")
def alterar_livro(livro_id: int, dados: AlterarLivro):
    for livro in acervo_livros:
        if livro.id == livro_id:
            livro.genero = dados.genero
            livro.ano = dados.ano
            return livro

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Livro não localizado com id = {livro_id}")


@app.delete("/livros/{livro_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_livro(livro_id: int):
    for livro in acervo_livros:
        if livro.id == livro_id:
            acervo_livros.remove(livro)
            return

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Livro não localizado com id = {livro_id}")
