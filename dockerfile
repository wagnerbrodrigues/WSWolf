# Etapa de construção
FROM python:3.12-slim as builder

# Definindo argumentos
ARG fator_bazin
ARG param
ARG meses_bazin

# Define o diretório de trabalho como /app
WORKDIR /app

# Instalação de dependências para compilação
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    python3-dev \
    mariadb-client \
    libmariadb-dev-compat \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Copia o conteúdo local para o contêiner no diretório /app
COPY /app /app

# Instalação das dependências Python
RUN pip install --upgrade pip
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r /app/requirements.txt

# Etapa final
FROM python:3.12-slim

# Define o diretório de trabalho como /app
WORKDIR /app

# Instalação de dependências de runtime
RUN apt-get update && apt-get install -y \
    mariadb-client \
    chromium \
    chromium-driver \
    libmariadb3 \
    && rm -rf /var/lib/apt/lists/*

# Copia as rodas pré-compiladas e instala as dependências Python
COPY --from=builder /wheels /wheels
RUN pip install --no-cache /wheels/*

# Copia o conteúdo local para o contêiner no diretório /app
COPY /app /app

# Define variáveis de ambiente
ENV PYDEVD_DISABLE_FILE_VALIDATION=1
ENV fator_bazin=$fator_bazin
ENV meses_bazin=$meses_bazin
ENV param=$param

# Comando padrão a ser executado ao iniciar o contêiner
CMD ["python", "./main.py"]
#docker build . -t testedebug > output.txt 2>&1 && docker run -p 5678:5678 --network mysql_network --name testedebug testedebug
#CMD ["python", "-m", "debugpy", "--listen", "0.0.0.0:5678", "--wait-for-client", "main.py"]
