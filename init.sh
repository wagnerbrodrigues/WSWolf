#!/bin/bash
echo "               _            "
echo "              / \\      _-'  "
echo "            _/|  \\-''- _ /  "
echo "        __-' { |          \\  "
echo "            /             \\  "
echo "            /       \"o.  |o }"
echo "            |            \\ ; "
echo "                          ', "
echo "               \\_         __\\"
echo "                 ''-_    \\.//"
echo "                   / '-____' "
echo "                  /          "
echo "                _'           "
echo "              _-'            "
echo ""
echo "██╗    ██╗███████╗██╗    ██╗ ██████╗ ██╗     ███████╗"
echo "██║    ██║██╔════╝██║    ██║██╔═══██╗██║     ██╔════╝"
echo "██║ █╗ ██║███████╗██║ █╗ ██║██║   ██║██║     █████╗  "
echo "██║███╗██║╚════██║██║███╗██║██║   ██║██║     ██╔══╝  "
echo "╚███╔███╔╝███████║╚███╔███╔╝╚██████╔╝███████╗██║     "
echo " ╚══╝╚══╝ ╚══════╝ ╚══╝╚══╝  ╚═════╝ ╚══════╝╚═╝     "
echo "      "
echo "Exemplo de Uso: wswolf --param=\"fundamentalista,backup\" --bazin=6"

# Inicialização das variáveis
# Determina o diretório onde o script atual está localizado
current_dir="$(dirname "$0")"
wswolf_compose_file="$current_dir/docker-compose.yaml"

param=""
fator_bazin=""
meses_bazin=""
init_mysql="no"  # Se a execução é para iniciar o mysql
atua_db="no" 


# Leitura dos parâmetros
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --param=*) param="${1#*=}"; shift ;;
        --bazin=*) fator_bazin="${1#*=}"; shift ;;
        --meses_bazin=*) meses_bazin="${1#*=}"; shift ;;
        --init-mysql) init_mysql="yes"; shift ;;
        --atua-db) atua_db=1; shift ;;
        *) echo "Opção inválida: $1" >&2; exit 1 ;;
    esac
done



# Validações de dependências
if ! command -v gzip &> /dev/null; then
    echo "gzip não está instalado. Por favor, instale-o."
    exit 1
fi

if ! command -v docker &> /dev/null; then
    echo "docker não está instalado. Por favor, instale-o."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "docker-compose não está instalado. Por favor, instale-o."
    exit 1
fi

# Validação do Docker
if ! docker info &> /dev/null; then
    echo "O Docker não está em execução. Por favor, inicie o Docker e tente novamente."
    exit 1
fi

if [[ $atua_db == 1 ]]; then
    param="backup"
else 
    # # # Iniciar MySQL
    if bash "$current_dir/init-mysql.sh"; then
        echo "MySQL iniciado com sucesso."
    else
        echo "Erro ao iniciar o MySQL. Código de retorno: $?"
        exit 1
    fi
fi

# # # Se a opção de iniciar MySQL foi passada, finaliza apos inicialização. Essa opção serve somente para iniciar o database.
if [[ $init_mysql == "yes" ]]; then
    exit 0
fi

# Exportação
export fator_bazin
export meses_bazin
export param

# Apaga Logs de execução anteriores
rm -rf $current_dir/logs/*

# Remover o contêiner anterior
if docker-compose -f "$wswolf_compose_file" down; then
   echo "Contêiner anterior removido com sucesso."
else
   echo "Erro ao remover o contêiner anterior."
fi

# Iniciar o contêiner
if docker-compose -f "$wswolf_compose_file" up --build -d && docker image prune -f; then
    echo "Contêiner WsWolf iniciado com sucesso"
else
    echo "Erro ao iniciar o contêiner WsWolf."
    exit 1
fi
