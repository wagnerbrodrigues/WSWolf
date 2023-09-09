import mysql.connector
import pandas as pd
import configparser
import os

class database:

    def __init__(self, logger):
        currentDir = os.path.dirname(__file__) 
        config_file_path = currentDir + '\mysql_config.conf'
        config = configparser.ConfigParser()
        config.read(config_file_path)

        self.host = config['MySQL']['host']
        self.user = config['MySQL']['user']
        self.port = int(config['MySQL']['port'])
        self.password = config['MySQL']['password']
        self.database = config['MySQL']['database']
    
        self.con = self.get_database()
        self.logger = logger

 

    def insertDB(self, table, df):
        if df.empty:
            self.logger.info("DataFrame está vazio. Nenhuma inserção será realizada.")
            return

        # Obter os nomes das colunas
        cols = ",".join([str(i) for i in df.columns.tolist()])
        cursor = self.con.cursor()

        # Iterar sobre as linhas do DataFrame
        try:
            
            for _, row in df.iterrows():
                # Gerar os placeholders para os valores
                placeholders = "%s," * len(row)
                placeholders = placeholders[:-1]  # Remover a última vírgula

                # Gerar a consulta SQL
                sql = f"INSERT INTO {table} ({cols}) VALUES ({placeholders})"

                # Executar a consulta SQL passando os valores da linha
                cursor.execute(sql, tuple(row))
            
            self.con.commit()

        except Exception as e:
            self.logger.exception(f"insertDB: {e}, erro ao inserir na tabela {table}")


    def updateDB(self, table, df, condition_col):
        cursor = self.con.cursor()

        try:
            for _, row in df.iterrows():
                values = []
                condition = [] #row[condition_col]

                for col, value in row.items():
                    if col in condition_col:
                        condition.append(f"{col} = '{value}'")
                    elif not pd.isnull(value):
                        values.append(f"{col} = '{value}'")

                values_str = ", ".join(values)
                condition_str = " AND ".join(condition)
                
                sql = f"UPDATE {table} SET {values_str} WHERE {condition_str}"
                cursor.execute(sql)

            self.con.commit()

        except Exception as e:
            self.logger.exception(f"updateDB: {e}, erro ao atualizar a tabela {table}")

    def load_table_to_dataframe(self, table):
        cursor = self.con.cursor()
        sql = f"SELECT * FROM {table}"

        try:
            cursor.execute(sql)
            columns = [column[0] for column in cursor.description]
            data = cursor.fetchall()

            df = pd.DataFrame(data, columns=columns)
            return df

        except Exception as e:
            self.logger.exception(f"load_table_to_dataframe: {e}, erro ao carregar a tabela {table}")

  
    def load_table_to_dataframe_where(self, table, where_column=None, where_value=None):
        cursor = self.con.cursor()
        sql = f"SELECT * FROM {table}"

        if where_column : #and where_value:
            sql += f" WHERE {where_column} = %s"
            params = (where_value,)
        else:
            params = None

        try:
            cursor.execute(sql, params)
            columns = [column[0] for column in cursor.description]
            data = cursor.fetchall()

            df = pd.DataFrame(data, columns=columns)
            return df

        except Exception as e:
            self.logger.exception(f"load_table_to_dataframe: {e}, erro ao carregar a tabela {table}")
    
    def delete_from_table_where(self, table, where_column=None, where_value=None):
        cursor = self.con.cursor()
        sql = f"DELETE FROM {table}"

        if where_column and where_value:
            sql += f" WHERE {where_column} = %s"
            params = (where_value,)
        else:
            params = None

        try:
            cursor.execute(sql, params)
            self.con.commit()
            self.logger.info(f"Registros deletados da tabela {table}")
        except Exception as e:
            self.con.rollback()  # Desfaz alterações em caso de erro
            self.logger.exception(f"delete_from_table_where: {e}, erro ao deletar da tabela {table}")

    
    def get_latest_date(self):
        # Conectar ao banco de dados MySQL
        cursor = self.con.cursor()
        # Consultar a data mais recente na tabela controle_coleta
        query = "SELECT MAX(dt_coleta) FROM controle_coleta"

        try:
            cursor.execute(query)
            latest_date = cursor.fetchone()[0]

            return latest_date

        except Exception as e:
            self.logger.exception(f"get_latest_date: {e}, erro ao obter a data mais recente")

    def truncate_table(self, table_name):
        cursor = self.con.cursor()
        try:
            cursor.execute(f"TRUNCATE TABLE {table_name}")
            self.con.commit()
        except Exception as e:
            self.logger.exception(f"truncate_tables {e}")    

    def get_database(self):
        con = mysql.connector.connect(
            host = self.host,
            user = self.user,
            port = self.port,
            password = self.password,
            database = self.database
        )

        return con