from util.database import database
from util.applogger import AppLogger

logger = AppLogger('compara_careira.log')

#Arquivos de Configuração
from util.config import * 
from util.util import * 

db = database(logger)

def posicao_recente():
    dfCarteira = db.load_table_to_dataframe(view_ultima_coleta)
    return dfCarteira

def carteira_wswolf():
    dfCarteiraComprada = db.load_table_to_dataframe(view_carteira_sistema)
    return dfCarteiraComprada

def carteira_pessoal():
    dfCarteiraComprada = db.load_table_to_dataframe(view_carteira_pessoal)
    return dfCarteiraComprada

def comparar_carteira(row, dfUltimaPosicao):
    columns_to_compare = ['vlr_acao', 'vlm_diario', 'dy', 'pl', 'vpa', 'pvp', 'roe', 'lpa', 'pebit', 
                          'vlr_intrinseco', 'bazin12', 'bazin36', 'bazin60', 'vlr_teto_margem', 'score']
    cod_acao = row['cod_acao']
    linha = dfUltimaPosicao.query("cod_acao == @cod_acao")

    result = pd.Series()
    result['cod_acao'] = row['cod_acao']
    result['dt_compra'] = linha['dt_coleta'].iloc[0]
    result['dt_posicao'] = row['dt_coleta']

    for col in columns_to_compare:
        aux = linha[col].iloc[0]
        if row[col] > aux:
            result[col] = str(aux) + ' ↓'
        elif row[col] < aux:
            result[col] = str(aux) + ' ↑'
        else:
            result[col] = str(aux)

    return result

def Compara():
    dfUltimaPosicao = posicao_recente()
    dfCarteiraWSWolf = carteira_wswolf()
    dfCarteiraPessoal = carteira_pessoal()

    # Colunas para comparar
    
    
    dfCompare = dfCarteiraWSWolf.apply(comparar_carteira, axis=1, dfUltimaPosicao=dfUltimaPosicao)
    print("*** CARTEIRA WSWOLF ***")
    print(dfCompare)
    print("***********************")
    dfCompare = dfCarteiraPessoal.apply(comparar_carteira, axis=1, dfUltimaPosicao=dfUltimaPosicao)
    print("*** CARTEIRA PESSOAL ***")
    print(dfCompare)
    print("************************")

    # for index, row in dfCarteiraWSWolf.iterrows():
    #     cod_acao = row['cod_acao']
    #     linha = dfUltimaPosicao.query("cod_acao == @cod_acao")
    #     dfCompare.at[index, 'cod_acao'] = row['cod_acao']
    #     dfCompare.at[index, 'dt_compra'] = linha['dt_coleta'].iloc[0]
    #     dfCompare.at[index, 'dt_posicao'] = row['dt_coleta']

    #     for col in columns_to_compare:
    #         print(col)
            
    #         aux = linha[col].iloc[0]
    #         if row[col] > aux:
    #             dfCompare.at[index, col] =  str(aux) + ' ↓'
    #         elif row[col] < aux:
    #             dfCompare.at[index, col] =  str(aux) + ' ↑'
    #         else:
    #             dfCompare.at[index, col] =  str(aux) 
    
    # print(dfCompare)

    # Selecionar apenas as colunas de df1 no DataFrame resultante
    #df_result = df1

    # Visualizar o DataFrame resultante


    # # for col in columns_to_compare:
    # #     arrow = df2[col].apply(lambda x: ' ↑' if x > df1[col][0] else ' ↓' if x < df1[col][0] else '')
    # #     df2[col] = df2[col].astype(str) + arrow
    # columns_to_compare = ['vlr_acao', 'vlm_diario', 'dy', 'pl', 'vpa', 'pvp', 'roe', 'lpa', 'pebit', 'vlr_intrinseco', 'bazin12', 'bazin36', 'bazin60', 'vlr_teto_margem', 'score']
    # df_merged = df2.merge(df1, on='cod_acao', suffixes=('_df2', '_df1'))
    # for col in columns_to_compare:
    #     arrow = df_merged.apply(lambda row: ' ↑' if row[col + '_df2'] > row[col + '_df1'] else ' ↓' if row[col + '_df2'] < row[col + '_df1'] else '', axis=1)
    #     df_merged[col + '_df2'] = df_merged[col + '_df2'].astype(str) + arrow

    # # Visualizar o DataFrame resultante
    # print(df_merged)

    # print(f'A carteira de WsWolf teve uma lucro de {diferenca_porcentagem_wswolf}')
    # print(f"Se você investisse R$ 10.000,00 na carteira wswolf, hoje você teria R$ {lucro_wswolf:.2f}")

    # print(f'A carteira de WsWolf teve uma lucro de {diferenca_porcentagem_pessoal}')
    # print(f"Se você investisse R$ 10.000,00 na carteira pessoal, hoje você teria R$ {lucro_pessoal:.2f}")
    #     df1 = dfaux[dfaux['cod_acao'].isin(df2['cod_acao'])]
    # df1 = df1.reset_index(drop=True)

    # dfaux = posicao_recente()
    # df1 = dfaux[dfaux['cod_acao'].isin(df2['cod_acao'])]

    # df_compara_pessoal = dfaux[dfaux['cod_acao'].isin(df3['cod_acao'])]
    # df_compara_pessoal = df_compara_pessoal.reset_index(drop=True)


    # valor_wswolf = df2['vlr_acao'].sum()
    # valor_atual = df1['vlr_acao'].sum()
    
    # valor_pessoal = df3['vlr_acao'].sum()
    # valor_atual_compara_pessoal = df_compara_pessoal['vlr_acao'].sum()

    # diferenca_porcentagem_wswolf = ((valor_atual / valor_wswolf) - 1) * 100
    # # Calcular o lucro com base na variação percentual e aplicação de R$ 10.000,00
    # lucro_wswolf = 10000 * (1 + diferenca_porcentagem_wswolf / 100)

    # diferenca_porcentagem_pessoal = ((valor_atual_compara_pessoal / valor_pessoal) - 1) * 100
    # # Calcular o lucro com base na variação percentual e aplicação de R$ 10.000,00
    # lucro_pessoal = 10000 * (1 + diferenca_porcentagem_pessoal / 100)

    



Compara()