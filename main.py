from rich import print
from rich.console import Console

from scraper_acoes import scraper_acoes
from processa_fundamentalista import fundamentalista
from scraper_opcoes import scraper_opcoes
#from processa_opcoes import processa_opcoes

# Funções do menu
def funcao1():
    scpa = scraper_acoes()
    scpa.main()
    del scpa

def funcao2():
    fund = fundamentalista()
    fund.main()
    del fund

def funcao3():
    scpo = scraper_opcoes()
    scpo.main()
    del scpo

def funcao4():
    # prossop = processa_opcoes()
    # prossop.main()
    # del prossop
    print("Vai vir")

def sair():
    print("Saindo do menu...")
    quit()

# Função para exibir o menu
def exibir_menu():
    console = Console()
    console.print("==== Menu ====", style="bold green")
    console.print("1. Scraper Ações")
    console.print("2. Processa Fundamentalista")
    console.print("3. Scraper Opções --Em construção", style="bold red")
    console.print("4. Processa Opções --Em construção", style="bold red")
    console.print("0. Sair")

# Dicionário para mapear as opções do menu para as funções correspondentes
opcoes_menu = {
    "1": funcao1,
    "2": funcao2,
    "3": funcao3,
    "4": funcao4,
    "0": sair
}

# Loop do menu
while True:
    exibir_menu()
    opcao = input("Digite o número da opção desejada: ")

    # Verifica se a opção é válida e chama a função correspondente
    if opcao in opcoes_menu:
        opcoes_menu[opcao]()
    else:
        print("Opção inválida! Por favor, escolha uma opção válida.")