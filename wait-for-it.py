import time
import mysql.connector

def check_mysql_availability(host, port, user, password, max_attempts=30, interval_seconds=5):
    attempts = 0
    while attempts < max_attempts:
        try:
            connection = mysql.connector.connect(host=host, port=port, user=user, password=password)
            connection.close()
            print("Contêiner do MySQL está pronto!")
            return True
        except mysql.connector.Error as err:
            attempts += 1
            print(f"Tentativa {attempts}/{max_attempts}: Aguardando contêiner do MySQL...")
            time.sleep(interval_seconds)
    print(f"Falha ao aguardar contêiner do MySQL após {max_attempts} tentativas.")
    return False

if __name__ == "__main__":
    host = "localhost"
    port = 3306
    user = "user"  # Substitua pelo usuário do MySQL definido no docker-compose.yml
    password = "pass"  # Substitua pela senha do MySQL definida no docker-compose.yml

    check_mysql_availability(host, port, user, password)