# Essência Gourmet

## Sobre o projeto

Este projeto foi desenvolvido em equipa do módulo de **Python Programming**, integrado no curso de **Análise de Dados** da **CEASE Digital**.

O objetivo é desenvolver uma aplicação em Python para a gestão do restaurante fictício **Essência Gourmet, Lda.**, um restaurante de luxo especializado em menus de degustação de alta gastronomia.

A aplicação procura simplificar e organizar a gestão de clientes, salas temáticas e reservas, garantindo o controlo da disponibilidade das salas e evitando conflitos de horários.

## Equipa

Projeto desenvolvido em equipa por:

- **Samiris Santos**
- **João Carvalho**
- **Gonçalo Santos**

## Funcionalidades

A aplicação permite:

- **Gestão de clientes:** registar, consultar, pesquisar e atualizar informações dos clientes.
- **Gestão de salas:** registar, consultar e atualizar salas temáticas, incluindo a respetiva capacidade, funcionários e custo.
- **Gestão de reservas:** criar, consultar e cancelar reservas.
- **Verificação de disponibilidade:** verificar a capacidade das salas e evitar sobreposição de reservas.
- **Validação de dados:** garantir que os dados introduzidos pelo utilizador respeitam os critérios definidos.
- **Registo de erros:** guardar informações sobre erros ocorridos durante a execução da aplicação.

## Tecnologias utilizadas

- Python
- SQLite
- SQL

## Estrutura do projeto

```text
Essencia-Gourmet/
│
├── main.py                  # Menu principal da aplicação
├── README.md                # Documentação do projeto
│
├── data/
│   └── essencia_gourmet.db  # Base de dados SQLite
│
├── sql/
│   ├── criar_tabelas.sql    # Criação das tabelas
│   └── dados_teste.sql      # Inserção de dados de teste
│
├── db/
│   └── database.py          # Ligação à base de dados
│
├── modules/
│   ├── customers.py         # Gestão de clientes
│   ├── rooms.py             # Gestão de salas e funcionários
│   └── reservations.py      # Gestão de reservas e disponibilidade
│
└── utils/
    ├── config.py            # Constantes e configurações
    ├── logger.py            # Registo de erros
    └── validations.py       # Validação de dados de entrada
```

## Base de dados

A aplicação utiliza SQLite para armazenar os dados de forma persistente.

Os scripts SQL estão organizados na pasta `sql/`:

- `criar_tabelas.sql`: cria a estrutura da base de dados.
- `dados_teste.sql`: insere dados de exemplo para facilitar os testes da aplicação.

A base de dados `essencia_gourmet.db` fica armazenada na pasta `data/`.

## Execução da aplicação

Para executar a aplicação, basta correr o ficheiro principal a partir da pasta do projeto:

```bash
python main.py
```

---

## 👩‍💻
**Samiris Santos** — [LinkedIn](https://www.linkedin.com/in/samiris-santos/)

*Python Programming | Data Analysis Course | CEASE Digital*