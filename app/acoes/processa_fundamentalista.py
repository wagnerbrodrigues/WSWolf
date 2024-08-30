import math
from db.database import database
from datetime import datetime
import pandas as pd
from tqdm import tqdm
from decimal import Decimal
from util.applogger import AppLogger
from sklearn.linear_model import LinearRegression

from util.config import * 

class fundamentalista:
    def __init__(self, fator_bazin=6, meses_bazin=60):
        self.logger = AppLogger(log_fundamentalista)
        self.db = database(self.logger)
        self._fator_bazin = fator_bazin
        self._meses_bazin = meses_bazin

    # Função para verificar se a tendência é de alta (crescente)
    def tendencia_crescente(self, df: pd.DataFrame, campo_vlr: str, campo_data: str) -> bool:
        df[campo_data] = pd.to_datetime(df[campo_data])
        df['data_ordinal'] = df[campo_data].map(pd.Timestamp.toordinal)

        X = df['data_ordinal'].values.reshape(-1, 1)
        y = df[campo_vlr].values

        model = LinearRegression().fit(X, y)
        coef = model.coef_[0]

        return coef > 0
        
    def indicadores_fundamentalistas(self, row: pd.Series):
        score = 0
        PL = row['pl']
        volume_diario = row['vlm_diario']
        DY = row['dy']
        bazin = row['bazin12']
        valor_atual = row['vlr_acao']
        vlr_intrinseco = row['vlr_intrinseco']
        vlr_teto_margem = row['vlr_teto_margem']
        ROE = row['roe']
        PVP = row['pvp']
        pebit = row['pebit']
        dlebit = row['dlebit']
        tag_along = row['tag_along']
        VPA = row['vpa']
        deductions = []  # Utiliza uma lista para acumular as deduções

        #empresa inoperavel 
        # if volume_diario < 3000000.00: return 0, ""

        df_lpa = self.db.load_table_to_dataframe_where(tabela_coleta_acao, 'cod_acao', row['cod_acao'])
        
        if self.tendencia_crescente(df_lpa,'lpa','dt_coleta'):
            score += 1
        else:
            deductions.append("lpa")

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
        if ROE > 12:
            score += 1
        else:
            deductions.append("ROE")

        # Avaliação de DY
        if DY >= self._fator_bazin:
            score += 1
        else:
            deductions.append("DY")

        # Avaliação de DY
        if bazin > valor_atual:
            score += 1
        else:
            deductions.append("bazin")

        # Avaliação de DY
        if vlr_teto_margem > valor_atual:
            score += 1
        else:
            deductions.append("teto_margem")
    

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

        # Avaliação de VPA
        if vlr_intrinseco > valor_atual:
            score += 1
        else:
            deductions.append("vlr_intrinseco")

        # Avaliação de dlebit
        if dlebit >= 0 and dlebit < 3: 
            score += 1
        elif dlebit < 0 and pebit > 0: 
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
    

    def calcular_valor_intrinseco(self, vpa, lpa) -> float:
        # Se existirem valores negativos, não retorna o calculo
        if vpa < 0 or lpa < 0:
            return float(0)

        try:
            result = math.sqrt(22.5 * vpa * lpa)
            return float(result)
        except ValueError as e:
            print(e)
            return float(0)

    def media_por_periodo(self, df: pd.DataFrame, coluna_valor='vlr') -> float:
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


    def calculo_Bazin(self, df: pd.DataFrame) -> float:
        media = self.media_por_periodo(df)
        result = (media * 100) / self._fator_bazin
        return float(result)

    def valor_teto_margem(self, row: pd.Series)-> float:
        valor_intrinseco = row['vlr_intrinseco']
        bazin12 = row['bazin12']
        menor_valor = min(valor_intrinseco, bazin12) 
        return float(menor_valor * 0.9)
  
    def main(self) -> None:
        dfinfo_acoes = self.db.load_table_to_dataframe(view_ultima_coleta)

        tqdm.pandas()

        for index, row in tqdm(dfinfo_acoes.iterrows(), total=len(dfinfo_acoes), desc="Processando linhas"):
            acao = row['cod_acao']
            self.logger.info(f'Processando fundamentalista: {acao}')

            dfDividendo = self.db.load_table_to_dataframe_where(tabela_dividendo, 'cod_acao', acao)

            dfinfo_acoes.at[index, 'vlr_intrinseco'] = self.calcular_valor_intrinseco(row['vpa'], row['lpa'])
            dfinfo_acoes.at[index, 'bazin12'] = self.calculo_Bazin(dfDividendo)
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