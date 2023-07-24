from rich.console import Console

from scrapper_opcoes import scrapper_opcoes
from processa_fundamentalista import fundamentalista
from scrapper_acoes import scrapper_acoes
from scrapper_opcoes import scrapper_opcoes
#from monta_carteira  import monta_carteira
from compara_carteira import compara_carteira

scpp = scrapper_opcoes()
scpa = scrapper_acoes()
fund = fundamentalista()
#mont = monta_carteira()
comp = compara_carteira()

# Função para exibir o menu
def exibir_menu():
    console = Console()

    while True:
        console.print("\n[bold green]Menu Principal[/bold green]\n")
        console.print("1. Scrapper Ações")
        console.print("2. Scrapper Opções")
        console.print("3. Processa Fundamentalista")
        console.print("4. Monta Carteira")
        console.print("5. Compara Carteira")
        console.print("0. Sair\n")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            scpp.main()
        elif opcao == "2":
            scpp.main()
        elif opcao == "5":
            comp.main()
        elif opcao == "0":
            break
        else:
            console.print("[bold red]Opção inválida. Por favor, tente novamente.[/bold red]")

# Função correspondente à opção 1 do menu
def funcao1():
    # Código da função 1
    print("Função 1 foi chamada")

def funcao2():
    # Código da função 1
    print("Função 1 foi chamada")

exibir_menu()
# Função correspondente à opção
