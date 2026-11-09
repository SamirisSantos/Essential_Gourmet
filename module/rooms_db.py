# Gestão de Salas - Base de Dados
# Este ficheiro contém as funções 
# responsáveis pelas operações SQL
# relacionadas com a gestão das salas, 
# incluindo inserir, consultar
# e atualizar os registos na base de dados.

#python -m module.rooms

# Importacao de modulos necessarios
import sqlite3
from db.database import ligar
from utils.logger import register_error

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
	# with para gerir a ligação e 
	# finally para garantir que ela é fechada
	finally:
		if connection:
			connection.close()

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
	finally:
		if connection:
			connection.close()

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
	finally:
		if connection:
			connection.close()

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
	finally:
		if connection:
			connection.close()
