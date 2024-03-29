@echo off

REM Nome do ambiente virtual
set "env_name=wswolf"

REM Instalar dependências Python do requirements.txt
python -m pip install -r requirements.txt

REM Caminho para o arquivo docker-compose.yml
set "mysql_compose_file=mysql\docker-compose-mysql.yaml"
set "wsfolf_compose_file=docker-compose-wswolf.yaml"

REM Subir o contêiner MySQL com o Docker Compose
docker-compose -f %mysql_compose_file% up -d

REM Esperar até que o contêiner do MySQL esteja pronto
python app\db\wait-for-it.py

REM Nome do arquivo ZIP
set "zip_file=mysql\backup\dump.sql.zip"

REM Caminho para o diretório de destino da descompactação
set "extracted_dir=mysql"

REM Descompactar o arquivo ZIP
powershell Expand-Archive -Path %zip_file% -DestinationPath %extracted_dir% -Force

REM Restaurar o banco de dados no MySQL
set "backup_file=%extracted_dir%\dump.sql"

REM Ler as configurações do MySQL do arquivo mysql_config.conf dentro da subpasta db
for /f "delims=" %%a in (app\db\mysql_config.conf) do set "%%a"

REM Restaurar o banco de dados no MySQL
docker exec -i  %container_name%  mysql -h %host% -u %user% -p%password% %database% < %backup_file%
echo Banco de dados restaurado com sucesso!

REM Subir o contêiner MySQL com o Docker Compose
docker-compose -f %wsfolf_compose_file% up -d