@echo off
setlocal

REM Defina o nome do arquivo de script Python
set "script_coleta=scraper_acoes.py"
set "script_processa=processa_fundamentalista.py"
set "script_backup=\mysql\backup.py"

REM Obter o diretório atual
for %%I in ("%~dp0") do set "diretorio_atual=%%~fI"

REM Concatenar o diretório com o nome do arquivo de script
set "caminho_completo_coleta=%diretorio_atual%\%script_coleta%"
set "caminho_completo_processa=%diretorio_atual%\%script_processa%"
set "caminho_completo_backup=%diretorio_atual%\%script_backup%"

REM Executar o script Python
python3 "%caminho_completo_coleta%"
python3 "%caminho_completo_processa%"
python3 "%caminho_completo_backup%"

REM Pausar para visualizar a saída do script antes de fechar a janela
pause

endlocal



