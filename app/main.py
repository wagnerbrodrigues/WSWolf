import os
from acoes.scraper_acoes import scraper_acoes
from acoes.processa_fundamentalista import fundamentalista
from opcoes.scraper_opcoes import scraper_opcoes
from opcoes.processa_opcoes import processa_opcoes
from db.backup import Backup

parametros_raw: str = os.getenv("param", "")
parametros: list = set(item.strip() for item in parametros_raw.split(",") if item.strip())

fator_bazin_str = os.getenv("fator_bazin", "6")
fator_bazin = int(fator_bazin_str) if fator_bazin_str.isdigit() else 6

meses_bazin_str = os.getenv("meses_bazin", "60")
meses_bazin = int(meses_bazin_str) if meses_bazin_str.isdigit() else 60


def scraper():
    scpp = scraper_acoes()
    scpp.main()
    del scpp

def fundamenta():
    proc_acoes = fundamentalista(fator_bazin=fator_bazin,meses_bazin=meses_bazin)
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
        scraper()
        fundamenta()
        execute_backup()

if __name__ == "__main__":
    main()
