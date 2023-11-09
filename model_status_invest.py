import pandas as pd
from util.config_status_invest import * 
from util.navegador import Navegador

class ModelStatusInvest(Navegador):
    def __init__(self, logger):
        super().__init__(logger)

    def indicadores_pagina(self, acao, dt_coleta):

        data = {   
            'cod_acao': acao,
            'dt_coleta': dt_coleta,
            'vlr_acao' : [super().pegar_valor_numerico_elemento_por_xpath(element_vlr_acao)],
            'vlm_diario' : [super().pegar_valor_numerico_elemento_por_xpath(element_vlm_diario)],
            'dy' : [super().pegar_valor_numerico_elemento_por_xpath(element_dy)],
            'pl' : [super().pegar_valor_numerico_elemento_por_xpath(element_pl)],
            'pvp' : [super().pegar_valor_numerico_elemento_por_xpath(element_pvp)],
            'vpa' : [super().pegar_valor_numerico_elemento_por_xpath(element_vpa)],
            'roe' : [super().pegar_valor_numerico_elemento_por_xpath(element_roe)],
            'lpa' : [super().pegar_valor_numerico_elemento_por_xpath(element_lpa)],
            'pebit':  [super().pegar_valor_numerico_elemento_por_xpath(element_pebit)] ,
            'dlebit':  [super().pegar_valor_numerico_elemento_por_xpath(element_dlebit)] 
        }
        df = pd.DataFrame(data)
        return df
    
    def corrigir_formato_data(self, df, coluna_data):
        df[coluna_data] = pd.to_datetime(df[coluna_data], dayfirst=True, errors='coerce').dt.strftime("%Y-%m-%d")
        df[coluna_data] = df[coluna_data].apply(lambda x: x if pd.notna(x) else None)
        return df
    
    def _parse_dividendo(self, str_dividendo, acao, dt_coleta):
        try:
            dfDividendo = pd.read_json(str_dividendo)

            dfDividendo = dfDividendo.rename(columns={
            'ed': 'dt_comunicado',
            'pd': 'dt_pagamento',
            'et': 'tp_dividendo',
            'v': 'vlr'
            })

            dfDividendo =  self.corrigir_formato_data(dfDividendo, 'dt_comunicado')
            dfDividendo =  self.corrigir_formato_data(dfDividendo, 'dt_pagamento')

            columns_to_remove = ['y', 'm', 'd', 'ad', 'etd', 'ov', 'sv', 'sov', 'adj']
            dfDividendo = dfDividendo.drop(columns=columns_to_remove)
            dfDividendo['cod_acao'] = acao 
            dfDividendo['dt_coleta'] = dt_coleta 
            
        except Exception as e:
            self.logger.exception(f"Erro no parse de dividendos de {acao}, erro: {e}")
        finally:
            return dfDividendo
    
    def dividendo(self, acao, dt_coleta):
        dfDividendo = pd.DataFrame()

        try:
            results = super().pegar_elemento_por_id('results')
            dividendo_raw = results.get_attribute('value')

            if not dividendo_raw or dividendo_raw == '[]':
                return dfDividendo
            
            dfDividendo = self._parse_dividendo(dividendo_raw, acao, dt_coleta)
        
        except Exception as e:
           self.logger.exception(f'Erro ao obter dividendos de {acao}')

        finally:
            return dfDividendo