# Gestão de Clientes - Interação com o Utilizador
# Deve ser possível, adicionar um cliente com:
# • Nome completo
# • Data de nascimento
# • Sexo
# • NIF
# • Nº de telemóvel
# • Email

# Importação de módulos necessários
from . import cliente_db
from utils import validacoes 

# Menu para realizar ações sobre clientes
def menu_clientes():
	while True:
		#validacoes.limpar()
		print("\n===== GESTÃO DE CLIENTES =====")
		print("1 - Registar cliente")
		print("2 - Consultar clientes")
		print("3 - Pesquisar cliente")
		print("4 - Editar cliente")
		print("0 - Voltar ao menu principal")
		opcao = input("Escolha uma opção: ").strip()
		if opcao == "1":
			validacoes.limpar()
			adicionar_cliente()
		elif opcao == "2":
			validacoes.limpar()
			listar_clientes()
		elif opcao == "3":
			validacoes.limpar()
			pesquisar_cliente()
		elif opcao == "4":
			validacoes.limpar()
			editar_cliente()
		elif opcao == "0":
			break
		else:
			print("Opção inválida.")


def pedir_nif_unico(cliente_id=0):
	# Solicita e valida o NIF do cliente
	while True:
		nif = validacoes.validar_nif("NIF: ")

		# Verifica se o NIF já existe na base de dados
		if cliente_db.nif_existe(nif, cliente_id):
			print("Este NIF já está registado.")
		else:
			return nif


def mostrar_cliente(cliente):
	# Mostra os dados de um cliente
	print("\n--- DADOS DO CLIENTE ---")
	print("-" * 40)
	print(f"ID:                 {cliente['id']}")
	print(f"Nome:               {cliente['nome']}")
	print(f"Data de nascimento: {cliente['data_nascimento']}")
	print(f"Sexo:               {cliente['sexo']}")
	print(f"NIF:                {cliente['nif']}")
	print(f"Telemóvel:          {cliente['telemovel']}")
	print(f"Email:              {cliente['email']}")


def adicionar_cliente():
	# Solicita os dados para registar um novo cliente
	print("\n--- ADICIONAR CLIENTE ---")

	nome = validacoes.validar_nome("Nome completo: ")
	data_nascimento = validacoes.validar_data_nascimento("Data de nascimento (DD/MM/YYYY): ")
	sexo = validacoes.validar_opcao("Sexo (M/F/O): ", ["M", "F", "O"])
	nif = pedir_nif_unico()
	telemovel = validacoes.validar_telemovel("Telemóvel: ")
	email = validacoes.validar_email("Email: ")

	# Envia os dados para a base de dados
	cliente_id = cliente_db.aguardar_cliente(
		nome, data_nascimento, sexo, nif, telemovel, email)

	if cliente_id is not None:
		print(f"\nCliente guardado com sucesso!")
	else:
		print("Não foi possível registar o cliente.")


def listar_clientes():
	# Consulta e mostra todos os clientes registados
	print("\n--- LISTA DE CLIENTES ---")

	clientes = cliente_db.obter_todos_clientes()

	if not clientes:
		print("Ainda não há clientes registados.")
		return

	for cliente in clientes:
		mostrar_cliente(cliente)
	print("-" * 40)
	print("Total:", len(clientes), "cliente(s)")

def editar_cliente():
	# Procura o cliente e solicita os novos dados
	print("\n--- EDITAR CLIENTE ---")

	nif = validacoes.validar_nif("Insira o NIF do cliente: ")
	cliente = cliente_db.procurar_por_nif(nif)

	if cliente is None:
		print("Cliente não encontrado.")
		return

	mostrar_cliente(cliente)

	print("\nInsira os novos dados do cliente:")

	nome = validacoes.validar_nome("Nome completo: ")
	data_nascimento = validacoes.validar_data_nascimento("Data de nascimento (DD/MM/YYYY): ")
	sexo = validacoes.validar_opcao("Sexo (M/F/O): ", ["M", "F", "O"])
	nif = pedir_nif_unico(cliente["id"])
	telemovel = validacoes.validar_telemovel("Telemóvel: ")
	email = validacoes.validar_email("Email: ")

	# Atualiza os dados na base de dados
	atualizado = cliente_db.atualizar_cliente(
		cliente["id"], nome, data_nascimento, sexo, nif, telemovel, email
	)

	if atualizado:
		print("Dados do cliente atualizados com sucesso!")
	else:
		print("Não foi possível atualizar os dados do cliente.")


def pesquisar_cliente():
	# Permite pesquisar um cliente pelo NIF ou nome
	print("\n--- PESQUISAR CLIENTE ---")
	print("1 - Pesquisar por NIF")
	print("2 - Pesquisar por nome")

	opcao = validacoes.validar_opcao("Escolha uma opção: ", ["1", "2"])

	if opcao == "1":
		nif = validacoes.validar_nif("Insira o NIF: ")
		cliente = cliente_db.obter_cliente_por_nif(nif)

		if cliente:
			mostrar_cliente(cliente)
		else:
			print("Cliente não encontrado.")
	else:
		nome = input("Insira o nome (ou parte dele): ").strip()
		clientes = cliente_db.obter_clientes_por_nome(nome)

		if not clientes:
			print("Nenhum cliente encontrado.")
			return

		for cliente in clientes:
			mostrar_cliente(cliente)
