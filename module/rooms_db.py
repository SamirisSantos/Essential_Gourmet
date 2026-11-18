# Gestão de Salas - Base de Dados
# Este ficheiro contém as funções responsáveis pelas operações SQL
# relacionadas com a gestão das salas, incluindo inserir, consultar
# e atualizar os registos na base de dados.

# Importação de módulos necessários
import sqlite3

from db.database import ligar
from utils.logger import registar_erro


def inserir_sala(tematica, capacidade, funcionarios, custo):
	# Guarda a sala na BD. Devolve o ID novo, ou None se der erro
	# Usar VALUES (?, ?) evita erros de SQL por causa de apóstrofos no texto
	ligacao = None
	try:
		with ligar() as ligacao:
			cursor = ligacao.execute(
				"INSERT INTO salas (tematica, capacidade, funcionarios, custo) VALUES (?, ?, ?, ?)",
				(tematica, capacidade, funcionarios, custo))
			# Devolve o ID da sala inserida
			return cursor.lastrowid
	except sqlite3.Error as erro:
		registar_erro("sala_db.inserir_sala", erro)
		return None
	finally:
		if ligacao:
			ligacao.close()


def obter_sala(sala_id):
	# Devolve uma sala em formato de dicionário, ou None se não existir
	ligacao = None
	try:
		with ligar() as ligacao:
			linha = ligacao.execute(
				"SELECT * FROM salas WHERE id = ?", (sala_id,)).fetchone()
			# Se encontrar a sala, converte o registo num dicionário
			if linha:
				return dict(linha)
			return None
	except sqlite3.Error as erro:
		registar_erro("sala_db.obter_sala", erro)
		return None
	finally:
		if ligacao:
			ligacao.close()


def obter_todas_salas():
	# Devolve a lista de todas as salas
	ligacao = None
	try:
		with ligar() as ligacao:
			linhas = ligacao.execute("SELECT * FROM salas ORDER BY id").fetchall()
		# Converte cada linha num dicionário e devolve uma lista
		salas = []
		for linha in linhas:
			salas.append(dict(linha))
		return salas
	except sqlite3.Error as erro:
		registar_erro("sala_db.obter_todas_salas", erro)
		return []
	finally:
		if ligacao:
			ligacao.close()


def atualizar_sala(sala_id, tematica, capacidade, funcionarios, custo):
	# Atualiza todos os campos de uma sala
	# Devolve True se alguma linha foi alterada
	ligacao = None
	try:
		with ligar() as ligacao:
			cursor = ligacao.execute("""
				UPDATE salas
				SET tematica = ?, capacidade = ?, funcionarios = ?, custo = ?
				WHERE id = ?
			""", (tematica, capacidade, funcionarios, custo, sala_id))
			# Verifica se alguma linha foi alterada
			return cursor.rowcount > 0
	except sqlite3.Error as erro:
		registar_erro("sala_db.atualizar_sala", erro)
		return False
	finally:
		if ligacao:
			ligacao.close()