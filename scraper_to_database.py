import os
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
currentDir = os.path.dirname(__file__) + "\\"
lista_B3 = currentDir + "acoes.json"
confi_pag = currentDir + "mapa_pag.json"
chromeDriver = currentDir + "driver_selenium\\chromedriver.exe"
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

def parseDividento(str_dividendo, acao):
    try:
        dfDividendo = pd.read_json(str_dividendo)

        dfDividendo = dfDividendo.rename(columns={
        'ed': 'data_comunicado',
        'pd': 'data_pagamento',
        'et': 'tipo',
        'v': 'valor'
        })
        dfDividendo['data_comunicado'] = pd.to_datetime(dfDividendo['data_comunicado'], dayfirst=True, errors='coerce').dt.strftime("%Y-%m-%d")
        dfDividendo['data_pagamento'] = pd.to_datetime(dfDividendo['data_pagamento'], dayfirst=True, errors='coerce').dt.strftime("%Y-%m-%d")

        columns_to_remove = ['y', 'm', 'd', 'ad', 'etd', 'ov', 'sv', 'sov', 'adj']
        dfDividendo = dfDividendo.drop(columns=columns_to_remove)
        dfDividendo['acao'] = acao 
        
    except Exception as e:
        logger.exception(f"Erro no parse de dividendos de {acao}, erro: {e}")

    return dfDividendo

def corrigir_formato_data(df, coluna_data):
    df[coluna_data] = pd.to_datetime(df[coluna_data], dayfirst=True).dt.strftime("%Y-%m-%d")
    return df

def le_pagina(url, acao, data):
    nv = navegator()
    nv.get(url)
    time.sleep(0.25)

    try:
        dfPagina = pd.DataFrame({
            'data_coleta': data,
            'acao' : acao,
            'valor_atual' : [tryCast(nv.find_element(By.XPATH, '//*[@id="main-2"]/div[2]/div/div[1]/div/div[1]/div/div[1]/strong').text)],
            'volume_diario' : [tryCast(nv.find_element(By.XPATH, '/html/body/main/div[2]/div/div[5]/div/div/div[3]/div/div/div/strong').text)],
            'dy' : [tryCast(nv.find_element(By.XPATH, '/html/body/main/div[2]/div/div[1]/div/div[4]/div/div[1]/strong').text)],
            'pl' : [tryCast(nv.find_element(By.XPATH, '/html/body/main/div[2]/div/div[7]/div[2]/div/div[1]/div/div[2]/div/div/strong').text)],
            'setor' : [nv.find_element(By.XPATH, '/html/body/main/div[5]/div[1]/div/div[3]/div/div[1]/div/div/div/a/strong').text],
            'pvp' : [tryCast(nv.find_element(By.XPATH, '/html/body/main/div[2]/div/div[7]/div[2]/div/div[1]/div/div[4]/div/div/strong').text)],
            'vpa' : [tryCast(nv.find_element(By.XPATH, '/html/body/main/div[2]/div/div[7]/div[2]/div/div[1]/div/div[9]/div/div/strong').text)],
            'roe' : [tryCast(nv.find_element(By.XPATH, '/html/body/main/div[2]/div/div[7]/div[2]/div/div[4]/div/div[1]/div/div/strong').text)],
            'lpa' : [tryCast(nv.find_element(By.XPATH, '/html/body/main/div[2]/div/div[7]/div[2]/div/div[1]/div/div[11]/div/div/strong').text)],
            'pebit':  [tryCast(nv.find_element(By.XPATH, '/html/body/main/div[2]/div/div[7]/div[2]/div/div[1]/div/div[8]/div/div/strong').text)]
        })

        #le dividendos
        results = nv.find_element(By.ID, 'results')
        dividendos_raw = results.get_attribute('value')
        dfDividendos = parseDividento(dividendos_raw, acao)
        

    except Exception as e:
        logger.exception(f"Leitura Pagina: {e}, erro na leitura da pagina {url}")
    finally:
        nv.quit()

    return dfPagina, dfDividendos


def main():

    lista_acao = getConfig(lista_B3)
    db = database()
    db.truncate_tables()
    data = datetime.now().date()
    logger.info('*** INICIANDO LEITURA ***')


    for acao in lista_acao:
        #Criando url
        url = f"https://statusinvest.com.br/acoes/{acao}"
        logger.info(f'Lendo {acao}, URL {url}')

        try:
            #Coletando infos
            pag, dividendos = le_pagina(url, acao, data)
            db.insertDB("info_acoes", pag)
            db.insertDB("dividendos", dividendos)
            
        except Exception as e:
            print(e)

main()

