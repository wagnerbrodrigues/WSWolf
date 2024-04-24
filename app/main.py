import os
from acoes.scraper_acoes import scraper_acoes
from acoes.processa_fundamentalista import fundamentalista
from opcoes.scraper_opcoes import scraper_opcoes
from opcoes.processa_opcoes import processa_opcoes
from db.backup import Backup

parametros_raw: str = os.getenv("param", "")
parametros: list = set(item.strip() for item in parametros_raw.split(",") if item.strip())
fator_bazin: int = int(os.getenv("fator_bazin", 6))

def scraper():
    scpp = scraper_acoes()
    scpp.main()
    del scpp

def fundamenta():
    proc_acoes = fundamentalista(fator_bazin=fator_bazin)
    proc_acoes.main()
    del proc_acoes

# def execute_opcoes():
#     scpo = scraper_opcoes()
#     scpo.main()
#     del scpo

#     proc_opcoes = processa_opcoes()
#     proc_opcoes.main()
#     del proc_opcoes

def execute_backup():
    bkp = Backup()
    bkp.execute_mysql_dump()
    del bkp

def main():
    if len(parametros) > 0:
        if "scraper" in parametros:
            scraper()
        if "fundamentalista" in parametros:
            fundamenta()
        if "backup" in parametros:
            execute_backup()
    else:
        print("else")
        scraper()
        fundamenta()
        execute_backup()

if __name__ == "__main__":
    main()
