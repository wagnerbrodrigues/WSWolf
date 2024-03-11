import os
import subprocess

from .config_db import *

class Backup:
    def __init__(self):
        self.dump_file_path = self.get_dump_file_path()

    def get_dump_file_path(self):
        current_dir = os.path.dirname(__file__)
        return os.path.join(current_dir, "backup", "dump.sql")

    def execute_mysql_dump(self):
        try:
            # Comando para realizar o dump diretamente no sistema
            dump_command = [
                'mysqldump',
                f'--no-tablespaces',
                f'--host={host}',
                f'--user={user}',
                f'--password={password}',
                f'--port={port}',
                '--databases', dbname
            ]

            # Executa o comando de dump diretamente no sistema
            dump_output = subprocess.check_output(dump_command, universal_newlines=True)

            # Escreve a saída do dump em um arquivo local
            with open(self.dump_file_path, 'w') as dump_file:
                dump_file.write(dump_output)

            # Compacta o arquivo SQL com gzip
            gzip_file_path = self.dump_file_path + '.gz'
            with open(self.dump_file_path, 'rb') as sql_file:
                with open(gzip_file_path, 'wb') as gzip_file:
                    subprocess.run(['gzip', '-c'], input=sql_file.read(), stdout=gzip_file)

            print("Arquivo SQL compactado com gzip:", gzip_file_path)

        except subprocess.CalledProcessError as e:
            print(f"Erro ao realizar o dump: {e}")

if __name__ == "__main__":
    backup_instance = Backup()
    backup_instance.execute_mysql_dump()

