import math
from db.database import database
from datetime import datetime
import pandas as pd
from util.applogger import AppLogger
from decimal import Decimal

from util.config import * 

from tqdm import tqdm

class fundamentalista:
    def __init__(self, fator_bazin=6):
        self.logger = AppLogger(log_fundamentalista)
        self.db = database(self.logger)
        self.fator_bazin = fator_bazin
        
    def indicadores_fundamentalistas(self, row) -> int:
        score = 0
        PL = row['pl']
        volume_diario = row['vlm_diario']
        DY = row['dy']
        valor_atual = row['vlr_acao']
        ROE = row['roe']
        PVP = row['pvp']
        pebit = row['pebit']
        dlebit = row['dlebit']
        tag_along = row['tag_along']
        VPA = row['vpa']

        #empresa inoperavel 
        if volume_diario < 3000000.00: return 0

        #score indicadores
        if PL < 10 and PL > 0 : score += 1
        if PL < 0: score -= 1
        if pebit < 10 and pebit > 0 : score += 1
        if pebit < 0: score -= 1
        if ROE > 0 : score += 1
        if DY > 6: score += 1
        if PVP > 2: score -= 1
        if VPA > valor_atual: score -= 1
        if PVP > 0 and PVP < 1: score += 1
        if dlebit > 0 and dlebit < 3: score += 1

        if tag_along == 100 : score += 1
        if tag_along == 0 : score -= 1

        return score


    def calcular_valor_intrinseco(self, vpa, lpa) :
        # Se existirem valores negativos, não retorna o calculo
        if vpa < 0 or lpa < 0:
            return float(0)

        try:
            result = math.sqrt(22.5 * vpa * lpa)
            return float(result)
        except ValueError as e:
            print(e)
            return float(0)

    def media_por_periodo(self, df, num_periodos) -> float:
        # Garantir que a coluna 'dt_comunicado' está no formato datetime
        df['dt_comunicado'] = pd.to_datetime(df['dt_comunicado'], errors='coerce')

        # Calcular a data inicial para o cálculo da média
        data_inicial = datetime.now() - pd.DateOffset(months=12 * num_periodos)

        # Filtrar o DataFrame para registros dentro do período desejado
        df_filtrado = df[df['dt_comunicado'] >= data_inicial]

        # Calcular a média dos valores
        media_valores = df_filtrado['vlr'].sum() / num_periodos

        return float(media_valores)


    def calculo_Bazin(self, df, periodo) -> float:
        media = self.media_por_periodo(df, periodo)
        result = (media * 100) / self.fator_bazin
        return float(result)

    def valor_teto_margem(self, row)-> float:
        valor_intrinseco = row['vlr_intrinseco']
        bazin12 = row['bazin12']
        bazin36 = row['bazin36']
        bazin60 = row['bazin60']
        #determina o menor valor encontrado para a acao
        menor_valor = min(valor_intrinseco, bazin12, bazin36, bazin60)
        #margem de 10% para a compra, em cima do menor valor
        return float(menor_valor * 0.9)
    
   
    def main(self) -> None:
        dfinfo_acoes = self.db.load_table_to_dataframe(view_ultima_coleta)
        dfDividendo = self.db.load_table_to_dataframe(tabela_dividendo)
        tqdm.pandas()

        for index, row in tqdm(dfinfo_acoes.iterrows(), total=len(dfinfo_acoes), desc="Processando linhas"):
            acao = row['cod_acao']
            dfDividendo = self.db.load_table_to_dataframe_where(tabela_dividendo, 'cod_acao', acao)

            dfinfo_acoes.at[index, 'vlr_intrinseco'] = self.calcular_valor_intrinseco(row['vpa'], row['lpa'])
            dfinfo_acoes.at[index, 'bazin12'] = self.calculo_Bazin(dfDividendo, 1)
            dfinfo_acoes.at[index, 'bazin36'] = self.calculo_Bazin(dfDividendo, 3)
            dfinfo_acoes.at[index, 'bazin60'] = self.calculo_Bazin(dfDividendo, 5)
            dfinfo_acoes.at[index, 'vlr_teto_margem'] = self.valor_teto_margem(dfinfo_acoes.iloc[index])
            dfinfo_acoes.at[index, 'score'] = self.indicadores_fundamentalistas(dfinfo_acoes.iloc[index])

  
        dfinfo_acoes = dfinfo_acoes.drop(columns=['setor', 'segto_atua'])

        condicoes = ['cod_acao', 'dt_coleta']
        self.db.updateDB(tabela_coleta_acao, dfinfo_acoes, condicoes)

if __name__ == "__main__":
    fund = fundamentalista()
    fund.main()