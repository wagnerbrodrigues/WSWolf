#!/bin/bash

# Define as variáveis para armazenar os valores do arquivo .env
host=""
user=""
password=""
database=""
container_name=""

# Loop para ler o arquivo .env
while IFS='=' read -r key value; do
    # Remove espaços em branco dos valores das chaves e dos valores
    key=$(echo "$key" | tr -d '[:space:]')
    value=$(echo "$value" | tr -d '[:space:]')
    
    # Verifica a chave e atribui o valor correspondente à variável apropriada
    case "$key" in
        "DB_HOST") host="$value" ;;
        "DB_USERNAME") user="$value" ;;
        "DB_ROOT_PASSWORD") password="$value" ;;
        "DB_NAME") database="$value" ;;
        "CONTAINER_NAME") container_name="$value" ;;
    esac
done < <(grep -E '^(DB_HOST|DB_USERNAME|DB_ROOT_PASSWORD|DB_NAME|CONTAINER_NAME)=' .env)

# Exemplo de uso
echo "Host: $host"
echo "User: $user"
echo "Password: $password"
echo "Database: $database"
echo "Container Name: $container_name"

