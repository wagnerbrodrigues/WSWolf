from datetime import datetime
from tqdm import tqdm

from db.database import database
from util.applogger import AppLogger
from util.config import * 
from util.config_status_invest import * 
from model_status_invest import ModelStatusInvest

from util.config_inesting import *

import pandas as pd

class scraper_acoes:

    def __init__(self):
        self.dt_coleta = datetime.now().date()
        self.logger = AppLogger(log_scraper_acoes)
        self.db = database(self.logger)
        self.msi = ModelStatusInvest(self.logger)

    def controleColeta(self):
        try:
            url = 'https://statusinvest.com.br/acoes/'
            dfDtColeta = pd.DataFrame([[self.dt_coleta, url]], columns=['dt_coleta', 'url'])

            self.db.insertDB(tabela_controle_coleta, dfDtColeta)
        except Exception as e:
            self.logger.exception(f"Controle Coleta: {e}, erro ao inserir data controle {url}")

    
    def process_row(self, row):
        acao = row['cod_acao']
        urlinvesting = row['url']
        url = f"https://statusinvest.com.br/acoes/{acao}"
        
        self.logger.info(f'Lendo {acao}, URL {url}')
        try:
            if not self.msi.abrir_pgina(url, element_vlr_acao):
                return None
            
            dfPag = self.msi.indicadores_pagina(acao,self.dt_coleta)
            dfDividendo = self.msi.dividendo(acao, self.dt_coleta)

            # if urlinvesting != '':
            #    dfPag['beta'] = self.le_beta(urlinvesting)

            self.db.insertDB(tabela_coleta_acao, dfPag)
            self.db.insertDB(tabela_dividendo, dfDividendo)
        except Exception as e:
            self.logger.exception(f"Erro na coleta: {e}")
    
    def verifica_coleta(self):
        dfColeta = self.db.load_table_to_dataframe_where(tabela_controle_coleta,'dt_coleta', self.dt_coleta)
   
        return dfColeta.empty

    def main(self):

        if not self.verifica_coleta():
            self.logger.info(f"A coleta para a data {self.dt_coleta} já foi realizada")
            return None

        self.db.truncate_table(tabela_dividendo)
        
        dfacoes = self.db.load_table_to_dataframe(view_acao_url) 
        self.controleColeta()
        self.logger.info('*** INICIANDO LEITURA ***')

        tqdm.pandas()

        dfacoes.progress_apply(self.process_row, axis=1)

        self.msi.fechar_driver()


if __name__ == "__main__":
    scpp = scraper_acoes()
    scpp.main()