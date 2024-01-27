from datetime import datetime
from tqdm import tqdm

from db.database import database
from util.applogger import AppLogger
from util.config import * 
from .config_status_invest import * 
from .model_status_invest import ModelStatusInvest
import time

import pandas as pd

class scraper_acoes:

    def __init__(self):
        self.dt_coleta = datetime.now().date()
        self.logger = AppLogger(log_scraper_acoes)
        self.db = database(self.logger)
        self.msi = ModelStatusInvest(self.logger)
    
    def process_row(self, row):
        acao = row['cod_acao']
        #urlinvesting = row['url']
        url = f"https://statusinvest.com.br/acoes/{acao}"
        
        self.logger.info(f'Lendo {acao}, URL {url}')
        try:
            if not self.msi.abrir_pgina(url, element_vlr_acao):
                return None
            
            dfPag = self.msi.indicadores_pagina(acao,self.dt_coleta)
            dfDividendo = self.msi.dividendo(acao, self.dt_coleta)
            time.sleep(1)

            self.db.insertDB(tabela_coleta_acao, dfPag)
            self.db.delete_from_table_where(tabela_dividendo,'cod_acao',acao)
            self.db.insertDB(tabela_dividendo, dfDividendo)
        except Exception as e:
            self.logger.exception(f"Erro na coleta: {e}")
    

    def main(self):
        dfacoes = self.db.load_table_to_dataframe(view_lista_para_coleta) 
        tqdm.pandas()
        tempo = 0

        while not dfacoes.empty or tempo == 100:
            self.logger.info('*** INICIANDO LEITURA ***')
            dfacoes.progress_apply(self.process_row, axis=1)
            dfacoes = self.db.load_table_to_dataframe(view_lista_para_coleta)
            tempo += 10
            time.sleep(tempo)

        self.msi.fechar_driver()


if __name__ == "__main__":
    scpp = scraper_acoes()
    scpp.main()