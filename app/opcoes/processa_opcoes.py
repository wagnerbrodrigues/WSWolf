import time
import pandas as pd
from datetime import datetime

from util.applogger import AppLogger
from db.database import database
from .config_opcoes_net import * 
from util.config import *

class processa_opcoes:
    def __init__(self):
        self.dt_coleta = datetime.now().date()
        self.logger = AppLogger(log_processa_opcoes)
        self.db = database(self.logger)
        self.dt_coleta = datetime.now().date()

    def pega_arquivo(self, cod_acao):
        lista_arquivos = os.listdir(diretorio_downloads)
        arquivos = [os.path.join(diretorio_downloads, arquivo) for arquivo in lista_arquivos if arquivo.endswith(".xlsx")]
        for arquivo in arquivos:
            if cod_acao in arquivo:
                return arquivo
            
        self.logger.warning(f'Ativo {cod_acao} não tem arquivo')
        return None  # Retorna None se nenhum arquivo corresponder ao valor cod_acao

    def le_arquivos(self):
        # Inicializa um DataFrame vazio
        df_final = pd.DataFrame()
        dfUltimaCarteira = self.db.load_table_to_dataframe(view_ultima_coleta)

        for _, row in dfUltimaCarteira.iterrows():
            try:
                arquivo = self.pega_arquivo(row['cod_acao'])
                if arquivo:
                    df = pd.read_excel(arquivo, skiprows=1, dtype=str)
                    df['cod_acao'] = row['cod_acao']
                    df_final = pd.concat([df_final, df], ignore_index=True)
            except Exception as e:
                self.logger.exception(f"Erro ao ler o arquivo {arquivo}: {e}")
        
        return df_final    
    
    def formata_coluna_valor(self, value):
        if isinstance(value, float):
            return '{:.2f}'.format(value).replace('.', '')
        elif isinstance(value, int):
            return '{:.2f}'.format(value / 100).replace('.', '')
        else:
            return value


    def main(self):
        dfOpcoes = self.le_arquivos()

        column_mapping = {
            'cod_acao' : 'cod_acao', 
            'Ticker': 'cod_opcao',
            'Vencimento': 'dt_vencimento',
            'Dias úteis': 'dias_uteis',
            'Tipo' : 'tp_contrato',
            'F.M.': 'ind_formador_mercado',
            'Mod.': 'tp_opcao',
            'Strike': 'strike',
            'A/I/OTM': 'moneyness',
            'Dist. (%) do Strike': 'dist_strike_pct',
            'Último': 'ult_vlr',
            'Var. (%)': 'variacao_pct',
            'Var.\xa0(%)': 'variacao_pct',
            'Data/Hora': 'dt_ult_negocio',
            'Núm. de Neg.': 'num_negocio',
            'Vol. Financeiro': 'vol_finc',
            'Vol. Impl. (%)': 'vol_impl_pct',
            'Delta': 'delta',
            'Gamma': 'gamma',
            'Theta ($)': 'theta_vlr',
            'Theta (%)': 'theta_pct',
            'Vega': 'vega',
            'IQ': 'in_the_money',
            'Coberto': 'coberto',
            'Travado': 'travado',
            'Descob.': 'descoberto',
            'Tit.': 'titulares',
            'Lanç.': 'lancadores',
        }

        dfOpcoes.columns = dfOpcoes.columns.str.strip()

        dfOpcoes = dfOpcoes.rename(columns=column_mapping)
        dfOpcoes.dropna(subset=['ult_vlr'], inplace=True)

        dfOpcoes['ult_vlr'] = dfOpcoes['ult_vlr'].apply(lambda x: str(x).zfill(3)[:-2] + '.' + str(x).zfill(3)[-2:])
        dfOpcoes['strike'] = dfOpcoes['strike'].apply(lambda x: str(x).zfill(3)[:-2] + '.' + str(x).zfill(3)[-2:])
        dfOpcoes['vol_finc'] = dfOpcoes['vol_finc'].str.replace(',', '').str.replace('.', '')
        dfOpcoes['vol_finc'] = pd.to_numeric(dfOpcoes['vol_finc'])
        dfOpcoes['dt_vencimento'] = pd.to_datetime(dfOpcoes['dt_vencimento'], format='%d/%m/%Y').dt.strftime('%Y-%m-%d')
        dfOpcoes['dt_ult_negocio'] = pd.to_datetime(dfOpcoes['dt_ult_negocio'], format='%d/%m/%Y').dt.strftime('%Y-%m-%d')

        dfOpcoes['dt_coleta'] = self.dt_coleta
        self.db.truncate_table('opcoes_mercado')

        self.db.insertDB('opcoes_mercado', dfOpcoes)      

if __name__ == "__main__":
    po = processa_opcoes()
    po.main()
