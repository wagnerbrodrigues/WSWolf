import zipfile
import os
# import configparser
import subprocess

from .config_db import * 

class Backup:
    def __init__(self):
        # self.config_file_path = os.path.join(os.path.dirname(__file__), 'mysql_config.conf')
        self.dump_file_path = self.get_dump_file_path()

    def get_dump_file_path(self):
        current_dir = os.path.dirname(__file__)
     #   ws_wolf_dir = os.path.dirname(current_dir)
        return os.path.join(current_dir, "backup", "dump.sql")

    def execute_mysql_dump(self):
        try:

            # Comando para realizar o dump diretamente no sistema
            dump_command = [
                'mysqldump',
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

            # Criar arquivo ZIP compactado
            zip_file_path = self.dump_file_path + '.zip'
            with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                zip_file.write(self.dump_file_path, os.path.basename(self.dump_file_path))

            print("Arquivo ZIP compactado criado:", zip_file_path)

        except subprocess.CalledProcessError as e:
            print(f"Erro ao realizar o dump: {e}")

if __name__ == "__main__":
    backup_instance = Backup()
    backup_instance.execute_mysql_dump()
