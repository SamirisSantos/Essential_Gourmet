# Esse arquivo contem as funções de validações de input inciais

import math, datetime

def valid_text(text):
	#Solicita um texto que nao esteja vazio,
	# enquanto for vazio repeti a pergunta ate da um texto valido
	while True:
		#strip() é uma função que remove espaços extras inicias e finais
		#assim temos uma melhoria em armazenamento no banco de dados
		#tambem melhoria de experiencia de utilizadores e duplicidade de dados
		value = input(text).strip()
		# Se o campo não for vazio, retorna a entrada valida e tratada
		if value:
			return value
		else:
			# print("This field can't be empty")
			print("Preencha o campo vazio")

# --- As funções abaixo vão verificar numero valido positivo,
# --- Por que sempre positivo?
# --- Se trata de numero de quantidade de pessoas,
# --- numero de reservas, quantidade de assentos,
# --- preços de produtos, sendo eles das salas tematicas e no menu
# --- Esses valores não pode ser menor que zero.

def valid_decimal(text):
	#Recebe qualquer tipo de entrada de decimal, com virgula ou ponto
	#Como por exemplo 5.4 ou 5,4
	#Garantido a usabildade do sistema
	#Tambem tratando antes de importar no banco de dados
	#A função tambem valida se o decimal é um monetário positivo válido
	while True:
		#replace() é uma função que troca um caractere por outro caractere
		value = input(text).strip().replace(",",".")
		
		#Separa as partes do numero.Ex: 12.50 -> ['12', '50']
		parts = value.split(".")

		#Verificar um numero compatível com sistema monetário
		
		#Primeiro etapa: verifica existir apenas um separado, é invalido 12.39.2
		if len(parts) > 2:
			#print("Invalid value")
			print("Valor inválido")
			#o continue garante uma nova tentativa ao utilizador
			continue
		
		#Segunda etapa: verificar se a parte inteira é um numero positivo
		if not parts[0].isdecimal():
			print("Valor inválido")
			continue

		#Terceira etapa: verificar se a parte decimal tem apenas dois digitos e digitos são validos
		if len(parts) == 2:
			if not parts[1].isdecimal():
				print("Valor inválido")
				continue
			if len(parts[1]) > 2:
				print("Valor inválido")
				continue
		
		#Quarta etapa: limitar o tamanho do valor,
		# para evitar OverflowError no banco de dados:
		# limite o float = 1.7976931348623157e+308
		# teste import sys print(sys.float_info.max)
		if len(parts[0]) > 9:
			print("Valor muito grande")
			continue

		#Depois de tratar todo o numero vamos converte para float
		return float(value)

def valid_integer(text, min=None, max=None):
	#Valida se a entrada do usuário é um inteiro positivo valido,
	#Caso tenha quantidade limite, 
	# como: quantidade de assentos e quantidade pessoas por reserva
	while True:
		value = input(text).strip()

		# Aqui verifica se o input é um numero,
		# Não aceita caracteres, espacos e numero decimais
		# isdecimal() é uma função que verifica ss os caracteres são numero entre 0 e 9
		if not value.isdecimal():
			print("Valor inválido")
			continue
		
		#Converte o str do input para int
		num = int(value)

		# Caso o valor tenha um limite de maximo e minino,
		# essa condição valida isso,
		# como o valor minino de pessoa para reserva é 1 e maximo é 8
		# mas se nao exista o limite, o valor default é none
		if min is not None and num < min:
			print (f"Insira o valor válido maior que: {min}")
		elif max is not None and num > max:
			print (f"Insira o valor válido menor que: {max}")
		else:
			return num

# --- As funções abaixo vão verificar formato de data e hora
# --- Converte para o formato valido para guarda no banco de dados
# --- --- --- --- ---- ---- --- 
# --- Formatos de data e hora utilizado pelo datatime
# --- %Y = Ano (YYYY)
# --- %m = Mês (MM)
# --- %d = Dia (DD)
# --- %H = Hora (HH)
# --- %M = Minutos (MM)
# --- %S = Segundos (SS)
# --- --- --- --- ---- ---- --- 
# --- Formato usado no SQLite
# --- Data: YYYY-MM-DD
# --- Hora: HH:MM:SS

def valid_date(text):
	#Essa função valida a entrada de data 
	while True:
		value = input(text).strip()
		try:
			# Aqui verifica se o formato passado pelo utilizador segue os formato DD/MM/YYYY
			# strptime() converte texto em data/hora e valida
			date = datetime.strptime(value, "%d/%m/%Y")
			# Converte para o formato valido do banco de dados
			# strftime() converte data/hora em texto no formato pretendido
			return date.strftime("%Y-%m-%d")
		except:
			# Caso o formato nao é valido pedi para o usuário escreve de novo
			# e mostra como deve ser inserido a data
			print("Data inválida! Use o formato DD/MM/YYYY.")

def valid_time(text):
	#Essa função valida a entrada de hora
	# Segue a mesma logica da função valid_date
	while True:
		value = input(text).strip()
		try:
			time = datetime.strptime(value,"%H:%M")
			return time.strftime("%H:%M:%S")
		except ValueError:
			print("Hora inválida! Use o formato HH:MM.")


# --- A função abaixo vai verificar as opções usadas
# --- Como por exemplo SEXO: M, F, O, fora isso nao é valido

def valid_option(text, op):
	# recebe a mensagem para input e a lista de opção
	while True:
		# upper() Deixa a str maiúscula
		value = input(text).strip().upper()
		# verifica se entrada do usuario é um opção valida.
		for option in op:
			if value == option.upper():
				return option
		print(f"Opção invalida. Escolha uma dessa opções: {', '.join(op)}.")
