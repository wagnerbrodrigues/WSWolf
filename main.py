def main():
    if indicadores_fundamentalistas(PL, volume_diario, DY):
    
    if  indicatcalculo_bazin(dividendos, valor_atual):
        #df =  df._append({'acao': acao, 'media_5_anos': valor_medio, 'bazin': bazin,'pl': pl,'dy': dy})
        line = pd.DataFrame([{'acao': acao, 'media_5_anos': valor_medio, 'bazin': bazin,'pl': PL ,'dy': DY}])
        df = pd.concat([df, line], ignore_index=True)
