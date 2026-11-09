
PRAGMA foreign_keys = ON;

BEGIN TRANSACTION;

-- Tabela de clientes
CREATE TABLE clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    data_nascimento TEXT NOT NULL,
    sexo TEXT NOT NULL CHECK (sexo IN ('M', 'F', 'O')),
    nif TEXT NOT NULL UNIQUE,
    telemovel TEXT NOT NULL,
    email TEXT NOT NULL
);

-- Tabela de salas
-- Salas vem antes de reservas porque as reservas apontam para ela
CREATE TABLE salas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tematica TEXT NOT NULL,
    capacidade INTEGER NOT NULL CHECK (capacidade > 0),
    funcionarios TEXT NOT NULL,
    custo REAL NOT NULL CHECK (custo >= 0)
);


-- Tabela de reservas
CREATE TABLE reservas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER NOT NULL,
    id_sala INTEGER NOT NULL,
    data_reserva TEXT NOT NULL,
    hora_reserva TEXT NOT NULL,
    num_pessoas INTEGER NOT NULL CHECK (num_pessoas > 0),
    valor_total REAL NOT NULL CHECK (valor_total >= 0),
    estado TEXT NOT NULL DEFAULT 'Ativa'
        CHECK (estado IN ('Ativa', 'Cancelada')),

    FOREIGN KEY (id_cliente) REFERENCES clientes (id),
    FOREIGN KEY (id_sala) REFERENCES salas (id)
);

COMMIT;
