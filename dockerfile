FROM python:alpine3.19

# Copia o conteúdo local para o contêiner no diretório /app
COPY /app /app

# Define o diretório de trabalho como /app
WORKDIR /app

# Instalação do Chromium
RUN apk add chromium
RUN apk add chromium-chromedriver

ENV PYDEVD_DISABLE_FILE_VALIDATION=1

# Instalação das dependências Python
RUN pip install -r requirements.txt

# Comando padrão a ser executado ao iniciar o contêiner
CMD ["python", "./main.py"]
#docker build . -t testedebug > output.txt 2>&1 &&  docker run -p 5678:5678 --network mysql_network --name testedebug testedebug
#CMD ["python", "-m", "debugpy", "--listen", "0.0.0.0:5678", "--wait-for-client", "main.py"]