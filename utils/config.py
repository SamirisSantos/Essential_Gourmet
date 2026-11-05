# Esse arquivo foi criado para guarda valores constante do projeto
# Como valor do menu, caminhos de arquivos e formato de data
# Caso tenha alguma mudanca de valores fica mais simples alterar no local só

# Bibliotecas importadas
# pathlib é utilizada para manipular caminho sw arquivos e diretorios

from pathlib import Path

# Definicao da raiz do projeto, a partir desse arquivo
BASE_DIR = Path(__file__).resolve().parent.parent
#BASE_DIR = Path.cwd().resolve()
# __file__	.../Essential_Gourmet/utils/config.py 
# .resolve(), o caminho completo
# .parent .../Essential_Gourmet/utils - a pasta que esta esse arquivo
# .parent.parent	.../Essential_Gourmet - pasta principal

# Pasta do banco de dados
DATA_DIR = BASE_DIR / "data"
# Verifica se tem uma pasta com o banco de dados
DATA_DIR.mkdir(exist_ok=True)

# Arquivo do database
DB_PATH = DATA_DIR / "data.db"
# Pasta dos log de erro
LOG_PATH = DATA_DIR / "errors.txt" 

MENU_PRICE = 220.0
# Padrao de data e hora utilizado em Portugal
DATE_FORMAT = "%d/%m/%Y"
DATETIME_FORMAT = "%d/%m/%Y %H:%M"

# --- Formatos de data e hora utilizado pelo datatime
# --- %Y = Ano (YYYY)
# --- %m = Mês (MM)
# --- %d = Dia (DD)
# --- %H = Hora (HH)
# --- %M = Minutos (MM)
# --- %S = Segundos (SS)

