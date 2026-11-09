import sqlite3

from utils.config import DB_PATH

def ligar():
	connection = sqlite3.connect(DB_PATH)
	# Ativa a verificação das chaves estrangeiras
	connection.execute("PRAGMA foreign_keys = ON")
	# Permite converter os resultados em dicionários
	connection.row_factory = sqlite3.Row
	return connection

