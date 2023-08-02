import subprocess
import zipfile
import os

def execute_mysql_dump(container_name, host, user, password, database, dump_file_path):
    try:
        # Comando para realizar o dump dentro do contêiner
        dump_command = [
            'docker', 'exec', '-i', container_name,
            'mysqldump',
            f'--host={host}',
            f'--user={user}',
            f'--password={password}',
            f'--databases', database
        ]

        # Executa o comando de dump dentro do contêiner
        dump_output = subprocess.check_output(dump_command)

        # Escreve a saída do dump em um arquivo local
        with open(dump_file_path, 'wb') as dump_file:
            dump_file.write(dump_output)

        # Criar arquivo ZIP compactado
        zip_file_path = dump_file_path + '.zip'
        with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.write(dump_file_path, os.path.basename(dump_file_path))

        print("Arquivo ZIP compactado criado:", zip_file_path)

        print("Arquivo ZIP criado:", zip_file_path)

        
    except subprocess.CalledProcessError as e:
        print(f"Erro ao realizar o dump: {e}")

# Parâmetros para o dump
container_name = 'mysql_scraper'
host = 'localhost'
user = 'root'
password = 'pass'
database = 'wswolf'
dump_file_path = os.path.dirname(__file__) + '\dump.sql'

# Executa o dump
execute_mysql_dump(container_name, host, user, password, database, dump_file_path)