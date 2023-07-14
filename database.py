import mysql.connector
import pandas as pd

class database:
    def __init__(self):
        self.con = self.get_database()

    def insertDB(self, table, df):
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
            print(f"insertDB: {e}, erro ao inserir na tabela {table}")  


    def updateDB(self, table, df, condition_col):
        cursor = self.con.cursor()

        try:
            for _, row in df.iterrows():
                values = []
                condition_val = row[condition_col]

                for col, value in row.items():
                    if col != condition_col and not pd.isnull(value):
                        values.append(f"{col} = '{value}'")

                values_str = ", ".join(values)
                sql = f"UPDATE {table} SET {values_str} WHERE {condition_col} = '{condition_val}'"
                cursor.execute(sql)

            self.con.commit()

        except Exception as e:
            print(f"updateDB: {e}, erro ao atualizar a tabela {table}")

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
            print(f"load_table_to_dataframe: {e}, erro ao carregar a tabela {table}")

    
    def truncate_tables(self):
        cursor = self.con.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        try:
            for table in tables:
                table_name = table[0]
                cursor.execute(f"TRUNCATE TABLE {table_name}")

            self.con.commit()
        except Exception as e:
            print(f"truncate_tables {e}")    

    def get_database(self):
        con = mysql.connector.connect(
            host="localhost",
            user="user",
            password="pass",
            database="scrapper"
        )

        return con