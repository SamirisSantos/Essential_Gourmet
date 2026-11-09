
-- Dados de teste - Essência Gourmet
-- Este ficheiro contém dados iniciais para testar a aplicação.
-- Inclui clientes, salas temáticas e reservas.

PRAGMA foreign_keys = ON;

BEGIN TRANSACTION;


-- =========================================
-- INSERIR CLIENTES
-- =========================================

-- A cliente Susan já foi inserida no criar_tabelas.sql.
-- Por isso, não é necessário inserir novamente.

INSERT INTO clientes
	(nome, data_nascimento, sexo, nif, telemovel, email)
VALUES
	('Mariana Costa', '1995-04-12', 'F',
	 '234567899', '912345671', 'mariana.costa@email.com'),

	('João Martins', '1988-09-23', 'M',
	 '345678915', '923456782', 'joao.martins@email.com'),

	('Carolina Ferreira', '1992-02-17', 'F',
	 '567891232', '934567893', 'carolina.ferreira@email.com'),

	('Pedro Almeida', '1985-11-30', 'M',
	 '678912343', '961234567', 'pedro.almeida@email.com');


-- =========================================
-- INSERIR SALAS
-- =========================================

INSERT INTO salas
	(tematica, capacidade, funcionarios, custo)
VALUES
	('Glamour', 8, 'Ana Silva, Miguel Costa', 80.00),

	('Espelhos', 6, 'Sofia Martins, Pedro Lopes', 60.00),

	('Latino', 10, 'Mariana Alves, João Pinto', 50.00),

	('Urbano', 4, 'Inês Ferreira', 40.00);


-- =========================================
-- INSERIR RESERVAS
-- =========================================

-- Os valores consideram o menu de 220 euros por pessoa
-- mais o custo da sala.

INSERT INTO reservas
	(id_cliente, id_sala, data_reserva, hora_reserva,
	 num_pessoas, valor_total, estado)
VALUES
	(1, 1, '2026-12-05', '19:00:00',
	 2, 520.00, 'Ativa'),

	(2, 2, '2026-12-05', '20:00:00',
	 4, 940.00, 'Ativa'),

	(3, 3, '2026-12-06', '19:30:00',
	 6, 1370.00, 'Ativa'),

	(4, 4, '2026-12-06', '20:00:00',
	 2, 480.00, 'Ativa'),

	(1, 1, '2026-12-07', '19:00:00',
	 3, 740.00, 'Ativa');

COMMIT;
