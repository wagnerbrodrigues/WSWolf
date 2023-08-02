import os
import pandas as pd

class processa_opcoes:
    
    def extrai_resultados(self, acao, vlr_atual):
        dataframe = self.le_arquivo(acao)
        dataframe.columns = dataframe.columns.str.strip()

        dataframe = self.filtrar_dataframe_por_vencimento(dataframe)

        dataframe["Último"] = dataframe["Último"] / 100
        dataframe["Strike"] = dataframe["Strike"] / 100
        dataframe["vlr_total"] = dataframe["Strike"] + dataframe["Último"]
        dataframe["descontado"] = dataframe["vlr_total"].apply(lambda x: 1 if vlr_atual > x else 0)
        dataframe_filtrado = dataframe[dataframe["Último"] < 0.10]
        # limite_superior = vlr_atual * 1.8

        # Filtrar o DataFrame
        # dataframe_filtrado = dataframe_filtrado[dataframe_filtrado['Strike'] <= limite_superior]

        # Ordena o DataFrame em ordem decrescente com base no campo "Último"
        return dataframe_filtrado.sort_values(by="Dist. (%) do Strike", ascending=True)
    
    def filtrar_por_potencial_crescimento(self, df, param_por_mes):
        if not pd.api.types.is_datetime64_any_dtype(df['Vencimento']):
            df['Vencimento'] = pd.to_datetime(df['Vencimento'])
    
        df_resultado = pd.DataFrame()
        for vencimento in df['Vencimento']:
            df_filtrado = df.copy()
            df_filtrado['PotencialCrescimento'] = df_filtrado.apply(lambda row: row['vlr_atual'] + param_por_mes * (vencimento.month - row['Vencimento'].month), axis=1)

            # Filtrar o DataFrame onde o PotencialCrescimento é maior que o Strike
            df_filtrado = df_filtrado[df_filtrado['PotencialCrescimento'] > df_filtrado['Strike']]

            # Adicionar a data de vencimento para cada resultado filtrado
            df_filtrado['Vencimento'] = vencimento

            # Concatenar o resultado no DataFrame acumulado
            df_resultado = pd.concat([df_resultado, df_filtrado])

        # Resetar o índice do DataFrame acumulado para garantir uma sequência contínua
        df_resultado.reset_index(drop=True, inplace=True)

        return df_resultado
    
    def filtrar_dataframe_por_vencimento(self, df):
        # Fazer uma cópia do DataFrame para não modificar o original
        df_copy = df.copy()

        # Converter a coluna 'Vencimento' para o tipo datetime
        df_copy['Vencimento'] = pd.to_datetime(df_copy['Vencimento'])

        # Obter a data atual
        data_atual = datetime.now()

        # Definir a quantidade de dias para filtrar (neste caso, 60 dias)
        dias_para_filtrar = 60

        # Calcular a data limite para filtrar
        data_limite = data_atual + timedelta(days=dias_para_filtrar)

        # Filtrar o DataFrame
        df_filtrado = df_copy[df_copy['Vencimento'] > data_limite]

        return df_filtrado
    
    def main(self)
        df_potencial = self.filtrar_por_potencial_crescimento(df_resultados, 3)
        # Exibir o DataFrame final
        print('********************')
        print('****  Potencial ****')
        print('********************')
        print(df_potencial)

        # Exibir o DataFrame final
        print('*******************')
        print('****  Pozinhos ****')
        print('*******************')
        print(df_resultados)
