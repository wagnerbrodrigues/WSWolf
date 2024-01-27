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

# # Verificar se o ambiente virtual já existe
# if [ ! -d "venv" ]; then
#     echo "Criando ambiente virtual..."
#     python3 -m venv venv
# fi

# # Ativar o ambiente virtual
# if [ -f "venv/bin/activate" ]; then
#     source venv/bin/activate
#     echo "Ambiente virtual ativado."
# else
#     echo "O ambiente virtual não foi encontrado. Certifique-se de que foi criado corretamente."
#     exit 1
# fi

# Caminho para o arquivo docker-compose.yml
mysql_compose_file="docker-compose-mysql.yaml"
wswolf_compose_file="docker-compose.yaml"

# Nome do arquivo ZIP
zip_file="mysql/backup/dump.sql.zip"

# Caminho para o diretório de destino da descompactação
extracted_dir="mysql"

# Restaurar o banco de dados no MySQL
backup_file="$extracted_dir/dump.sql"

# Inicialização das variáveis
host=""
user=""
password=""
database=""
container_name=""

# Ler as configurações do MySQL do arquivo mysql_config.conf dentro da subpasta db
while IFS='=' read -r key value; do
    key=$(echo $key | tr -d '[:space:]')  # Remover espaços em branco
    value=$(echo $value | tr -d '[:space:]')
    # Verifica a chave e atribui o valor correspondente à variável apropriada
    case "$key" in
        "DB_HOST") host="$value" ;;
        "DB_ROOTUSER") root_user="$value" ;;
        "DB_ROOT_PASSWORD") password="$value" ;;
        "DB_NAME") database="$value" ;;
        "CONTAINER_NAME") container_name="$value" ;;
    esac
done < <(grep -E '^(DB_HOST|DB_ROOTUSER|DB_ROOT_PASSWORD|DB_NAME|CONTAINER_NAME)=' .env)

# Subir o contêiner MySQL com o Docker Compose
if docker-compose -f "$mysql_compose_file" up --build -d; then
    echo "Contêiner MySQL iniciado com sucesso."
else
    echo "Erro ao iniciar o contêiner MySQL."
    exit 1
fi

# Descompactar o arquivo ZIP
unzip -o "$zip_file" -d "$extracted_dir"


# Restaurar o banco de dados no MySQL
docker exec -i "$container_name" mysql -h "$host" -u "$root_user" -p"$password" "$database" < "$backup_file" || true
echo "Banco de dados restaurado com sucesso!"

# # Desativação do ambiente virtual
# deactivate

# Subir o contêiner WsWolf com o Docker Compose
if docker-compose -f "$wswolf_compose_file" up --build -d; then
    echo "Contêiner WsWolf iniciado com sucesso."
else
    echo "Erro ao iniciar o contêiner WsWolf."
    exit 1
fi