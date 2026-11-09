# 🍽️ Essência Gourmet — Reservation Management System

A Python console application for managing customers, themed rooms, and reservations at a luxury fine-dining restaurant.

This project was developed as a **team project** for the **Python Programming** module of the **Data Analysis** course at **CEASE Digital**.

## 📖 About the Project

**Essência Gourmet** is a fictional luxury restaurant specialising in exclusive tasting menus, served in themed rooms with limited seating capacity and dedicated staff.

Previously, reservations were managed manually through phone calls and paper records, which could lead to scheduling errors, overlapping bookings, and difficulties managing room availability.

This application aims to simplify and improve the restaurant's administrative processes by providing an organised system for managing customers, rooms, and reservations.

It checks room availability, prevents bookings that exceed room capacity or overlap with existing reservations, and automatically calculates the total reservation cost.

All information is stored in a local **SQLite database**, while unexpected errors are recorded in a log file.

## ✨ Features

### Customers
- Register new customers.
- View and search customer information.
- Update existing customer records.
- Validate customer information before saving it.

### Rooms
- Register themed rooms.
- View and update room information.
- Manage room capacity, assigned staff, and costs.
- Validate room information.

### Reservations
- Create new reservations.
- View reservation details.
- Check room availability based on capacity and reservation duration.
- Prevent overlapping reservations.
- Automatically calculate the total reservation cost.
- Cancel existing reservations.

### General
- Interactive console-based menu.
- Input validation.
- SQLite database integration.
- Automatic database initialisation on the first run.
- Automatic insertion of test data during initialisation.
- Error logging.

## 🛠️ Technologies

- **Python 3.11+**
- **SQLite**
- **SQL**
- **Git & GitHub**

## 🚀 Getting Started

### Requirements

- Python 3.11 or higher
- Git

### Installation

Clone the repository:

```bash
git clone https://github.com/SamirisSantos/Essential_Gourmet.git
```

Navigate to the project directory:

```bash
cd Essential_Gourmet
```

### Running the Application

Run the main file:

```bash
python main.py
```

On the first run, the application checks whether the database exists. If it does not, it creates the database, executes the SQL scripts to create the tables, and inserts the test data.

On subsequent runs, the existing database is reused, preventing the test data from being inserted again.

## 📁 Project Structure

```text
Essential_Gourmet/
│
├── main.py                  # Application entry point and main menu
├── README.md                # Project documentation
│
├── data/
│   ├── criar_tabelas.sql    # Database table creation script
│   ├── dados_teste.sql      # Test data insertion script
│   └── essencia_gourmet.db  # SQLite database (generated)
│
├── db/
│   └── database.py          # Database connection
│
├── modules/
│   ├── customers.py         # Customer management
│   ├── rooms.py             # Room management
│   └── reservations.py      # Reservation management and availability
│
└── utils/
    ├── config.py            # Shared constants and configuration
    ├── logger.py            # Error logging
    └── validations.py       # Input validation functions
```

## 👩‍💻
**Samiris Santos** — [LinkedIn](https://www.linkedin.com/in/samiris-santos/)

*Python Programming | Data Analysis Course | CEASE Digital*