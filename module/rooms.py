#Gestão de Salas
# Deve ser possível adicionar novas salas 
# com as seguintes características:
# • Quantidade de assentos (capacidade máxima de pessoas)
# • Temática da sala (Glamour, Espelhos, Latino, Urbano, etc.)
# • Funcionários atribuídos à sala
# • Custo da sala

#python -m module.rooms

# Importacao de modulos necessarios
from db.database import ligar #TODO
from utils.logger import register_error #TODO
from utils import validations

def insert_room():
	#Solicitar os dados de uma nova sala, valida os dados e insere na tabela
	# e no fim atribui o funcionario
	theme = validations.valid_text("Nome da sala: ")
	# a quantiade de assentos na sala tem que ser no minino 1,
	# por regra nenhuma uma sala deve exisiti sem assentos
	capacity = validations.valid_integer("Quantidade de assentos: ", min=1)
	cost = validations.valid_decimal("Valor da sala: ")
	
	# TODO: Ligar à base de dados e inserir a sala.

	# lastrowid retorna o ID da ultima linha inserida
	# nesse caso vai retorna o ID da sala, 
	# para atriburir chave estrageira na tabela dos funcionarios responsavel pela sala
	room_id = cursor.lastrowid 
	#Quantidade de funcionarios responsavel pela sala e os nomes
	qnt = validations.valid_integer("Quantidade de funcionário: ", min=1)
	empoloyees = []

	i = 0

	while i < qnt:
		name = validations.valid_text(f"Nome do funcionario {i+1}: ")
		cursor.execute(f"INSERT INTO employees (name, room_id) VALUES ('{name}', {room_id})")
	# TODO: Ligar e add funcionarios na base de dados


def list_room():
	# Lista todas as salas registradas,
	# incluindo a capacidade, custo e funcionário responsável
	pass

def get_room():
	pass

def edit_room():
	pass

def assign_employee():
	pass

def get_employee_by_room(room_id):
	pass