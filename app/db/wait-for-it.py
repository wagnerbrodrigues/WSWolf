import time
import os
import configparser
import mysql.connector

def check_mysql_availability(host, port, user, password, max_attempts=30, interval_seconds=5):

    max_attempts = 30
    interval_seconds = 5

    attempts = 0
    while attempts < max_attempts:
        try:
            # Obtenha uma conexão usando o método get_database
            connection = mysql.connector.connect(host=host, port=port, user=user, password=password)
            connection.close()
            print("Contêiner do MySQL está pronto!")
            return True
        except Exception as e:
            attempts += 1
            print(f"Tentativa {attempts}/{max_attempts}: Aguardando contêiner do MySQL...")
            time.sleep(interval_seconds)
    print(f"Falha ao aguardar contêiner do MySQL após {max_attempts} tentativas.")
    return False

if __name__ == "__main__":
    currentDir = os.path.dirname(__file__) 
    config_file_path = os.path.join(currentDir, 'mysql_config.conf')

    config = configparser.ConfigParser()
    config.read(config_file_path)

    host = config['MySQL']['host']
    user = config['MySQL']['user']
    port = int(config['MySQL']['port'])
    password = config['MySQL']['password']

    print(f"{host}, {port}, {user}, {password}")

    check_mysql_availability(host, port, user, password) 