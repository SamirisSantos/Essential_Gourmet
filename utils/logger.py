#Registo de erros num ficheiro de texto (log.txt), com data e hora
#logging é uma biblioteca que registar mensagens (erros, avisos, informação)
# pode mostrar na tela ou grava no arquivo
import logging

from utils.config import LOG_PATH

# Configuração feita uma vez, quando o ficheiro é importado.
# Cada linha fica: data e hora | nível | mensagem
logging.basicConfig(
	filename=LOG_PATH,
	level=logging.ERROR,
	format="%(asctime)s | %(levelname)s | %(message)s",
	datefmt="%d/%m/%Y %H:%M:%S",
	encoding="utf-8",
)

def register_error(origin, error):
	#Escreve um erro no ficheiro de log.
	#origin: onde aconteceu (ex: 'rooms.insert_room')
	#error: o erro apanhado no except
	logging.error("%s -> %s", origin, error)