# Reservas de Salas - Interação com o Utilizador
# Responsável por interagir com o utilizador
# Deve ser possível efetuar uma marcação de reserva, indicando:
# • Cliente associado
# • Sala pretendida
# • Data e hora da marcação
# • Quantidade de pessoas
# • Valor total

from datetime import datetime

from . import reservation_db
from .customers_db import obter_todos_clientes
from .customers import adicionar_cliente, listar_clientes
from utils.config import PRECO_MENU, DURACAO_RESERVA
from utils import validations

def menu_reservas():
	# Menu para realizar ações sobre reservas
	while True:
		#validations.limpar()
		print("\n===== GESTÃO DE RESERVAS =====")
		print("1 - Criar reserva")
		print("2 - Listar reservas")
		print("3 - Cancelar reserva")
		print("0 - Voltar ao menu principal")
		opcao = input("Escolha uma opção: ").strip()
		if opcao == "1":
			validations.limpar()
			criar_reserva()
		elif opcao == "2":
			#validacoes.limpar()
			consultar_reservas()
		elif opcao == "3":
			validations.limpar()
			cancelar_reserva()
		elif opcao == "0":
			break
		else:
			print("Opção inválida.")

def criar_reserva():
	# Consulta os clientes registados na base de dados
	clientes = obter_todos_clientes()
	# Verifica se existem clientes registados
	if not clientes:
		print("Ainda não existem clientes registados.")
		return
	# Apresenta a lista de clientes
	print("\n--- CLIENTES REGISTADOS ---")
	for cliente in clientes:
		print(f"ID: {cliente['id']} | Nome: {cliente['nome']}")
	# Solicita o ID do cliente que pretende fazer a reserva
	cliente_id = validations.validar_inteiro("ID do cliente: ", minimo=1)
	# Verifica se o ID introduzido pertence a um cliente registado
	cliente_existe = False
	for cliente in clientes:
		if cliente["id"] == cliente_id:
			cliente_existe = True
			break
	if not cliente_existe:
		print("\nCliente não encontrado.")
		return

	# Solicita a data e a hora pretendidas para a reserva
	data_reserva = validations.validar_data("Data da reserva (DD/MM/AAAA): ")
	hora_reserva = validations.validar_hora("Hora da reserva (HH:MM): ")

	# Junta a data e a hora para verificar se a reserva
	# não está marcada para uma data ou hora no passado
	data_hora_reserva = datetime.strptime(data_reserva + " " + hora_reserva, "%Y-%m-%d %H:%M:%S")
	if data_hora_reserva < datetime.now():
		print("\nNão é possível realizar uma reserva no passado.")
		return

	# Solicita a quantidade de pessoas para a reserva
	num_pessoas = validations.validar_inteiro("Número de pessoas: ", minimo=1)
	# Consulta as salas disponíveis de acordo com a data,
	# hora e capacidade necessárias para a reserva
	salas_disponiveis = reservation_db.obter_salas_disponiveis(data_reserva, hora_reserva, num_pessoas)
	# Verifica se existem salas disponíveis
	if not salas_disponiveis:
		print("\nNão existem salas disponíveis para esta data e hora.")
		return
	
	# Apresenta as salas disponíveis
	print("\n--- SALAS DISPONÍVEIS ---")
	for sala in salas_disponiveis:
		print(
			f"ID: {sala['id']} | "
			f"Temática: {sala['tematica']} | "
			f"Capacidade: {sala['capacidade']} pessoas | "
			f"Custo da sala: {sala['custo']:.2f} €"
		)

	# Solicita o ID da sala pretendida
	sala_id = validations.validar_inteiro("Escolha o ID da sala: ", minimo=1)

	# Verifica se a sala escolhida pertence à lista
	# de salas disponíveis para a reserva
	sala_escolhida = None
	for sala in salas_disponiveis:
		if sala["id"] == sala_id:
			sala_escolhida = sala
			break

	if sala_escolhida is None:
		print("Sala inválida ou indisponível.")
		return

	# Calcula o valor total da reserva:
	# Número de pessoas x preço do menu + custo da sala
	valor_total = (num_pessoas * PRECO_MENU) + sala_escolhida["custo"]

	# Apresenta o resumo dos valores da reserva
	print("\n--- RESUMO DA RESERVA ---")
	print(f"Duração da reserva: {DURACAO_RESERVA} horas")
	print(f"Preço do menu por pessoa: {PRECO_MENU:.2f} €")
	print(f"Custo da sala: {sala_escolhida['custo']:.2f} €")
	print(f"Valor total: {valor_total:.2f} €")
	print(f"Valor por pessoa: {(valor_total / num_pessoas):.2f} €")

	# Solicita a confirmação antes de guardar a reserva
	confirmacao = validations.validar_opcao("Deseja confirmar a reserva? (S/N): ", ["S", "N"])
	if confirmacao == "N":
		print("Reserva cancelada.")
		return

	# Guarda os dados da reserva na base de dados
	reserva_id = reservation_db.adicionar_reserva(
		cliente_id, sala_id, data_reserva, hora_reserva, num_pessoas, valor_total)

	# Verifica se a reserva foi registada com sucesso
	if reserva_id:
		print(f"Reserva registada com sucesso! ID: {reserva_id}")
	else:
		print("Não foi possível registar a reserva.")


