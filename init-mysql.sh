#Caminho para o arquivo docker-compose.yml
mysql_compose_file="docker-compose-mysql.yaml"

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


# Função para verificar se o MySQL está pronto para conexão
wait_for_mysql() {
    
    until docker exec "$container_name" mysqladmin ping -h"$host" --silent; do
        echo "Aguardando o MySQL estar pronto para conexão..."
        sleep 1
    done
}

# Subir o contêiner MySQL com o Docker Compose
if docker-compose -f "$mysql_compose_file" up --build -d; then
    echo "Contêiner MySQL iniciado com sucesso."
    # Aguardar até que o MySQL esteja pronto para conexão
    wait_for_mysql
    echo "MySQL está pronto para conexão."
else
    echo "Erro ao iniciar o contêiner MySQL."
    exit 1
fi

# Descompactar o arquivo ZIP
unzip -o "$zip_file" -d "$extracted_dir"

# Restaurar o banco de dados no MySQL
docker exec -i "$container_name" mysql -h "$host" -u "$root_user" -p"$password" "$database" < "$backup_file" || true
echo "Banco de dados restaurado com sucesso!"
