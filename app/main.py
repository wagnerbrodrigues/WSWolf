import sys

from acoes.scraper_acoes import scraper_acoes
from acoes.processa_fundamentalista import fundamentalista

from opcoes.scraper_opcoes import scraper_opcoes
from opcoes.processa_opcoes import processa_opcoes

from db.backup import Backup

from util.applogger import AppLogger
from util.config import * 

if __name__ == "__main__":
    #init
    scpp = scraper_acoes()
    scpp.main()
    del scpp

    proc_acoes = fundamentalista()
    proc_acoes.main()
    del proc_acoes

    # scpo = scraper_opcoes()
    # scpo.main()
    # del scpo

    # proc_opcoes = processa_opcoes()
    # proc_opcoes.main()
    # del proc_opcoes

    bkp = Backup()
    bkp.execute_mysql_dump()
    del bkp

    sys.exit()  # Encerrar o programa


