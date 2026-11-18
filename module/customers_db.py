# Gestão de Clientes - Base de Dados
# Este ficheiro contém as funções responsáveis pelas operações SQL
# relacionadas com a gestão dos clientes, incluindo inserir, consultar,
# pesquisar e atualizar os registos na base de dados.


# Importação de módulos necessários

from codecs import register_error
import sqlite3

from db.database import ligar
from utils.logger import registar_erro

def aguardar_cliente(nome, data_nascimento, sexo, nif, telemovel, email):
	# Insere um novo cliente na base de dados
	ligacao = None
	try:
		with ligar() as ligacao:
			cursor = ligacao.execute("""
				INSERT INTO clientes (nome, data_nascimento, sexo, nif, telemovel, email)
				VALUES (?, ?, ?, ?, ?, ?) """,
				(nome, data_nascimento, sexo, nif, telemovel, email))
			# Devolve o ID do cliente inserido
			return cursor.lastrowid
	except sqlite3.Error as erro:
		registar_erro("cliente_db.adicionar_cliente", erro)
		return None
	finally:
		if ligacao:
			ligacao.close()


def atualizar_cliente(cliente_id, nome, data_nascimento, sexo, nif, telemovel, email):
	# Atualiza os dados de um cliente através do seu ID
	ligacao = None
	try:
		with ligar() as ligacao:
			cursor = ligacao.execute(""" UPDATE clientes SET nome = ?, data_nascimento = ?,
					sexo = ?, nif = ?, telemovel = ?, email = ?
				WHERE id = ? """,
				(nome, data_nascimento, sexo, nif, telemovel, email, cliente_id))
			# Verifica se algum registo foi atualizado
			return cursor.rowcount > 0
	except sqlite3.Error as erro:
		registar_erro("cliente_db.atualizar_cliente", erro)
		return False
	finally:
		if ligacao:
			ligacao.close()


def procurar_por_nif(nif):
	# Consulta um cliente através do seu NIF
	ligacao = None
	try:
		with ligar() as ligacao:
			linha = ligacao.execute(
				"SELECT * FROM clientes WHERE nif = ?", (nif,)).fetchone()
			# Se encontrar o cliente, converte o registo num dicionário
			if linha:
				return dict(linha)
			return None
	except sqlite3.Error as erro:
		registar_erro("cliente_db.procurar_por_nif", erro)
		return None
	finally:
		if ligacao:
			ligacao.close()


def obter_clientes_por_nome(nome):
	# Pesquisa clientes através do nome ou parte do nome
	ligacao = None
	try:
		with ligar() as ligacao:
			linhas = ligacao.execute("""
				SELECT * FROM clientes WHERE nome LIKE ?
				ORDER BY nome """, ("%" + nome + "%",)).fetchall()
			# Converte os resultados numa lista de dicionários
			clientes = []
			for linha in linhas:
				clientes.append(dict(linha))
			return clientes
	except sqlite3.Error as erro:
		registar_erro("cliente_db.obter_clientes_por_nome", erro)
		return []
	finally:
		if ligacao:
			ligacao.close()


def obter_todos_clientes():
	# Consulta todos os clientes registados na base de dados
	ligacao = None
	try:
		with ligar() as ligacao:
			linhas = ligacao.execute(""" SELECT *
				FROM clientes ORDER BY nome """).fetchall()
			# Converte os resultados numa lista de dicionários
			clientes = []
			for linha in linhas:
				clientes.append(dict(linha))
			return clientes
	except sqlite3.Error as erro:
		registar_erro("cliente_db.obter_todos_clientes", erro)
		return []
	finally:
		if ligacao:
			ligacao.close()


def nif_existe(nif, cliente_id=0):
	# Verifica se outro cliente já está registado com o mesmo NIF
	# Na adição, o ID é 0 porque ainda não existe um cliente associado
	# Na edição, ignora o ID do próprio cliente
	ligacao = None
	try:
		with ligar() as ligacao:
			linha = ligacao.execute("""
				SELECT id
				FROM clientes
				WHERE nif = ? AND id != ?
			""", (nif, cliente_id)).fetchone()
			# Se encontrar um registo, significa que o NIF já existe
			return linha is not None
	except sqlite3.Error as erro:
		registar_erro("cliente_db.nif_existe", erro)
		return True
	finally:
		if ligacao:
			ligacao.close()