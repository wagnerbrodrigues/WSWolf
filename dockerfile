# Use a imagem python:3-alpine como base
FROM python:alpine3.19

# Define o diretório de trabalho como /app
WORKDIR /app

# Instalação do MySQL Client
RUN apk --no-cache add mysql-client
RUN apk --no-cache add mariadb-connector-c


# Copia o conteúdo local para o contêiner no diretório /app
COPY /app /app

# Instalação do Chromium
RUN apk add chromium
RUN apk add chromium-chromedriver

# Instalação das dependências Python
RUN pip install -r requirements.txt

# Comando padrão a ser executado ao iniciar o contêiner
CMD ["python", "./main.py"]
