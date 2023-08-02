@echo off

REM Nome do ambiente virtual
set "env_name=wswolf"

REM Criar ambiente virtual
:: virtualenv %env_name%


REM Ativar ambiente virtual
:: all %env_name%\Scripts\activate

REM Instalar dependências Python do requirements.txt
python3 -m pip install -r requirements.txt

REM Caminho para o arquivo docker-compose.yml
set "compose_file=mysql\docker-compose.yaml"

REM Subir o contêiner MySQL com o Docker Compose
docker-compose -f %compose_file% up -d

REM Esperar até que o contêiner do MySQL esteja pronto
python wait-for-it.py

REM Nome do arquivo ZIP
set "zip_file=mysql\dump.sql.zip"

REM Caminho para o diretório de destino da descompactação
set "extracted_dir=mysql"

REM Descompactar o arquivo ZIP
powershell Expand-Archive -Path %zip_file% -DestinationPath %extracted_dir% -Force

REM Restaurar o banco de dados no MySQL
set "backup_file=%extracted_dir%\dump.sql"

REM Restaurar o banco de dados no MySQL
set "mysql_host=localhost"
set "mysql_user=root"  REM Substitua pelo usuário do MySQL definido no docker-compose.yml
set "mysql_password=pass"  REM Substitua pela senha do MySQL definida no docker-compose.yml
set "mysql_db=wswolf"  REM Substitua pelo nome do banco de dados definido no docker-compose.yml

docker exec -i mysql_scraper mysql -h %mysql_host% -u %mysql_user% -p%mysql_password% %mysql_db% < %backup_file%

echo Banco de dados restaurado com sucesso!