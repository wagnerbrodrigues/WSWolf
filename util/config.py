import os 

tabela_acao = 'acao'
tabela_coleta_acao = 'coleta_acao'
tabela_dividendo = 'dividendo'
tabela_posicao_carteira = 'posicao_carteira'
tabela_controle_coleta = 'controle_coleta'
view_carteira_sistema = 'carteira_wswolf'
view_carteira_aleatoria = 'carteira_aleatoria'
view_ultima_coleta = 'ultima_coleta'
view_ultima_carteira = 'ultima_carteira'
view_acao_url = 'acao_url'


currentDir = os.path.dirname(__file__) 
diretorioWsWolf = os.path.dirname(currentDir)
diretorio_downloads =  diretorioWsWolf + "\\downloads" # os.path.join(os.path.expanduser("~"), "Downloads")

# chromeDriver = diretorioWsWolf + "\\driver_selenium\\chromedriver.exe"
# geckoDriver = diretorioWsWolf + "\\driver_selenium\\geckodriver.exe"
log_scraper_acoes = diretorioWsWolf + '\\log\\scraper_opcoes.log'
log_scraper_opcoes = diretorioWsWolf + '\\log\\scraper_opcoes.log'
log_fundamentalista = diretorioWsWolf + '\\log\\fundamentalista.log'
log_compara_carteira = diretorioWsWolf + '\\log\\compara_carteira.log'


