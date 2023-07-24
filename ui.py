from rich.console import Console
import scraper_to_database

# Função para exibir o menu
def exibir_menu():
    console = Console()

    while True:
        console.print("\n[bold green]Menu Principal[/bold green]\n")
        console.print("1. Função 1")
        console.print("2. Função 2")
        console.print("3. Sair\n")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            funcao1()
        elif opcao == "2":
            funcao2()
        elif opcao == "3":
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
