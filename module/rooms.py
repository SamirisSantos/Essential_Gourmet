#Gestão de Salas
# Deve ser possível adicionar novas salas 
# com as seguintes características:
# • Quantidade de assentos (capacidade máxima de pessoas)
# • Temática da sala (Glamour, Espelhos, Latino, Urbano, etc.)
# • Funcionários atribuídos à sala
# • Custo da sala

#python -m module.rooms

# Importacao de modulos necessarios
import sqlite3
from db.database import ligar #TODO
from utils.logger import register_error #TODO
from utils import validations
from utils.config import MAX, MIN

def insert_room(theme, capacity, cost, employee):
	# Guarda a sala no BD. Devolve o ide novo, ou None se der erro
	# Usar VALUES(?, ?) evita erro de insercao do SQL por causa do uso do apostrofos no meio da str.
	try:
		with ligar() as connection:
			cursor = connection.execute("INSERT INTO sala (tematica,capacidade, funcionarios, custo) VALUES (?, ?, ?, ?)",
										(theme,capacity,employee,cost))
	except sqlite3.Error as error:
		register_error("rooms.insert_room", error)
		return None

def add_room():
	#Solicida ao usuario os dados da sala e guarda
	theme = validations.valid_text("Nome da sala: ")
	# a quantiade de assentos na sala tem que ser no minino 1,
	# por regra nenhuma uma sala deve exisiti sem assentos
	capacity = validations.valid_integer("Quantidade de assentos: ", min=MIN, max=MAX)
	# valor da sala
	cost = validations.valid_decimal("Valor da sala: ")
	# funcionario responsavel
	employee = validations.valid_text("Funcionário responsável: ")
	if insert_room(theme, capacity, cost, employee) is None:
		print("Nao foi possivel")

def get_room(room_id):
	#Essa função pega os dados de uma tabela e converte para um dicionário
	#Devolve um sala
	try:
		with ligar() as connection:
			#fetchone() busca e retorna a proxima linha do resultado de uma consulta em SQL
			row = connection.execute("SELECT * FROM salas WHERE id=?", (room_id,)).fetchone()
			#Encontra a sala, converte os dados para um dicionario, se nao conseguir retorna None
			if row:
				# dict() é uma função que permite criar 
				# ou converter dados para um dicionário
				return dict(row)
			else:
				return None
	except sqlite3.Error as error:
		register_error("rooms.get_room", error)
		return None

def get_all_rooms():
	#Devolve a lista de todas as sala
	try:
		with ligar() as connection:
			rows = connection.execute("SELECT * FROM salas ORDER BY id").fetchall()
		result = []
		# Percorre os registos, 
		# converte cada linha num dicionário e devolve uma lista.
		for row in rows:
			result.append(dict(row))
		return result
	except sqlite3.Error as error:
		register_error("rooms.get_all_rooms", error)
		return []

def list_room():
	# Lista todas as salas registradas,
	# De maneira mais visual para o usuário
	for sala in res:
		print(f"""
		Numero da Sala: {sala['id']} \n
		Sala: {sala['tematica'].upper()} \n
		Capacidade: {sala['capacidade']} pessoas \n
		Funcionario responsavel:{sala['funcionario']} \n
		Custo: {sala['custo']:.2f} €
		-------------------------
		""")

def update_room(room_id, theme, capacity, employee, cost):
	# Atualiza todos os campos de uma sala
	# Se tiver um linha alterada na tabela retorna True
	# Vai apenas mexer na base de dados, nao fala com usuário
	try:
		with ligar() as connection:
			cursor = connection.execute(
				"""
				UPDATE rooms
				SET theme = ?, capacity = ?, employee = ?, cost = ?
				WHERE room_id = ?
				""",
				(theme, capacity, employee, cost, room_id)
			)
			# Verifica se alguma linha foi alterada
			return cursor.rowcount > 0
	except sqlite3.Error as error:
		register_error("rooms.update_room", error)
		return False

def edit_room():
	# Conversa com usuário para verificar quais campos deseja alterar
	# Se não houver salas, não adianta pedir um id
	if not get_all_rooms():
		print("Ainda não há salas registadas.")
		return

	list_room()
	# Repete a pergunta até existir uma sala com esse id (0 para cancelar)
	while True:
		room_id = validations.valid_integer("Id da sala a editar (0 para cancelar): ", min=0, max=999999)
		if room_id == 0:
			return
		room = get_room(room_id)
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
			room["capacidade"] = validations.valid_integer("Novos assentos: ", min=1, max=100)
		elif option == 3:
			room["funcionarios"] = validations.valid_text("Novos funcionários (separados por vírgula): ")
		else:
			room["custo"] = validations.valid_decimal("Novo valor da sala: ")

		# Grava logo a alteração
		if update_room(room["id"], room["tematica"], room["capacidade"],
						room["funcionarios"], room["custo"]):
			print("Sala atualizada com sucesso.")
		else:
			print("Não foi possível atualizar a sala.")

		# Volta a ler a sala da BD, para o menu mostrar o que está realmente guardado
		room = get_room(room["id"]) or room
