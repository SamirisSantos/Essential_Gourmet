
# Bibliotecas importadas
import sqlite3
from pathlib import Path
from module import customers, rooms, reservation

# Caminho principal do projeto
BASE_DIR = Path(__file__).resolve().parent

# Caminhos dos ficheiros
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "essencia_gourmet.db"
SQL_CREATE = DATA_DIR / "criar_tabelas.sql"
SQL_TEST = DATA_DIR / "dados_teste.sql"


def initialize_database():
	"""
	Verifica se a base de dados existe.
	Caso não exista, cria as tabelas e insere os dados de teste.
	"""

	# Verifica se a base de dados já existe
	if DB_PATH.exists():
		print("Base de dados encontrada.")
		return

	print("Base de dados não encontrada.")
	print("A inicializar a base de dados...")

	# Verifica se os scripts SQL existem
	if not SQL_CREATE.exists() or not SQL_TEST.exists():
		print("Erro: não foi possível encontrar os ficheiros SQL.")
		return

	connection = None

	try:
		# Cria a pasta data caso ainda não exista
		DATA_DIR.mkdir(parents=True, exist_ok=True)

		# Cria a base de dados e estabelece a ligação
		connection = sqlite3.connect(DB_PATH)

		# Ativa a verificação das chaves estrangeiras
		connection.execute("PRAGMA foreign_keys = ON")

		# Executa o script de criação das tabelas
		with open(SQL_CREATE, "r", encoding="utf-8") as file:
			connection.executescript(file.read())

		print("Tabelas criadas com sucesso.")

		# Executa o script de inserção dos dados de teste
		with open(SQL_TEST, "r", encoding="utf-8") as file:
			connection.executescript(file.read())

		print("Dados de teste inseridos com sucesso.")

	except sqlite3.Error as error:
		print(f"Erro ao inicializar a base de dados: {error}")

	except OSError as error:
		print(f"Erro ao ler os ficheiros SQL: {error}")

	finally:
		if connection:
			connection.close()


def main():
	# Inicializa a base de dados antes de iniciar a aplicação
	initialize_database()

	# Menu principal
	while True:
		print("\n========== ESSÊNCIA GOURMET ==========")
		print("1 - Gestão de clientes")
		print("2 - Gestão de salas")
		print("3 - Gestão de reservas")
		print("0 - Sair")
		print("======================================")

		option = input("Escolha uma opção: ").strip()

		if option == "1":
			pass

		elif option == "2":
			print("Gestão de salas")

		elif option == "3":
			print("Gestão de reservas")

		elif option == "0":
			print("A encerrar a aplicação...")
			break

		else:
			print("Opção inválida. Tente novamente.")

# Garante que a função main() só é executada quando este ficheiro
# é iniciado diretamente, evitando a sua execução automática
# quando o ficheiro é importado por outro módulo.
if __name__ == "__main__":
	main()
