# Gestão de Clientes - Interação com o Utilizador
# Deve ser possível, adicionar um cliente com:
# • Nome completo
# • Data de nascimento
# • Sexo
# • NIF
# • Nº de telemóvel
# • Email

# Importação de módulos necessários
from . import clients_db
from utils import validations

def customers_menu():
	while True:
		print("\n===== GESTÃO DE CLIENTES =====")
		print("1 - Registar cliente")
		print("2 - Listar clientes")
		print("3 - Pesquisar cliente")
		print("4 - Editar cliente")
		print("0 - Voltar ao menu principal")
		opcao = input("Escolha uma opção: ").strip()
		if opcao == "1":
			add_client()
		elif opcao == "2":
			list_clients
		elif opcao == "3":
			search_client()
		elif opcao == "4":
			edit_client()
		elif opcao == "0":
			break
		else:
			print("Opção inválida.")

def ask_nif(client_id=None):
	#Solicita e valida o NIF do cliente
	while True:
		nif = validations.valid_nif("NIF: ")

		#Verifica se o NIF já existe na base de dados
		if clients_db.nif_exists(nif, client_id):
			print("Este NIF já está registado.")
		else:
			return nif

def show_client(client):
	#Mostra os dados de um cliente
	print("\n--- DADOS DO CLIENTE ---")
	print(f"ID: {client['id']}")
	print(f"Nome: {client['nome']}")
	print(f"Data de nascimento: {client['data_nascimento']}")
	print(f"Sexo: {client['sexo']}")
	print(f"NIF: {client['nif']}")
	print(f"Telemóvel: {client['telemovel']}")
	print(f"Email: {client['email']}")


def add_client():
	#Solicita os dados para registar um novo cliente
	print("\n--- REGISTRA CLIENTE ---")

	name = validations.valid_name("Nome completo: ")
	birth_date = validations.valid_birth_date("Data de nascimento (DD/MM/YYYY): ")
	sex = validations.valid_option("Sexo (M/F/O): ", ["M", "F", "O"])
	nif = ask_nif()
	phone = validations.valid_phone("Telemóvel: ")
	email = validations.valid_email("Email: ")

	#Envia os dados para a base de dados
	client_id = clients_db.add_client(
		name, birth_date, sex, nif, phone, email
	)

	if client_id is not None:
		print(f"\nCliente registado com sucesso! ID: {client_id}")
	else:
		print("Não foi possível registar o cliente.")


def list_clients():
	#Consulta e mostra todos os clientes registados
	print("\n--- LISTA DE CLIENTES ---")

	clients = clients_db.get_all_clients()

	if not clients:
		print("Não existem clientes registados.")
		return

	for client in clients:
		show_client(client)


def edit_client():
	#Procura o cliente e solicita os novos dados
	print("\n--- EDITAR CLIENTE ---")

	nif = validations.valid_nif("Insira o NIF do cliente: ")
	client = clients_db.get_client_by_nif(nif)

	if client is None:
		print("Cliente não encontrado.")
		return

	show_client(client)

	print("\nInsira os novos dados do cliente:")

	name = validations.valid_name("Nome completo: ")
	birth_date = validations.valid_birth_date("Data de nascimento (DD/MM/YYYY): ")
	sex = validations.valid_option("Sexo (M/F/O): ", ["M", "F", "O"])
	nif = ask_nif(client["id"])
	phone = validations.valid_phone("Telemóvel: ")
	email = validations.valid_email("Email: ")

	#Atualiza os dados na base de dados
	updated = clients_db.update_client(
		client["id"], name, birth_date, sex, nif, phone, email
	)

	if updated:
		print("Dados do cliente atualizados com sucesso!")
	else:
		print("Não foi possível atualizar os dados do cliente.")


def search_client():
	#Permite pesquisar um cliente pelo NIF ou nome
	print("\n--- PESQUISAR CLIENTE ---")
	print("1 - Pesquisar por NIF")
	print("2 - Pesquisar por nome")

	option = validations.valid_option("Escolha uma opção: ", ["1", "2"])

	if option == "1":
		nif = validations.valid_nif("Insira o NIF: ")
		client = clients_db.get_client_by_nif(nif)

		if client:
			show_client(client)
		else:
			print("Cliente não encontrado.")
