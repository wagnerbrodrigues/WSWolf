import os
import configparser

currentDir = os.path.dirname(__file__) 
config_file_path = os.path.join(currentDir, '.env')
config = configparser.ConfigParser()
config.read(config_file_path)

host = config['MySQL']['DB_HOST']
user = config['MySQL']['DB_USERNAME']
root = config['MySQL']['DB_USERNAME']
port = int(config['MySQL']['DB_PORT'])
password = config['MySQL']['DB_PASSWORD']
dbname = config['MySQL']['DB_NAME']