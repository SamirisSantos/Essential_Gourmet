#Reservas de Salas  - Base de Dados
# Este ficheiro contém as funções responsáveis pelas operações SQL
# relacionadas com a gestão das reservas, incluindo consultar clientes,
# inserir, consultar, verificar disponibilidade e cancelar reservas.
# Não contém interação direta com o utilizador.

import sqlite3

from db.database import ligar
from utils.logger import register_error
from utils.config import RESERVATION_DURATION
from .customers_db import get_all_clients as get_clients

def add_reservation(id_cliente, id_room, res_date, res_time, num_people, total):
	# Insere uma nova reserva na base de dados
	# Não tem interação direta com o utilizador
	try:
		connection = None

		with ligar() as connection:
			cursor = connection.execute(""" INSERT INTO reservas
				(id_cliente, id_sala, data_reserva, hora_reserva, num_pessoas, valor_total)
				VALUES (?, ?, ?, ?, ?, ?)
			""", (id_cliente, id_room, res_date, res_time, num_people, total))
			# Devolve o ID da reserva inserida
			return cursor.lastrowid
	except sqlite3.Error as error:
		register_error("reservation_db.add_reservation", error)
		return None
	finally:
		if connection:
			connection.close()

def get_all_reservations():
	try:
		with ligar() as connection:
			res = connection.execute("""SELECT reservas.id, clientes.nome AS client_name, salas.tematica AS room_theme,
					reservas.data_reserva, reservas.hora_reserva, reservas.num_pessoas,
					reservas.valor_total, reservas.estado FROM reservas
				INNER JOIN clientes
					ON reservas.id_cliente = clientes.id
				INNER JOIN salas
					ON reservas.id_sala = salas.id
				ORDER BY reservas.data_reserva, reservas.hora_reserva
			""")
		rows = res.fetchall()
		# Converte o resultado em dicionario
		reserva = []
		for row in rows:
			reserva.append(dict(row))
		return reserva
	except sqlite3.Error as error:
		register_error("reservation.get_all_reservations", error)
		return None
	# with para gerir a ligaçãoo e 
	# finally para garantir que ela é fechada
	finally:
		if connection:
			connection.close()

def get_reservation(reservation_id):
	# Consulta apenas uma reserva
	try:
		with ligar() as connection:
			res = connection.execute("SELECT * From reservas WHERE id = ?", (reservation_id,))
			# fetchone busca a proxima linha do resultado da consulta
			row = res.fetchone()
			# Se tem a reserva devolve o valor se nao retorna None
			# Converte o registo num dicionário
			if row:
				return dict(row)
			else:
				return None
	except sqlite3.Error as error:
		register_error("reservation.get_reservation", error)
		return None
	# with para gerir a ligaçãoo e 
	# finally para garantir que ela é fechada
	finally:
		if connection:
			connection.close()

def get_available_rooms(res_data, res_time, num_people):
	try:
		with ligar() as connection:
			# Verifica se existe alguma sobreposição dos intervalo das reservas
			# Assim sabendo se existe algum conflito quando uma reserva começa e a outra termina
			# Pois uma reserva deve terminar antes que outra reserva comece
			res = connection.execute(""" SELECT * FROM salas WHERE capacidade >= ?
					AND NOT EXISTS (SELECT 1 FROM reservas WHERE reservas.id_sala = salas.id
							AND reservas.estatos = 'Ativa')
					-- Verifica se existe um conflito de horas com outras reserva ativas da mesma sala
					-- Verifica se a reserva existente começa antes do fim da nova
					-- (data/hora pretendida + a duração da nova reserva)
					AND datetime( reservas.data_reserva || ' ' || reservas.hora_reserva
							) < datetime( ? || ' ' || ?, '+' || ? || ' hours')

					-- Verifica se a reserva existente termina depois do início da nova
					-- Mesma logica de cima, mas para hora e data existente
					AND datetime( reservas.data_reserva || ' ' || reservas.hora_reserva,
						'+' || ? || ' hours') > datetime(? || ' ' || ?)
				)
				ORDER BY id
			"""), (num_people, res_data, res_time, RESERVATION_DURATION,
					RESERVATION_DURATION, res_data, res_time)
		# Converte os resultados em dicionários
		rows = res.fetchall()
		available_rooms = []
		for row in rows:
			available_rooms.append(dict(row))
	except sqlite3.Error as error:
		register_error("reservation.get_available_rooms", error)
		return []
	# with para gerir a ligaçãoo e 
	# finally para garantir que ela é fechada
	finally:
		if connection:
			connection.close()
	
def cancel_reservation(reservation_id):
	# Cancelamento de reserva
	try:
		with ligar() as connection:
			# Cancela a reserva e altera apenas o status da reserva sem excluir definitivamente
			# Essa é uma estrategia para manter dados de controle do restaurante caso necessário
			res = connection.execute("""UPDATE reservas SET estado = 'Cancelada' 
							WHERE  id = ? AND estado = 'Ativa'""", (reservation_id,))
			# confirma se a reserva foi cancelada corretamente
			cancelled = res.rowcount > 0
			return cancelled
	except sqlite3.Error as error:
		register_error("reservation.cancel_reservation", error)
		return False
	# with para gerir a ligaçãoo e 
	# finally para garantir que ela é fechada
	finally:
		if connection:
			connection.close()
