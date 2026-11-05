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
from utils.config import MAX

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
	capacity = validations.valid_integer("Quantidade de assentos: ", min=1, max=MAX)
	# valor da sala
	cost = validations.valid_decimal("Valor da sala: ")
	# funcionario responsavel
	employee = validations.valid_text("Funcionário responsável: ")
	if insert_room(theme, capacity, cost, employee) is None:
		print("Nao foi possivel")


def list_room():
	# Lista todas as salas registradas,
	cursor.execute("SELECT * FROM rooms")
	# fetchall busca todos os conjuntos de dados
	res = cursor.fetchall()

	# Pecorrer as linhas da tabela e imprimi formatado para melhor visualizacao.
	# sala[1] = sala x, coluna 1
	for sala in res:
		print(f"""
		Sala: {sala[1].upper()} \n
		Capacidade: {sala[2]} pessoas \n
		Custo: {sala[3]:.2f} € \n
		Funcionario responsavel:{sala[4]}
		-------------------------
		""")

def get_room():
	pass

def edit_room():
	pass

def assign_employee():
	pass

def get_employee_by_room(room_id):
	pass