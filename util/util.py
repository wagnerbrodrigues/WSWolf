import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from util.config import * 

def corrigir_formato_data(df, coluna_data):
    df[coluna_data] = pd.to_datetime(df[coluna_data], dayfirst=True, errors='coerce').dt.strftime("%Y-%m-%d")
    return df

def pagina_ativa(xpath, nv):
    #'//*[@id="main-2"]/div[2]/div/div[1]/div/div[1]/div/div[1]/strong'
    try:
        WebDriverWait(nv, 0.25).until(EC.presence_of_element_located((By.XPATH, xpath)))
        return True
    except (NoSuchElementException, TimeoutException) as e :
        print(e)
        return False 
    
def get_navegator():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")

    service = Service(chromeDriver)  # Insira o caminho para o chromedriver
    return webdriver.Chrome(service=service, options=options)  

        #  dfPagina = pd.DataFrame({
        #         'dt_coleta': self.dt_coleta,
        #         'cod_acao' : acao,
        #         'vlr_acao' : [self.tryCast(self.nv.pegar_elemento_por_xpath('//*[@id="main-2"]/div[2]/div/div[1]/div/div[1]/div/div[1]/strong'))],
        #         'vlm_diario' : [self.tryCast(self.nv.pegar_elemento_por_xpath('/html/body/main/div[2]/div/div[5]/div/div/div[3]/div/div/div/strong'))],
        #         'dy' : [self.tryCast(self.nv.pegar_elemento_por_xpath( '/html/body/main/div[2]/div/div[1]/div/div[4]/div/div[1]/strong'))],
        #         'pl' : [self.tryCast(self.nv.pegar_elemento_por_xpath( '/html/body/main/div[2]/div/div[7]/div[2]/div/div[1]/div/div[2]/div/div/strong'))],
        #         'pvp' : [self.tryCast(self.nv.pegar_elemento_por_xpath( '/html/body/main/div[2]/div/div[7]/div[2]/div/div[1]/div/div[4]/div/div/strong'))],
        #         'vpa' : [self.tryCast(self.nv.pegar_elemento_por_xpath( '/html/body/main/div[2]/div/div[7]/div[2]/div/div[1]/div/div[9]/div/div/strong'))],
        #         'roe' : [self.tryCast(self.nv.pegar_elemento_por_xpath( '/html/body/main/div[2]/div/div[7]/div[2]/div/div[4]/div/div[1]/div/div/strong'))],
        #         'lpa' : [self.tryCast(self.nv.pegar_elemento_por_xpath( '/html/body/main/div[2]/div/div[7]/div[2]/div/div[1]/div/div[11]/div/div/strong'))],
        #         'pebit':  [self.tryCast(self.nv.pegar_elemento_por_xpath( '/html/body/main/div[2]/div/div[7]/div[2]/div/div[1]/div/div[8]/div/div/strong'))]
        #     })