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
view_lista_para_coleta = 'lista_para_coleta'

currentDir = os.path.dirname(__file__)
diretorioWsWolf = os.path.dirname(currentDir)
diretorio_downloads = os.path.join(currentDir, "downloads")

log_scraper_acoes = os.path.join(diretorioWsWolf, 'logs', 'scraper_acoes.log')
log_scraper_opcoes = os.path.join(diretorioWsWolf, 'logs', 'scraper_opcoes.log')
log_fundamentalista = os.path.join(diretorioWsWolf, 'logs', 'fundamentalista.log')
log_compara_carteira = os.path.join(diretorioWsWolf, 'logs', 'compara_carteira.log')
log_processa_opcoes = os.path.join(diretorioWsWolf, 'logs', 'log_processa_opcoes.log')
log_main = os.path.join(diretorioWsWolf, 'logs', 'log_main.log')


