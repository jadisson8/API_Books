# 1. Maquina com Python
FROM python:3.13.0-slim-bullseye

# 2. Copy arquivos
WORKDIR /home/app
COPY ./requirements.txt .

# 3. Instalar as Dependencias
RUN pip install -r requirements.txt

# 4. Copy arquivos
COPY . .

# 4. Expor Porta
EXPOSE 8000

# 5. Rodar a aplicação
CMD ["fastapi","run", "main.py", "0.0.0.0:8000"]
