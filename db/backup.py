import subprocess
import zipfile
import os
import configparser


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



currentDir = os.path.dirname(__file__) 
config_file_path = currentDir + '\mysql_config.conf'

diretorioWsWolf = os.path.dirname(currentDir)
dump_file_path =  diretorioWsWolf + "\\mysql\dump.sql"

config = configparser.ConfigParser()

# Parâmetros para o dump
config = configparser.ConfigParser()
config.read(config_file_path)

host = config['MySQL']['host']
user = config['MySQL']['user']
port = int(config['MySQL']['port'])
password = config['MySQL']['password']
database = config['MySQL']['database']
container_name = config['MySQL']['container_name']

# Executa o dump
execute_mysql_dump(container_name, host, user, password, database, dump_file_path)