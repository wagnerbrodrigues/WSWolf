from util.database import database
from util.applogger import AppLogger

#Arquivos de Configuração
from util.config import * 
from util.util import * 

class compara_carteira: 

    def __init__(self):
        logger = AppLogger(log_compara_carteira)
        self.db = database(logger)

    def posicao_recente(self):
        dfCarteira = self.db.load_table_to_dataframe(view_ultima_coleta)
        return dfCarteira

    def carteira_wswolf(self):
        dfCarteiraComprada = self.db.load_table_to_dataframe(view_carteira_sistema)
        return dfCarteiraComprada

    def carteira_pessoal(self):
        dfCarteiraComprada = self.db.load_table_to_dataframe(view_carteira_pessoal)
        return dfCarteiraComprada

    def comparar_carteira(self, row, dfUltimaPosicao):
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
    
    def compara_percentual(self, dfUltimaPosicao, dfCarteira):
        dftemp = dfUltimaPosicao[dfUltimaPosicao['cod_acao'].isin(dfCarteira['cod_acao'])]
        valorAtual = dftemp['vlr_acao'].sum()
        valorCompra = dfCarteira['vlr_acao'].sum()
        diferenca_porcentagem = ((valorAtual / valorCompra) - 1) * 100
        # Calcular o lucro com base na variação percentual e aplicação de R$ 10.000,00
        lucro_pessoal = 10000 * (1 + diferenca_porcentagem / 100)

        return diferenca_porcentagem, lucro_pessoal
    
    def Compara(self):
        dfUltimaPosicao = self.posicao_recente()
        dfCarteiraWSWolf = self.carteira_wswolf()
        dfCarteiraPessoal = self.carteira_pessoal()

        dfCompare = dfCarteiraWSWolf.apply(self.comparar_carteira, axis=1, dfUltimaPosicao=dfUltimaPosicao)
        print("*** CARTEIRA WSWOLF ***")
        print(dfCompare)
        print("***********************")
        dfCompare = dfCarteiraPessoal.apply(self.comparar_carteira, axis=1, dfUltimaPosicao=dfUltimaPosicao)
        print("*** CARTEIRA PESSOAL ***")
        print(dfCompare)
        print("************************")

    def main(self):
        self.Compara()
        dfUltimaPosicao = self.posicao_recente()
        dfCarteiraWSWolf = self.carteira_wswolf()
        dfCarteiraPessoal = self.carteira_pessoal()


        diferenca_porcentagem, lucro = self.compara_percentual(dfUltimaPosicao,dfCarteiraWSWolf)
        print(f"A carteira de WsWolf teve uma lucro de {round(diferenca_porcentagem, 2)}%")
        print(f"Se você investisse R$ 10.000,00 na carteira WsWolf, hoje você teria R$ {lucro:.2f}")

        diferenca_porcentagem, lucro = self.compara_percentual(dfUltimaPosicao,dfCarteiraPessoal)
        print(f"A carteira de Pessoal teve uma lucro de {round(diferenca_porcentagem, 2)}%")
        print(f"Se você investisse R$ 10.000,00 na carteira pessoal, hoje você teria R$ {lucro:.2f}")

        
if __name__ == "__main__":
    comp = compara_carteira()
    comp.main()