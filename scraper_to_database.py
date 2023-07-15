import time
import pandas as pd
from datetime import datetime, timedelta


import json

from selenium import webdriver
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from database import database
from applogger import AppLogger

#Arquivos de Configuração
from config import * 

logger = AppLogger('scrapper.log')



def getConfig(file):
    with open(file, 'r') as data:
        config = json.load(data)

    return config

def tryCast(valor):
    try:
        valor = valor.replace(".","")
        valor = valor.replace(",",".")
        valor = valor.replace("%", "")
        return float(valor)
    except:
        return 0

def navegator():
    service = Service(chromeDriver)  # Insira o caminho para o chromedriver
    return webdriver.Chrome(service=service)

def parseDividento(str_dividendo, acao, data_coleta):
    try:
        dfDividendo = pd.read_json(str_dividendo)

        dfDividendo = dfDividendo.rename(columns={
        'ed': 'dt_comunicado',
        'pd': 'dt_pagamento',
        'et': 'tp_dividendo',
        'v': 'vlr'
        })
        dfDividendo['dt_comunicado'] = pd.to_datetime(dfDividendo['dt_comunicado'], dayfirst=True, errors='coerce').dt.strftime("%Y-%m-%d")
        dfDividendo['dt_pagamento'] = pd.to_datetime(dfDividendo['dt_pagamento'], dayfirst=True, errors='coerce').dt.strftime("%Y-%m-%d")

        columns_to_remove = ['y', 'm', 'd', 'ad', 'etd', 'ov', 'sv', 'sov', 'adj']
        dfDividendo = dfDividendo.drop(columns=columns_to_remove)
        dfDividendo['cod_acao'] = acao 
        dfDividendo['dt_coleta'] = data_coleta 
        
    except Exception as e:
        logger.exception(f"Erro no parse de dividendos de {acao}, erro: {e}")

    return dfDividendo

def corrigir_formato_data(df, coluna_data):
    df[coluna_data] = pd.to_datetime(df[coluna_data], dayfirst=True).dt.strftime("%Y-%m-%d")
    return df

def le_pagina(url, acao, data_coleta):
    nv = navegator()
    nv.get(url)
    time.sleep(0.25)

    try:
        dfPagina = pd.DataFrame({
            'dt_coleta': data_coleta,
            'cod_acao' : acao,
            'vlr_acao' : [tryCast(nv.find_element(By.XPATH, '//*[@id="main-2"]/div[2]/div/div[1]/div/div[1]/div/div[1]/strong').text)],
            'vlm_diario' : [tryCast(nv.find_element(By.XPATH, '/html/body/main/div[2]/div/div[5]/div/div/div[3]/div/div/div/strong').text)],
            'dy' : [tryCast(nv.find_element(By.XPATH, '/html/body/main/div[2]/div/div[1]/div/div[4]/div/div[1]/strong').text)],
            'pl' : [tryCast(nv.find_element(By.XPATH, '/html/body/main/div[2]/div/div[7]/div[2]/div/div[1]/div/div[2]/div/div/strong').text)],
            'pvp' : [tryCast(nv.find_element(By.XPATH, '/html/body/main/div[2]/div/div[7]/div[2]/div/div[1]/div/div[4]/div/div/strong').text)],
            'vpa' : [tryCast(nv.find_element(By.XPATH, '/html/body/main/div[2]/div/div[7]/div[2]/div/div[1]/div/div[9]/div/div/strong').text)],
            'roe' : [tryCast(nv.find_element(By.XPATH, '/html/body/main/div[2]/div/div[7]/div[2]/div/div[4]/div/div[1]/div/div/strong').text)],
            'lpa' : [tryCast(nv.find_element(By.XPATH, '/html/body/main/div[2]/div/div[7]/div[2]/div/div[1]/div/div[11]/div/div/strong').text)],
            'pebit':  [tryCast(nv.find_element(By.XPATH, '/html/body/main/div[2]/div/div[7]/div[2]/div/div[1]/div/div[8]/div/div/strong').text)]
        })

        #le dividendos
        results = nv.find_element(By.ID, 'results')
        dividendo_raw = results.get_attribute('value')
        dfDividendo = parseDividento(dividendo_raw, acao, data_coleta)
        

    except Exception as e:
        logger.exception(f"Leitura Pagina: {e}, erro na leitura da pagina {url}")
    finally:
        nv.quit()

    return dfPagina, dfDividendo


def main():

    db = database()
    db.truncate_table(tabela_dividendo)
    data = datetime.now().date()
    dfacoes = db.load_table_to_dataframe(tabela_acao) # getConfig(lista_B3)

    logger.info('*** INICIANDO LEITURA ***')


    for index, row in dfacoes.iterrows():
        #Criando url
        acao = row['cod_acao']
        url = f"https://statusinvest.com.br/acoes/{acao}"
        logger.info(f'Lendo {acao}, URL {url}')

        try:
            #Coletando infos
            pag, dividendo = le_pagina(url, acao, data)
            db.insertDB(tabela_coleta_acao, pag)
            db.insertDB(tabela_dividendo, dividendo)
            
        except Exception as e:
            logger.exception(f"Erro na coleta: {e}")

main()

