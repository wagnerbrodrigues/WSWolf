import math
from db.database import database
from datetime import datetime
import pandas as pd
from tqdm import tqdm
from decimal import Decimal
from util.applogger import AppLogger

from util.config import * 


class fundamentalista:
    def __init__(self, fator_bazin=6, meses_bazin=60):
        self.logger = AppLogger(log_fundamentalista)
        self.db = database(self.logger)
        self._fator_bazin = fator_bazin
        self._meses_bazin = meses_bazin
        
    def indicadores_fundamentalistas(self, row):
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
        deductions = []  # Utiliza uma lista para acumular as deduções

        #empresa inoperavel 
        if volume_diario < 3000000.00: return 0, ""

        # Avaliação de PL
        if PL < 10 and PL > 0:
            score += 1
        else :
            score -= 1
            deductions.append("PL")

        # Avaliação de pebit
        if pebit < 10 and pebit > 0:
            score += 1
        else:
            deductions.append("pebit")

        # Avaliação de ROE
        if ROE > 0:
            score += 1
        else:
            deductions.append("ROE")

        # Avaliação de DY
        if DY >= self._fator_bazin:
            score += 1
        else:
            deductions.append("DY")

        # Avaliação de PVP
        if PVP > 0 and PVP < 1:
            score += 1
        elif PVP > 2:
            score -= 1
            deductions.append("PVP")
        else:
            deductions.append("PVP")

        # Avaliação de VPA
        if VPA > valor_atual:
            score += 1
        else:
            deductions.append("VPA")

        # Avaliação de dlebit
        if dlebit >= 0 and dlebit < 3: 
            score += 1
        else:
            deductions.append("dlebit")

        # Avaliação de tag_along
        if tag_along == 100:
            score += 1
        elif tag_along == 0:
            score -= 1
            deductions.append("tag_along")
        else:
            deductions.append("tag_along")

        # Converte a lista de deduções para uma string separada por vírgulas
        deduction_string = ", ".join(deductions)

        return score, deduction_string
    

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

    def media_por_periodo(self, df, coluna_valor='vlr') -> float:
        # Garantir que a coluna 'dt_comunicado' está no formato datetime
        df['dt_comunicado'] = pd.to_datetime(df['dt_comunicado'], errors='coerce')

        # Calcular a data inicial para o cálculo da média
        data_inicial = datetime.now() - pd.DateOffset(months=self._meses_bazin)

        # Filtrar o DataFrame para registros dentro do período desejado
        df_filtrado = df[df['dt_comunicado'] >= data_inicial]

        # Calcular o número de anos no período
        anos_periodo = self._meses_bazin / 12

        # Calcular a média dos valores
        if anos_periodo > 0 and not df_filtrado.empty:
            media_valores = df_filtrado[coluna_valor].sum() / anos_periodo
        else:
            media_valores = 0  # Evita divisão por zero e retorna 0 se não há dados suficientes

        return float(media_valores)


    def calculo_Bazin(self, df) -> float:
        media = self.media_por_periodo(df)
        result = (media * 100) / self._fator_bazin
        return float(result)

    def valor_teto_margem(self, row)-> float:
        valor_intrinseco = row['vlr_intrinseco']
        bazin12 = row['bazin12']
        #bazin36 = row['bazin36']
        #bazin60 = row['bazin60']
        #determina o menor valor encontrado para a acao
        menor_valor = min(valor_intrinseco, bazin12) #, bazin36, bazin60)
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
            dfinfo_acoes.at[index, 'bazin12'] = self.calculo_Bazin(dfDividendo)
            # dfinfo_acoes.at[index, 'bazin36'] = self.calculo_Bazin(dfDividendo, 3)
            # dfinfo_acoes.at[index, 'bazin60'] = self.calculo_Bazin(dfDividendo, 5)
            dfinfo_acoes.at[index, 'vlr_teto_margem'] = self.valor_teto_margem(dfinfo_acoes.iloc[index])
            score, mot_ded_score = self.indicadores_fundamentalistas(dfinfo_acoes.iloc[index])
            dfinfo_acoes.at[index, 'score'] = score
            dfinfo_acoes.at[index, 'mot_ded_score'] = mot_ded_score
  
        dfinfo_acoes = dfinfo_acoes.drop(columns=['setor', 'segto_atua'])

        condicoes = ['cod_acao', 'dt_coleta']
        self.db.updateDB(tabela_coleta_acao, dfinfo_acoes, condicoes)

if __name__ == "__main__":
    fund = fundamentalista()
    fund.main()