#Reservas de Salas - Interação com o Utilizador
# Responsavel por interagir com usuário
# Deve ser possível, efetuar uma marcação de reserva, indicando:
# • Cliente associado
# • Sala pretendida
# • Data e hora da marcação
# • Quantidade de pessoas
# • Valor total

from . import reservation_db
from datetime import datetime
from utils.config import MENU_PRICE, RESERVATION_DURATION
from utils import validations

def create_reservation():
	# Consulta os clientes registados na base de dados
	clients = reservation_db.get_clients()
	# Verifica se existem clientes registados
	if not clients:
		print("Ainda não existem clientes registados.")
		return
	# Apresenta a lista de clientes
	print("\n--- CLIENTES REGISTADOS ---")
	for client in clients:
		print(f"ID: {client['id']} | Nome: {client['nome']}")
	# Solicita o ID do cliente que pretende fazer a reserva
	client_id = validations.valid_integer("ID do cliente: ", min=1 )

	# Verifica se o ID introduzido pertence a um cliente registado
	client_exists = False

	for client in clients:
		if client["id"] == client_id:
			client_exists = True
			break

	if not client_exists:
		print("Cliente não encontrado.")
		return

	# Solicita a data e a hora pretendidas para a reserva
	reservation_date = validations.valid_date("Data da reserva (DD/MM/AAAA): ")

	reservation_time = validations.valid_time("Hora da reserva (HH:MM): ")

	# Junta a data e a hora para verificar se a reserva
	# não está marcada para uma data ou hora no passado
	reservation_datetime = datetime.strptime(reservation_date + " " + reservation_time,"%Y-%m-%d %H:%M:%S")
	if reservation_datetime < datetime.now():
		print("Não é possível realizar uma reserva no passado.")
		return
	# Solicita a quantidade de pessoas para a reserva
	num_people = validations.valid_integer( "Número de pessoas: ", min=1)

	# Consulta as salas disponíveis de acordo com a data,
	# hora e capacidade necessárias para a reserva
	available_rooms = reservation_db.get_available_rooms( reservation_date, reservation_time, num_people)
	# Verifica se existem salas disponíveis
	if not available_rooms:
		print("Não existem salas disponíveis para esta data e hora.")
		return
	# Apresenta as salas disponíveis
	print("\n--- SALAS DISPONÍVEIS ---")

	for room in available_rooms:
		print(
			f"ID: {room['id']} | "
			f"Temática: {room['tematica']} | "
			f"Capacidade: {room['capacidade']} pessoas | "
			f"Custo da sala: {room['custo']:.2f} €"
		)
	# Solicita o ID da sala pretendida
	room_id = validations.valid_integer( "Escolha o ID da sala: ", min=1 )

	# Verifica se a sala escolhida pertence à lista
	# de salas disponíveis para a reserva
	selected_room = None
	for room in available_rooms:
		if room["id"] == room_id:
			selected_room = room
			break
	if selected_room is None:
		print("Sala inválida ou indisponível.")
		return

	# Calcula o valor total da reserva:
	# Número de pessoas x preço do menu + custo da sala
	total_value = (num_people * MENU_PRICE) + selected_room["custo"]
	# Apresenta o resumo dos valores da reserva
	print("\n--- RESUMO DA RESERVA ---")
	print(f"Duração da reserva: {RESERVATION_DURATION} horas")
	print(f"Preço do menu por pessoa: {MENU_PRICE:.2f} €")
	print(f"Custo da sala: {selected_room['custo']:.2f} €")
	print(f"Valor total: {total_value:.2f} €")
	print(f"Valor por pessoa: {(total_value/num_people):.2f} €")

	# Solicita a confirmação antes de guardar a reserva
	confirmation = validations.valid_option( "Deseja confirmar a reserva? (S/N): ", ["S", "N"])
	if confirmation == "N":
		print("Reserva cancelada.")
		return

	# Guarda os dados da reserva na base de dados
	reservation_id = reservation_db.add_reservation(client_id, room_id,reservation_date,
		reservation_time,num_people, total_value)
	# Verifica se a reserva foi registada com sucesso
	if reservation_id:
		print(f"Reserva registada com sucesso! ID: {reservation_id}")
	else:
		print("Não foi possível registar a reserva.")



def list_reservations():
	# Consulta todas as reservas registadas na base de dados
	reservations = reservation_db.get_reservations()

	# Verifica se existem reservas registadas
	if not reservations:
		print("Ainda não existem reservas registadas.")
		return

	# Apresenta a lista de reservas
	print("\n--- LISTA DE RESERVAS ---")
	for reservation in reservations:
		print(
			f"\nID: {reservation['id']}\n"
			f"Cliente: {reservation['client_name']}\n"
			f"Sala: {reservation['room_theme']}\n"
			f"Data: {reservation['data_reserva']}\n"
			f"Hora: {reservation['hora_reserva']}\n"
			f"Número de pessoas: {reservation['num_pessoas']}\n"
			f"Valor total: {reservation['valor_total']:.2f} €\n"
			f"Estado: {reservation['estado']}"
		)


def cancel_reservation_menu():
	# Consulta as reservas existentes na base de dados
	reservations = reservation_db.get_reservations()
	# Verifica se existem reservas para cancelar
	if not reservations:
		print("Ainda não existem reservas registadas.")
		return

	# Apresenta as reservas existentes
	print("\n--- LISTA DE RESERVAS ---")
	for reservation in reservations:
		print(
			f"\nID: {reservation['id']} | "
			f"Cliente: {reservation['client_name']} | "
			f"Sala: {reservation['room_theme']} | "
			f"Data: {reservation['data_reserva']} | "
			f"Hora: {reservation['hora_reserva']} | "
			f"Estado: {reservation['estado']}"
		)

	# Solicita o ID da reserva que o utilizador pretende cancelar
	reservation_id = validations.valid_integer( "\nID da reserva a cancelar: ", min=1)
	# Consulta os dados da reserva selecionada
	reservation = reservation_db.get_reservation(reservation_id)
	# Verifica se a reserva existe
	if reservation is None:
		print("Reserva não encontrada.")
		return
	# Verifica se a reserva já foi cancelada anteriormente
	if reservation["estado"] != "Ativa":
		print("Esta reserva já se encontra cancelada.")
		return
	# Solicita a confirmação antes de cancelar a reserva
	confirmation = validations.valid_option(
		"Deseja confirmar o cancelamento? (S/N): ",
		["S", "N"]
	)
	if confirmation == "N":
		print("Cancelamento interrompido.")
		return
	# Atualiza o estado da reserva na base de dados
	if reservation_db.cancel_reservation(reservation_id):
		print("Reserva cancelada com sucesso.")
	else:
		print("Não foi possível cancelar a reserva.")
