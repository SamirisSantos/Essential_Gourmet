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
	# valor da sala
	cost = validations.valid_decimal("Valor da sala: ")
	# funcionario responsavel
	empoloyee = validations.valid_text("Funcionário responsável: ")
	
	#Adicionar dados na tabela
	cursor.execute(f"INSERT INTO rooms (theme, capacity, cost, employee) VALUES('{theme}', {capacity}, {cost}, '{empoloyee}')")


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