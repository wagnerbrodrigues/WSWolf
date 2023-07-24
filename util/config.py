import os 

tabela_acao = 'acao'
tabela_coleta_acao = 'coleta_acao'
tabela_dividendo = 'dividendo'
tabela_posicao_carteira = 'posicao_carteira'
tabela_controle_coleta = 'controle_coleta'
view_carteira_sistema = 'carteira_wswolf'
view_carteira_pessoal = 'carteira_pessoal'
view_ultima_coleta = 'ultima_coleta'
currentDir = os.path.dirname(__file__) 
diretorioWsWolf = os.path.dirname(currentDir)

chromeDriver = diretorioWsWolf + "\\driver_selenium\\chromedriver.exe"
log_scrapper_acoes = diretorioWsWolf + '\\log\\scrapper_opcoes.log'
log_scrapper_opcoes = diretorioWsWolf + '\\log\\scrapper_opcoes.log'
log_fundamentalista = diretorioWsWolf + '\\log\\fundamentalista.log'
log_compara_carteira = diretorioWsWolf + '\\log\\compara_carteira.log'

