# Cinema Ticket Reservation System

A modular console-based cinema ticket reservation system built with Python and Object-Oriented Programming (OOP).

This project was developed as a learning-focused backend practice project to improve skills in:

- Object-Oriented Programming (OOP)
- Modular architecture
- Service-layer design
- JSON-based storage
- Authentication & validation
- Logging
- Testing with pytest
- Clean project structure

---

## Features

### Authentication System
- User registration and login
- Password hashing with salt
- Username uniqueness validation
- Password validation (min 8 chars, uppercase, lowercase)
- Hidden password input using `getpass`

### Movie & Showtime System
- Add and manage movies
- Multiple showtimes per movie
- Smart seat selection system
- Automatic seat unavailability after reservation

### Ticket Reservation
- Reserve tickets
- Cancel tickets
- View my tickets
- Age restriction validation

### Wallet System
- Deposit money
- Balance validation
- Prevent negative or invalid transactions

### Subscription System
- **Bronze** (Default): No extra benefits
- **Silver**: 20% cashback + 3 reservation credits
- **Gold**: 50% discount + Free drink

### Logging & Testing
- Comprehensive error, transaction and auth logging
- Unit tests with `pytest`

---

## Technologies Used

- Python 3.12
- OOP Principles
- JSON-based persistence
- Pytest
- Logging module
- UUID, Decimal, Enum, Datetime

---

## Project Structure

cinema-ticket-system/
├── .gitignore
├── admin_script.py
├── main.py
├── pytest.ini
├── testing.py
├── user_script.py
├── __init__.py
│
├── core/
│   ├── enums.py
│   ├── movie.py
│   ├── seat.py
│   ├── showtime.py
│   ├── subscription.py
│   ├── ticket.py
│   ├── user.py
│   └── __init__.py
│
├── data/
│   ├── movies.json
│   ├── showtimes.json
│   ├── subscriptions.json
│   ├── tickets.json
│   └── users.json
│
├── logs/
│   └── cinematicket.log
│
├── services/
│   ├── admin_service.py
│   ├── auth_service.py
│   ├── gateway.py
│   ├── gateway_service.py
│   ├── movie_service.py
│   ├── reservation_service.py
│   ├── subscription_service.py
│   ├── user_service.py
│   └── __init__.py
│
├── storage/
│   ├── file_paths.py
│   ├── json_storage.py
│   └── __init__.py
│
├── tests/
│   ├── test_admin_service.py
│   ├── test_auth_service.py
│   ├── test_movie.py
│   ├── test_movie_service.py
│   ├── test_reservation.py
│   ├── test_showtime.py
│   ├── test_subscription.py
│   ├── test_subscription_service.py
│   ├── test_ticket.py
│   ├── test_user.py
│   ├── test_user_service.py
│   └── __init__.py
│
├── utils/
│   ├── console.py
│   ├── exceptions.py
│   ├── logger.py
│   ├── security.py
│   └── __init__.py
│
└── venv/

---

# How to Run

## Clone the repository

```bash
git clone <your-repository-url>
cd cinema-ticket-system
```

## Create and activate virtual environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

## Install dependencies

```bash
pip install pytest
```

---

# Run the Application

## User Mode

```bash
python main.py
```

## Admin Mode

```bash
python main.py --admin
```

### Default Admin Credentials

```text
username: admin
password: Admin123
```

---

# Run Tests

```bash
pytest
```

---

# Notes

- This project uses JSON files for data persistence (educational purpose).
- Payment gateway is simulated.
- Focused on clean architecture, OOP, and modularity.

---

# Future Improvements

- Replace JSON with PostgreSQL / SQLite
- Web version with Django or FastAPI
- Real payment integration
- JWT authentication
- Docker support
- REST API
- Advanced seat map visualization

---

# Author

Built by Mary as a backend learning project.

Learning Project — Feel free to fork and improve!