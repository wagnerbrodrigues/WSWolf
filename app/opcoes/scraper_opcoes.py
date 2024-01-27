import time
from datetime import datetime

from util.applogger import AppLogger
from db.database import database
from .config_opcoes_net import * 
from util.config import *
from util.navegador import Navegador


class scraper_opcoes:
    def __init__(self):
        self.dt_coleta = datetime.now().date()
        self.logger = AppLogger(log_scraper_opcoes)
        self.nv = Navegador(self.logger)
        self.db = database(self.logger)

    
    def prepara_pagina(self):
        self.logger.info("Preparando a pagina")
        # radio_call = self.nv.pegar_elemento_por_xpath(element_radio_call)
        # radio_call.click()

        self.logger.info("Ajustando ranges de valor")
        self.nv.move_slider(element_slidder_mais, 60)
        self.nv.move_slider(element_slidder_menos, -60)
        time.sleep(2)
        self.logger.info("Check inputs de data")
        self.checkbox_data()
        self.logger.info("Download Arquivo")
        self.nv.espere_click_element_xpath(element_botao_export)
        time.sleep(2)

    def checkbox_data(self):
        try:
            # Encontra todos os elementos "input" dentro da div
            input_element = self.nv.pegar_elementos_filhos_por_tag(element_div_datas, 'input')
 
            for checkbox in input_element:
                self.nv.marcar_checkbox(checkbox)
        except Exception as e: 
            self.logger.exception(f"Erro ao aplicar Checkbox de data: {e}")
        

    def limpa_diretorio(self):
        # Listar todos os arquivos na pasta
        arquivos = os.listdir(diretorio_downloads)

        # Percorrer a lista de arquivos e apagar um por um
        for arquivo in arquivos:
            caminho_completo = os.path.join(diretorio_downloads, arquivo)
            if os.path.isfile(caminho_completo):
                os.remove(caminho_completo)

    def main(self):
        self.logger.info('*** INICIANDO LEITURA ***')
        self.limpa_diretorio()
        score = [8,9,10]

        dfUltimaCarteira = self.db.load_table_to_dataframe_where_list(view_ultima_coleta, 'score', score )

        for index, row in dfUltimaCarteira.iterrows():
            acao = row['cod_acao']
            url = f"https://opcoes.net.br/opcoes/bovespa/{acao}"
            self.logger.info(f"Realizando a leitura de: {url}")

            #self.nv.driver.get(url)
            if not self.nv.abrir_pgina(url,element_div_datas):
                return None

            time.sleep(0.25)
            self.prepara_pagina()

        self.nv.fechar_driver()

if __name__ == "__main__":
    scpo = scraper_opcoes()
    scpo.main()
