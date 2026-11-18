# Reservas de Salas - Interação com o Utilizador
# Responsável por interagir com o utilizador
# Deve ser possível efetuar uma marcação de reserva, indicando:
# • Cliente associado
# • Sala pretendida
# • Data e hora da marcação
# • Quantidade de pessoas
# • Valor total

import sqlite3

from db.database import ligar
from utils.logger import registar_erro
from utils.config import DURACAO_RESERVA

def adicionar_reserva(id_cliente, id_sala, data_reserva, hora_reserva, num_pessoas, total):
	# Insere uma nova reserva na base de dados
	ligacao = None
	try:
		with ligar() as ligacao:
			cursor = ligacao.execute("""
				INSERT INTO reservas
				(id_cliente, id_sala, data_reserva, hora_reserva, num_pessoas, valor_total)
				VALUES (?, ?, ?, ?, ?, ?)
			""", (id_cliente, id_sala, data_reserva, hora_reserva, num_pessoas, total))
			# Devolve o ID da reserva inserida
			return cursor.lastrowid
	except sqlite3.Error as erro:
		registar_erro("reserva_db.adicionar_reserva", erro)
		return None
	finally:
		if ligacao:
			ligacao.close()


def obter_todas_reservas():
	# Consulta todas as reservas, com o nome do cliente e a temática da sala
	ligacao = None
	try:
		with ligar() as ligacao:
			cursor = ligacao.execute("""
				SELECT reservas.id, clientes.nome AS nome_cliente, salas.tematica AS tematica_sala,
					reservas.data_reserva, reservas.hora_reserva, reservas.num_pessoas,
					reservas.valor_total, reservas.estado
				FROM reservas
				INNER JOIN clientes ON reservas.id_cliente = clientes.id
				INNER JOIN salas ON reservas.id_sala = salas.id
				ORDER BY reservas.data_reserva, reservas.hora_reserva
			""")
			linhas = cursor.fetchall()
		# Converte os resultados numa lista de dicionários
		reservas = []
		for linha in linhas:
			reservas.append(dict(linha))
		return reservas
	except sqlite3.Error as erro:
		registar_erro("reserva_db.obter_todas_reservas", erro)
		return []
	finally:
		if ligacao:
			ligacao.close()


def obter_reserva(reserva_id):
	# Consulta apenas uma reserva através do seu ID
	ligacao = None
	try:
		with ligar() as ligacao:
			linha = ligacao.execute(
				"SELECT * FROM reservas WHERE id = ?", (reserva_id,)).fetchone()
			# Se encontrar a reserva, converte o registo num dicionário
			if linha:
				return dict(linha)
			return None
	except sqlite3.Error as erro:
		registar_erro("reserva_db.obter_reserva", erro)
		return None
	finally:
		if ligacao:
			ligacao.close()


def obter_salas_disponiveis(data_reserva, hora_reserva, num_pessoas):
	# Devolve as salas com capacidade suficiente e sem reservas ativas sobrepostas.
	# Uma reserva existente sobrepõe-se à nova se:
	#   - começa antes do fim da nova (data/hora pretendida + duração) E
	#   - termina depois do início da nova.
	# Assim, uma reserva tem de terminar antes de outra começar.
	ligacao = None
	try:
		with ligar() as ligacao:
			cursor = ligacao.execute("""
				SELECT * FROM salas
				WHERE capacidade >= ?
				AND NOT EXISTS (
					SELECT 1 FROM reservas
					WHERE reservas.id_sala = salas.id
					AND reservas.estado = 'Ativa'
					AND datetime(reservas.data_reserva || ' ' || reservas.hora_reserva)
						< datetime(? || ' ' || ?, '+' || ? || ' hours')
					AND datetime(reservas.data_reserva || ' ' || reservas.hora_reserva,
						'+' || ? || ' hours') > datetime(? || ' ' || ?)
				)
				ORDER BY id
			""", (num_pessoas, data_reserva, hora_reserva, DURACAO_RESERVA,
					DURACAO_RESERVA, data_reserva, hora_reserva))
			linhas = cursor.fetchall()
		# Converte os resultados numa lista de dicionários
		salas = []
		for linha in linhas:
			salas.append(dict(linha))
		return salas
	except sqlite3.Error as erro:
		registar_erro("reserva_db.obter_salas_disponiveis", erro)
		return []
	finally:
		if ligacao:
			ligacao.close()


def desativar_reserva(reserva_id):
	# Cancela a reserva mudando só o estado, sem a apagar.
	# Assim ficam os dados de controlo do restaurante, caso sejam precisos.
	ligacao = None
	try:
		with ligar() as ligacao:
			cursor = ligacao.execute("""
				UPDATE reservas SET estado = 'Cancelada'
				WHERE id = ? AND estado = 'Ativa'
			""", (reserva_id,))
			# Confirma se a reserva foi cancelada
			return cursor.rowcount > 0
	except sqlite3.Error as erro:
		registar_erro("reserva_db.desativar_reserva", erro)
		return False
	finally:
		if ligacao:
			ligacao.close()