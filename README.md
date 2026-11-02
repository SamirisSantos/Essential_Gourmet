# Essencial Gourmet: Reservation Management

A console application in Python to manage costumers, thmed rooms and reservation for a dining restaurant

This project was developed for the **Python Programming** modulo of the **Data Analysis** course at **CEASE Digital**.

## Description

Essencial Gourmet is a luxury restaurant that offers only tasting menus, serverd in themed rooms with a limited number of seats and dedicated staf. Reservations used to be handle by phone and paper notes, withc led to scheduling erros and overlapping bookings.

This applications helps the administrative team manege reservations in a simple and accurate way. It controls room availability, prevents bookings that exceed a room's capacity and calculates the total prices of each reservation automatically.

All data is stored in a local SQLite database, and any unexpected error is wirtten to a log file.

## Instructions

### Requirements

- Pyhton 3.11 or higher

### Installation

```
git clone <https://github.com/SamirisSantos/Essential_Gourmet.git>
```

### Runnig the application

```
python main.py
```

On the first run, the `data/`folder and the database table are created automatically

### Project structure

```
├── main.py                  # main menu
├── README.md
├── db/
│   └── database.py          # database connection and schema
├── modules/
│   ├── customers.py         # customer management
│   ├── rooms.py             # room and employee management
│   └── reservations.py      # reservations and availability
├── utils/
│   ├── config.py            # shared constants
│   ├── logger.py            # error log setup
│   └── validations.py       # shared input validation
└── data/                    # created automatically
    ├── data.db
    └── errors.log
```

## Features

**Customers**


**Rooms**


**Reservations**


**General**

------

👩‍💻 Samiris Santos — [LinkedIn](https://www.linkedin.com/in/samiris-santos/)

*Python Programming | Data Analysis course | CEASE Digital*