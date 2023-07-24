import pandas as pd
from datetime import datetime
from tqdm import tqdm

from util.database import database
from util.applogger import AppLogger

from util.config import * 
from util.util import * 
from util.config_status_invest import * 
from util.navegador import Navegador

class scrapper_acoes:

    def __init__(self):
        self.dt_coleta = datetime.now().date()
        self.logger = AppLogger(log_scrapper_acoes)
        self.db = database(self.logger)
        self.nv = Navegador(chromeDriver,self.logger)

    def tryCast(self, valor):
        try:
            valor = valor.replace(".","")
            valor = valor.replace(",",".")
            valor = valor.replace("%", "")
            return float(valor)
        except:
            return 0

    def parseDividento(self, str_dividendo, acao):
        try:
            dfDividendo = pd.read_json(str_dividendo)

            dfDividendo = dfDividendo.rename(columns={
            'ed': 'dt_comunicado',
            'pd': 'dt_pagamento',
            'et': 'tp_dividendo',
            'v': 'vlr'
            })

            dfDividendo =  corrigir_formato_data(dfDividendo, 'dt_comunicado')
            dfDividendo =  corrigir_formato_data(dfDividendo, 'dt_pagamento')

            columns_to_remove = ['y', 'm', 'd', 'ad', 'etd', 'ov', 'sv', 'sov', 'adj']
            dfDividendo = dfDividendo.drop(columns=columns_to_remove)
            dfDividendo['cod_acao'] = acao 
            dfDividendo['dt_coleta'] = self.dt_coleta 
            
        except Exception as e:
            self.logger.exception(f"Erro no parse de dividendos de {acao}, erro: {e}")
        finally:
            return dfDividendo
    
    def le_pagina(self, acao):
        dfPagina = pd.DataFrame()
        try:
            dfPagina = pd.DataFrame({
                'dt_coleta': self.dt_coleta,
                'cod_acao' : acao,
                'vlr_acao' : [self.tryCast(self.nv.pegar_elemento_por_xpath( element_vlr_acao))],
                'vlm_diario' : [self.tryCast(self.nv.pegar_elemento_por_xpath( element_vlm_diario))],
                'dy' : [self.tryCast(self.nv.pegar_elemento_por_xpath( element_dy))],
                'pl' : [self.tryCast(self.nv.pegar_elemento_por_xpath( element_pl))],
                'pvp' : [self.tryCast(self.nv.pegar_elemento_por_xpath( element_pvp))],
                'vpa' : [self.tryCast(self.nv.pegar_elemento_por_xpath( element_vpa))],
                'roe' : [self.tryCast(self.nv.pegar_elemento_por_xpath( element_roe))],
                'lpa' : [self.tryCast(self.nv.pegar_elemento_por_xpath( element_lpa))],
                'pebit':  [self.tryCast(self.nv.pegar_elemento_por_xpath( element_pebit))]
            })

        except Exception as e:
            self.logger.exception(f"Leitura Pagina: {e}, erro na leitura da pagina {self.nv.driver.current_url}")
        finally:
            return dfPagina
        
    
    def le_dividendo(self, acao):
        dfDividendo = pd.DataFrame()

        try:
            results = self.nv.pegar_elemento_por_id('results')
            dividendo_raw = results.get_attribute('value')

            if not dividendo_raw or dividendo_raw == '[]':
                return dfDividendo
            
            dfDividendo = self.parseDividento(dividendo_raw, acao)
        
        except Exception as e:
           self.logger.exception(f'Erro ao obter dividendos de {acao}')

        finally:
            return dfDividendo
        

    def controleColeta(self):
        # Seu código para coletar os dados da URL usando o campo dt_coleta
        # e converter em um DataFrame
        try:
        # Exemplo de código para criar um DataFrame vazio
            dfDtColeta = pd.DataFrame(columns=['dt_coleta', 'url'])  # Substitua 'coluna1' e 'coluna2' com as colunas reais
            url = 'https://statusinvest.com.br/acoes/'
            dfDtColeta = pd.DataFrame([[self.dt_coleta, url]], columns=dfDtColeta.columns)
            

            self.db.insertDB(tabela_controle_coleta, dfDtColeta)
        except Exception as e:
            self.logger.exception(f"Controle Coleta: {e}, erro ao inserir data controle {url}")

    def process_row(self, row):
        acao = row['cod_acao']
        url = f"https://statusinvest.com.br/acoes/{acao}"
        
        self.logger.info(f'Lendo {acao}, URL {url}')
        try:
            self.nv.driver.get(url)

            if not self.nv.pagina_ativa(element_vlr_acao):
                return None

            dfPag = self.le_pagina(acao)
            dfDividendo = self.le_dividendo(acao)

            self.db.insertDB(tabela_coleta_acao, dfPag)
            self.db.insertDB(tabela_dividendo, dfDividendo)
        except Exception as e:
            self.logger.exception(f"Erro na coleta: {e}")
    


    def main(self):
        self.db.truncate_table(tabela_dividendo)
        
        dfacoes = self.db.load_table_to_dataframe(tabela_acao) 
        self.controleColeta()
        self.logger.info('*** INICIANDO LEITURA ***')

        tqdm.pandas()

        dfacoes.progress_apply(self.process_row, axis=1)

        self.nv.fechar_driver()


if __name__ == "__main__":
    scpp = scrapper_acoes()
    scpp.main()