def consultar_reservas():
	# Consulta todas as reservas registadas na base de dados
	reservas = reservation_db.obter_todas_reservas()

	# Verifica se existem reservas registadas
	if not reservas:
		print("Ainda não existem reservas registadas.")
		return

	# Apresenta a lista de reservas
	print("\n--- LISTA DE RESERVAS ---")
	for reserva in reservas:
		print(
			f"\nID: {reserva['id']}\n"
			f"Cliente: {reserva['nome_cliente']}\n"
			f"Sala: {reserva['tematica_sala']}\n"
			f"Data: {reserva['data_reserva']}\n"
			f"Hora: {reserva['hora_reserva']}\n"
			f"Número de pessoas: {reserva['num_pessoas']}\n"
			f"Valor total: {reserva['valor_total']:.2f} €\n"
			f"Valor por pessoa: {(reserva['valor_total'] / reserva['num_pessoas']):.2f} €\n"
			f"Estado: {reserva['estado']}"
		)


def cancelar_reserva():
	# Consulta as reservas existentes na base de dados
	reservas = reservation_db.obter_todas_reservas()

	# Verifica se existem reservas para cancelar
	if not reservas:
		print("Ainda não existem reservas registadas.")
		return

	# Apresenta as reservas existentes
	print("\n--- LISTA DE RESERVAS ---")
	for reserva in reservas:
		print(
			f"\nID: {reserva['id']} | "
			f"Cliente: {reserva['nome_cliente']} | "
			f"Sala: {reserva['tematica_sala']} | "
			f"Data: {reserva['data_reserva']} | "
			f"Hora: {reserva['hora_reserva']} | "
			f"Estado: {reserva['estado']}"
		)

	# Solicita o ID da reserva que o utilizador pretende cancelar
	reserva_id = validations.validar_inteiro("\nID da reserva a cancelar: ", minimo=1)

	# Consulta os dados da reserva selecionada
	reserva = reservation_db.obter_reserva(reserva_id)

	# Verifica se a reserva existe
	if reserva is None:
		print("Reserva não encontrada.")
		return

	# Verifica se a reserva já foi cancelada anteriormente
	if reserva["estado"] != "Ativa":
		print("Esta reserva já se encontra cancelada.")
		return

	# Solicita a confirmação antes de cancelar a reserva
	confirmacao = validations.validar_opcao(
		"Deseja confirmar o cancelamento? (S/N): ",
		["S", "N"]
	)
	if confirmacao == "N":
		print("Cancelamento não realizado.")
		return

	# Atualiza o estado da reserva na base de dados
	if reservation_db.desativar_reserva(reserva_id):
		print("Reserva cancelada com sucesso.")
	else:
		print("Não foi possível cancelar a reserva.")