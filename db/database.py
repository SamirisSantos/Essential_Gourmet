import sqlite3

from utils.config import DB_PATH

def ligar():
	#Cria a licação com a base de dados
	connetion = sqlite3.connect(DB_PATH)

	#Perminte acessar os dados pelos nome das colunas
	connetion.row_factory = sqlite3.Row

	return connetion

