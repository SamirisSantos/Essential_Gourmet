# Gestão de Salas - Interação com o Utilizador
# Deve ser possível adicionar novas salas 
# Responsavel por interagir com usuário
# com as seguintes características:
# • Quantidade de assentos (capacidade máxima de pessoas)
# • Temática da sala (Glamour, Espelhos, Latino, Urbano, etc.)
# • Funcionários atribuídos à sala
# • Custo da sala

#python -m module.rooms

# Importacao de modulos necessarios

from . import rooms_db
from utils import validations
from utils.config import MAX_CAPACITY, MIN_CAPACITY

def room_menu():
	# Menu para realizar ações sobre salas
	while True:
		print("\n===== GESTÃO DE SALAS =====")
		print("1 - Registar sala")
		print("2 - Listar salas")
		print("3 - Editar sala")
		print("0 - Voltar ao menu principal")
		opcao = input("Escolha uma opção: ").strip()
		if opcao == "1":
			add_room()
		elif opcao == "2":
			list_room()
		elif opcao == "3":
			edit_room()
		elif opcao == "0":
			break
		else:
			print("Opção inválida.")

def add_room():
	#Solicida ao usuario os dados da sala e guarda
	theme = validations.valid_text("Nome da sala: ")
	# a quantiade de assentos na sala tem que ser no minino 1,
	# por regra nenhuma uma sala deve exisiti sem assentos
	capacity = validations.valid_integer("Quantidade de assentos: ", min=MIN_CAPACITY, max=MAX_CAPACITY)
	# valor da sala
	cost = validations.valid_decimal("Valor da sala: ")
	# funcionario responsavel
	employee = validations.valid_text("Funcionário responsável: ")
	if rooms_db.insert_room(theme, capacity, cost, employee) is None:
		print("Nao foi possivel")

def list_room():
	# Lista todas as salas registradas,
	# De maneira mais visual para o usuário
	res = rooms_db.get_all_rooms
	for sala in res:
		print(f"""
		Numero da Sala: {sala['id']} \n
		Sala: {sala['tematica'].upper()} \n
		Capacidade: {sala['capacidade']} pessoas \n
		Funcionario responsavel:{sala['funcionario']} \n
		Custo: {sala['custo']:.2f} €
		-------------------------
		""")

def edit_room():
	# Conversa com usuário para verificar quais campos deseja alterar
	# Se não houver salas, não adianta pedir um id
	if not rooms_db.get_all_rooms():
		print("Ainda não há salas registadas.")
		return

	list_room()
	# Repete a pergunta até existir uma sala com esse id (0 para cancelar)
	while True:
		room_id = validations.valid_integer("Id da sala a editar (0 para cancelar): ", min=MIN_CAPACITY, max=MAX_CAPACITY)
		if room_id == 0:
			return
		room = rooms_db.get_room(room_id)
		if room is not None:
			# sala encontrada, sai deste ciclo
			break
		print("Número de sala inválido, insira um número válido (0 para cancelar).")

	# Repete o menu até o utilizador escolher sair
	while True:
		print(f"""
			O que quer alterar?
			1 - Temática ({room['tematica']})
			2 - Assentos ({room['capacidade']})
			3 - Funcionários ({room['funcionarios']})
			4 - Custo ({room['custo']:.2f} €)
			0 - Sair""")
		option = validations.valid_integer("Opção: ", min=0, max=4)

		if option == 0:
			return
		elif option == 1:
			room["tematica"] = validations.valid_text("Nova temática: ")
		elif option == 2:
			room["capacidade"] = validations.valid_integer("Novos assentos: ", min=MIN_CAPACITY, max=MAX_CAPACITY)
		elif option == 3:
			room["funcionarios"] = validations.valid_text("Novos funcionários (separados por vírgula): ")
		else:
			room["custo"] = validations.valid_decimal("Novo valor da sala: ")

		# Grava logo a alteração
		if rooms_db.update_room(room["id"], room["tematica"], room["capacidade"],
						room["funcionarios"], room["custo"]):
			print("Sala atualizada com sucesso.")
		else:
			print("Não foi possível atualizar a sala.")

		# Volta a ler a sala da BD, para o menu mostrar o que está realmente guardado
		room = rooms_db.get_room(room["id"]) or room
