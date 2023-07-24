from util.config import * 
from util.util import * 

from util.applogger import AppLogger
from util.database import database

from datetime import datetime
from tqdm import tqdm

from util.util import * 
from util.config_status_invest import * 
from util.navegador import Navegador

class scrapper_opcoes:
    def __init__(self):
        self.dt_coleta = datetime.now().date()
        self.logger = AppLogger(log_scrapper_opcoes)
        self.nv = Navegador(chromeDriver,self.logger)
        self.db = database(self.logger)
        
    def main(self):
        self.logger.info('*** INICIANDO LEITURA ***')

        tqdm.pandas()
        url = 'https://statusinvest.com.br/acoes/PETR4'
        self.nv.driver.get(url)

        if self.nv.pagina_ativa(element_vlr_acao):
            print("Pagina")
         
        self.nv.fechar_driver()

if __name__ == "__main__":
    scpp = scrapper_opcoes()
    scpp.main()