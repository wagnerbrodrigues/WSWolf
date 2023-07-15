import math
from database import database
from datetime import datetime, timedelta
import pandas as pd
from applogger import AppLogger
from decimal import Decimal, getcontext

from config import * 

logger = AppLogger('fundamentalista.log')

def indicadores_fundamentalistas(row):
    score = 0
    PL = row['pl']
    volume_diario = row['vlm_diario']
    DY = row['dy']
    valor_intrinseco = row['vlr_intrinseco']
    valor_atual = row['vlr_acao']
    ROE = row['roe']
    PVP = row['pvp']
    bazin12 = row['bazin12']
    bazin36 = row['bazin36']
    bazin60 = row['bazin60']
    pebit = row['pebit']
    valor_teto_margem = row['vlr_teto_margem']
    valor_gordon = row['vlr_gordon']

    #empresa inoperavel 
    if volume_diario < 3000000.00: return 0

    #score indicadores
    if PL < 0: score -= 1
    if PL < 10 : score += 1
    if pebit < 10 and pebit > 0: score += 1
    if ROE > 0 : score += 1
    if DY > 6: score += 1
    if PVP > 2: score -= 1
    if PVP > 0 and PVP < 1: score += 1

    #score valores
    if valor_intrinseco > valor_atual : score += 1
    if bazin12 > valor_atual: score +=1
    if bazin36 > valor_atual: score +=1
    if bazin60 > valor_atual: score +=1
    if valor_atual < valor_teto_margem : score +=1
  #  if valor_gordon > valor_atual : score +=1

    return score


def calcular_valor_intrinseco(vpa, lpa):
    #Calcula o valor intrínseco de uma ação usando a fórmula de Graham.
    try:
        return math.sqrt(22.5 * vpa * lpa)
    except Exception as e:
        print(e)
        return 0

def media_por_periodo(df, num_periodos):
    # # Converter a coluna de data para o tipo datetime, se necessário
    if not pd.api.types.is_datetime64_any_dtype(df['dt_comunicado']):
         df['dt_comunicado'] = pd.to_datetime(df['dt_comunicado'])

    # Ordenar o DataFrame por data em ordem decrescente
    df = df.sort_values('dt_comunicado', ascending=False)

    # Obter a data atual
    data_atual = datetime.now().date()

    # Filtrar o DataFrame para manter apenas as linhas que correspondem aos últimos 5 períodos
    data_inicial = data_atual - pd.DateOffset(months=12 * num_periodos)

    # Filtrar o DataFrame para manter apenas as linhas dentro do período de filtragem
    df_filtrado = df[df['dt_comunicado'] >= data_inicial]

    # Calcular a soma dos valores
    soma_valores = df_filtrado['vlr'].sum()

    # Calcular a média dos valores por ano
    media_valores = soma_valores / num_periodos

    return media_valores


def calculo_Bazin(df, periodo):
    media = media_por_periodo(df, periodo)
    #soma_valor = df['valor'].sum()
    return  (media * 100) / 6

def calcular_gordon(df, taxa_retorno):
    if df.empty:
        return None  # Retorna None se o DataFrame estiver vazio

    # Configurar a precisão decimal
    getcontext().prec = 28

    # Calcular o valor presente dos dividendos
    valor_presente = Decimal(0)
    for index, row in df.iterrows():
        valor_presente += Decimal(row['vlr']) / ((Decimal(1) + Decimal(taxa_retorno)) ** (index + 1))

    # Calcular a taxa de crescimento dos dividendos
    if df['vlr'].iloc[0] != 0:
        taxa_crescimento = (Decimal(df['vlr'].iloc[-1]) / Decimal(df['vlr'].iloc[0])) - Decimal(1)
    else:
        taxa_crescimento = Decimal(0)  # ou qualquer outro valor adequado

    # Calcular o preço justo da ação
    preco_justo = float(valor_presente / (Decimal(taxa_retorno) - taxa_crescimento))

    return preco_justo


def valor_teto_margem(row):
    valor_intrinseco = row['vlr_intrinseco']
    bazin12 = row['bazin12']
    bazin36 = row['bazin36']
    bazin60 = row['bazin60']
    valor_gordon = row['vlr_gordon']
    #determina o menor valor encontrado para a acao
    menor_valor = min(valor_intrinseco, bazin12, bazin36, bazin60)
    #margem de 10% para a compra, em cima do menor valor
    return menor_valor * 0.9

def main():
    db = database()

    dfinfo_acoes = db.load_table_to_dataframe(tabela_coleta_acao)
    dfinfo_acoes['vlr_intrinseco'] = dfinfo_acoes.apply(lambda row: calcular_valor_intrinseco(row['vpa'] , row['lpa']), axis=1)

    dfdividendo = db.load_table_to_dataframe(tabela_dividendo)

    for index, row in dfinfo_acoes.iterrows():
        dftemp = dfdividendo.loc[dfdividendo['cod_acao'] == row['cod_acao']]
        dfinfo_acoes.at[index, 'bazin12'] = calculo_Bazin(dftemp, 1)
        dfinfo_acoes.at[index, 'bazin36'] = calculo_Bazin(dftemp, 3)
        dfinfo_acoes.at[index, 'bazin60'] = calculo_Bazin(dftemp, 5)
        taxa_retorno = 0.06
        dfinfo_acoes.at[index, 'vlr_gordon'] = calcular_gordon(dftemp, taxa_retorno)

    
    dfinfo_acoes['vlr_teto_margem'] = dfinfo_acoes.apply(lambda row: valor_teto_margem(row), axis=1)
    dfinfo_acoes['score'] = dfinfo_acoes.apply(lambda row: indicadores_fundamentalistas(row), axis=1)

    db.updateDB(tabela_coleta_acao, dfinfo_acoes, 'cod_acao')

main()