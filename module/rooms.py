# Gestão de Salas - Interação com o Utilizador
# Deve ser possível adicionar novas salas com as seguintes características:
# • Quantidade de assentos (capacidade máxima de pessoas)
# • Temática da sala (Glamour, Espelhos, Latino, Urbano, etc.)
# • Funcionários atribuídos à sala
# • Custo da sala

# Importação de módulos necessários
from . import sala_db
from utils import validacoes
from utils.config import CAPACIDADE_MAXIMA, CAPACIDADE_MINIMA
from utils import validacoes 

def menu_salas():
	# Menu para realizar ações sobre salas
	while True:
		#validacoes.limpar()
		print("\n===== GESTÃO DE SALAS =====")
		print("1 - Registar sala")
		print("2 - Listar salas")
		print("3 - Editar sala")
		print("0 - Voltar ao menu principal")
		opcao = input("Escolha uma opção: ").strip()
		if opcao == "1":
			validacoes.limpar()
			registar_sala()
		elif opcao == "2":
			validacoes.limpar()
			listar_salas()
		elif opcao == "3":
			validacoes.limpar()
			editar_sala()
		elif opcao == "0":
			break
		else:
			print("Opção inválida.")


def registar_sala():
	# Solicita ao utilizador os dados da sala e guarda na base de dados
	print("\n--- REGISTAR SALA ---")

	tematica = validacoes.validar_texto("Temática da sala: ")
	# Por regra, uma sala não pode existir sem assentos
	capacidade = validacoes.validar_inteiro(
		"Quantidade de assentos: ", minimo=CAPACIDADE_MINIMA, maximo=CAPACIDADE_MAXIMA)
	funcionarios = validacoes.validar_texto("Funcionários responsáveis: ")
	custo = validacoes.validar_decimal("Custo da sala: ")

	sala_id = sala_db.inserir_sala(tematica, capacidade, funcionarios, custo)

	if sala_id is not None:
		print(f"\nSala registada com sucesso! ID: {sala_id}")
	else:
		print("Não foi possível registar a sala.")


def listar_salas():
	# Lista todas as salas registadas
	salas = sala_db.obter_todas_salas()

	if not salas:
		print("Ainda não há salas registadas.")
		return

	print("\n--- LISTA DE SALAS ---")
	for sala in salas:
		print(f"\nID: {sala['id']}")
		print(f"Temática: {sala['tematica'].upper()}")
		print(f"Capacidade: {sala['capacidade']} pessoas")
		print(f"Funcionários: {sala['funcionarios']}")
		print(f"Custo: {sala['custo']:.2f} €")
		print("-------------------------")


def editar_sala():
	# Pergunta ao utilizador que campos quer alterar
	# Se não houver salas, não adianta pedir um ID
	if not sala_db.obter_todas_salas():
		print("Ainda não há salas registadas.")
		return

	listar_salas()

	# Repete a pergunta até existir uma sala com esse ID (0 para cancelar)
	while True:
		sala_id = validacoes.validar_inteiro("ID da sala a editar (0 para cancelar): ", minimo=0)
		if sala_id == 0:
			return
		sala = sala_db.obter_sala(sala_id)
		if sala is not None:
			# Sala encontrada, sai deste ciclo
			break
		print("Número de sala inválido, insira um número válido (0 para cancelar).")

	# Repete o menu até o utilizador escolher sair
	while True:
		print("\nO que quer alterar?")
		print(f"1 - Temática ({sala['tematica']})")
		print(f"2 - Assentos ({sala['capacidade']})")
		print(f"3 - Funcionários ({sala['funcionarios']})")
		print(f"4 - Custo ({sala['custo']:.2f} €)")
		print("0 - Sair")
		opcao = validacoes.validar_inteiro("Opção: ", minimo=0, maximo=4)

		if opcao == 0:
			return
		elif opcao == 1:
			sala["tematica"] = validacoes.validar_texto("Nova temática: ")
		elif opcao == 2:
			sala["capacidade"] = validacoes.validar_inteiro(
				"Novos assentos: ", minimo=CAPACIDADE_MINIMA, maximo=CAPACIDADE_MAXIMA)
		elif opcao == 3:
			sala["funcionarios"] = validacoes.validar_texto("Novos funcionários (separados por vírgula): ")
		else:
			sala["custo"] = validacoes.validar_decimal("Novo custo da sala: ")

		# Grava logo a alteração
		if sala_db.atualizar_sala(sala["id"], sala["tematica"], sala["capacidade"],
								sala["funcionarios"], sala["custo"]):
			print("Sala atualizada com sucesso.")
		else:
			print("Não foi possível atualizar a sala.")

		# Volta a ler a sala da BD, para o menu mostrar o que está realmente guardado
		sala = sala_db.obter_sala(sala["id"]) or sala
		