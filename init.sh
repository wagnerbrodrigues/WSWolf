#!/bin/bash

# Validações
if ! command -v unzip &> /dev/null; then
    echo "unzip não está instalado. Por favor, instale-o."
    exit 1
fi

if ! command -v docker &> /dev/null; then
    echo "docker não está instalado. Por favor, instale-o."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "docker-compose não está instalado. Por favor, instale-o."
    exit 1
fi

# Validação do Docker
if ! docker info &> /dev/null; then
    echo "O Docker não está em execução. Por favor, inicie o Docker e tente novamente."
    exit 1
fi

wswolf_compose_file="docker-compose.yaml"

#Iniciar MySQL
bash init-mysql.sh


# Verificar o retorno do comando anterior
if [ $? -eq 0 ]; then
    echo "MySQL iniciado com sucesso."
else
    echo "Erro ao iniciar o MySQL. Código de retorno: $?"
fi


#Remover o contêiner anterior
if docker-compose -f "$wswolf_compose_file" down; then
   echo "Contêiner anterior removido com sucesso."
else
   echo "Erro ao remover o contêiner anterior."
fi

if docker-compose -f "$wswolf_compose_file" up --build -d; then
    echo "Contêiner WsWolf iniciado com sucesso"
else
    echo "Erro ao iniciar o contêiner WsWolf."
    exit 1
fi