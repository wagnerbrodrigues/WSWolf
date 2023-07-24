from util.database import database
import pandas as pd
from util.config import * 
from util.util import * 


def monta_carteira():
    print(obtem_ativos())

def obtem_ativos():
    db = database()

    dfacao = db.load_table_to_dataframe(tabela_coleta_acao)
    # Ordenar o DataFrame pelos campos 'score' e 'volume'
    data_sorted = dfacao.sort_values(by=['score', 'vlm_diario'], ascending=False)

    # Limitar aos 5 primeiros registros
    return data_sorted.head(10)

def monta_df_carteira():
    db = database()
    dfCarteira = pd.DataFrame(columns=['cod_carteira', 'cod_acao', 'dt_aquisicao', 'ind_comprado', 'vlr_aquisicao'])
    dfinfo_acoes = obtem_ativos ()
    
    for index, row in dfinfo_acoes.iterrows():
        cod_carteira = 1
        cod_acao = row['cod_acao']
        dt_aquisicao = row['dt_coleta']
        ind_comprado = 1
        vlr_aquisicao = row['vlr_acao']

        # Criar um novo registro no DataFrame dfCarteira
        novo_registro = pd.DataFrame([[cod_carteira, cod_acao, dt_aquisicao, ind_comprado, vlr_aquisicao]], columns=dfCarteira.columns)
        dfCarteira = pd.concat([dfCarteira, novo_registro], ignore_index=True)

    dfCarteira['dt_aquisicao'] = corrigir_formato_data(dfCarteira, 'dt_aquisicao')
    db.insertDB(tabela_posicao_carteira, dfCarteira)



monta_df_carteira()