# Gestão de Clientes - Base de Dados
# Este ficheiro contém as funções responsáveis pelas operações SQL
# relacionadas com a gestão dos clientes, incluindo inserir, consultar,
# pesquisar e atualizar os registos na base de dados.


# Importação de módulos necessários

import sqlite3

from db.database import ligar
from utils.logger import register_error

def add_client(name, birth_date, sex, nif, phone, email):
	# Insere um novo cliente na base de dados
	try:
		with ligar() as connection:
			cursor = connection.execute("""
				INSERT INTO clientes (nome, data_nascimento, sexo, nif, telemovel, email)
				VALUES (?, ?, ?, ?, ?, ?) """, (name, birth_date, sex, nif, phone, email))
			# Devolve o ID do cliente inserido
			return cursor.lastrowid
	except sqlite3.Error as error:
		register_error("clients_db.add_client", error)
		return None
	finally:
		if connection:
			connection.close()

def update_client(client_id, name, birth_date, sex, nif, phone, email):
	# Atualiza os dados de um cliente através do seu ID
	try:
		connection = None

		with ligar() as connection:
			cursor = connection.execute(""" UPDATE clientes SET nome = ?, data_nascimento = ?,
					sexo = ?, nif = ?, telemovel = ?, email = ?
				WHERE id = ? """, (name, birth_date, sex, nif, phone, email, client_id))
			# Verifica se algum registo foi atualizado
			return cursor.rowcount > 0
	except sqlite3.Error as error:
		register_error("clients_db.update_client", error)
		return False
	finally:
		if connection:
			connection.close()

def get_client_by_nif(nif):
	# Consulta um cliente através do seu NIF
	try:
		with ligar() as connection:
			row = connection.execute( "SELECT * FROM clientes WHERE nif = ?", (nif,) ).fetchone()
			# Se encontrar o cliente, converte o registo num dicionário
			if row:
				return dict(row)
			return None
	except sqlite3.Error as error:
		register_error("clients_db.get_client_by_nif", error)
		return None
	finally:
		if connection:
			connection.close()


def get_clients_by_name(name):
	# Pesquisa clientes através do nome ou parte do nome
	try:
		with ligar() as connection:
			rows = connection.execute("""
				SELECT * FROM clientes WHERE nome LIKE ?
				ORDER BY nome """, ("%" + name + "%",)).fetchall()
			# Converte os resultados numa lista de dicionários
			clients = []
			for row in rows:
				clients.append(dict(row))
			return clients
	except sqlite3.Error as error:
		register_error("clients_db.get_clients_by_name", error)
		return []
	finally:
		if connection:
			connection.close()


def get_all_clients():
	# Consulta todos os clientes registados na base de dados
	try:
		with ligar() as connection:
			rows = connection.execute(""" SELECT *
				FROM clientes ORDER BY nome """).fetchall()
			# Converte os resultados numa lista de dicionários
			clients = []
			for row in rows:
				clients.append(dict(row))
			return clients
	except sqlite3.Error as error:
		register_error("clients_db.get_all_clients", error)
		return []
	finally:
		if connection:
			connection.close()

def nif_exists(nif, client_id=0):
	# Verifica se outro cliente já está registado com o mesmo NIF
	# Na adição, o ID é 0 porque ainda não existe um cliente associado
	# Na edição, ignora o ID do próprio cliente

	try:
		with ligar() as connection:
			row = connection.execute("""
				SELECT id
				FROM clientes
				WHERE nif = ? AND id != ?
			""", (nif, client_id)).fetchone()
			# Se encontrar um registo, significa que o NIF já existe
			return row is not None
	except sqlite3.Error as error:
		register_error("clients_db.nif_exists", error)
		return True
	finally:
		if connection:
			connection.close()