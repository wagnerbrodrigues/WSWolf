import time
import pandas as pd
from datetime import datetime

from util.applogger import AppLogger
from mysql.database import database
from util.config_opcoes_net import * 
from util.navegador import Navegador


class scraper_opcoes:
    def __init__(self):
        self.dt_coleta = datetime.now().date()
        self.logger = AppLogger(log_scraper_opcoes)
        self.nv = Navegador(chromeDriver,self.logger)
        self.db = database(self.logger)

    
    def prepara_pagina(self):
        self.logger.info("Preparando a pagina")
        radio_call = self.nv.pegar_elemento_por_xpath(element_radio_call)
        radio_call.click()

        self.logger.info("Ajustando ranges de valor")
        self.nv.move_slider(element_slidder_mais, 60)
        self.nv.move_slider(element_slidder_menos, -60)
        time.sleep(2)
        self.logger.info("Check inputs de data")
        self.checkbox_data()
        self.logger.info("Download Arquivo")
        self.nv.espere_click_element_xpath(element_botao_export)

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


    def pega_ultimo_arquivo(self, acao):
        lista_arquivo = os.listdir(diretorio_downloads)

        arquivo_acao = [arquivo for arquivo in lista_arquivo if arquivo.endswith(".xlsx") and acao in arquivo]

        # Ordena a lista de arquivos filtrados pela data de modificação (o último arquivo estará no final da lista)
        arquivo_acao.sort(key=lambda x: os.path.getmtime(os.path.join(diretorio_downloads, x)))

        # Obtém o último arquivo .xlsx da lista
        return os.path.join(diretorio_downloads, arquivo_acao[-1])


    def le_arquivo(self, acao):
        nome_arquivo = self.pega_ultimo_arquivo(acao)
        return pd.read_excel(nome_arquivo, skiprows=1)
    

    def main(self):
        self.logger.info('*** INICIANDO LEITURA ***')
        self.limpa_diretorio()

        dfUltimaCarteira = self.db.load_table_to_dataframe(view_ultima_carteira)

        for index, row in dfUltimaCarteira.iterrows():
            acao = row['cod_acao']
            url = f"https://opcoes.net.br/opcoes/bovespa/{acao}"
            self.logger.info(f"Realizando a leitura de: {url}")

            self.nv.driver.get(url)
            if not self.nv.pagina_ativa(element_div_datas):
                return None

            time.sleep(0.25)
            self.prepara_pagina()

        self.nv.fechar_driver()

if __name__ == "__main__":
    scpo = scraper_opcoes()
    scpo.main()
