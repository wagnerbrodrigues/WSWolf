from database import database
import pandas as pd


def monta_carteira():
    print(obtem_ativos())

def obtem_ativos():
    db = database()

    dfacao = db.load_table_to_dataframe('info_acoes')
    # Ordenar o DataFrame pelos campos 'score' e 'volume'
    data_sorted = dfacao.sort_values(by=['score', 'volume_diario'], ascending=False)

    # Limitar aos 5 primeiros registros
    return data_sorted.head(10)

monta_carteira()