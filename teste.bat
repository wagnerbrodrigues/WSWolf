REM Ler as configurações do MySQL do arquivo mysql_config.conf dentro da subpasta db
for /f "delims=" %%a in (db\mysql_config.conf) do set "%%a"

REM Restaurar o banco de dados no MySQL
echo %container_name%  
echo %host% 
echo %password% %database% 
echo %backup_file%