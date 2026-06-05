# Bank API Challenge

This project is a simplified Bank API built with **FastAPI**, focusing on user registration, authentication via JWT, and basic financial transactions (deposits and withdrawals).

## 🏗️ System Infrastructure & Architecture

The project follows a modular structure to separate concerns and improve maintainability:

-   **`main.py`**: The entry point of the application located at the project root. It defines the FastAPI instance, routes (endpoints), and application startup logic.
-   **`models/models.py`**: Contains the **SQLAlchemy** database models (User, Account, Transaction), representing the relational structure of the system.
-   **`database.py`**: Manages the database connection using **aiosqlite** for asynchronous SQLite operations and sets up the SQLAlchemy `AsyncSession`.
-   **`services/account.py`**: Provides specialized account management services using lower-level query interfaces.
-   **`services/services.py`**: Encapsulates the business logic for banking operations (depositing money, withdrawing, and fetching statements).
-   **`schemas/schemas.py`**: Defines **Pydantic** models for data validation, serialization, and API documentation (Request/Response bodies).
-   **`auth.py`**: Handles security concerns, specifically JWT token generation for authenticated sessions.
-   **`requirements.txt`**: Lists all necessary Python packages and dependencies for the project.
-   **`exception.py`**: Custom exception classes for business logic and account errors.

## 🛠️ Technology Stack

-   **Framework**: FastAPI (Asynchronous Python web framework)
-   **Database**: SQLite (local file-based storage)
-   **ORM**: SQLAlchemy (Asynchronous support via `ext.asyncio`)
-   **Driver**: `aiosqlite`
-   **Authentication**: JWT (JSON Web Tokens) via `python-jose`
-   **Security**: Password hashing with `passlib` (bcrypt)

## 🚀 Getting Started

### 1. Environment Setup

It is recommended to use a virtual environment to manage dependencies:

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment (Linux/WSL)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Running the Application

To start the development server, run:

```bash
uvicorn main:app --reload
```
The API will be available at `http://127.0.0.1:8000`.

### 3. Documentation

FastAPI automatically generates interactive documentation:
-   **Swagger UI**: `http://127.0.0.1:8000/docs`
-   **ReDoc**: `http://127.0.0.1:8000/redoc`

## 🔑 Key Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/auth/login` | Authenticate user and receive a JWT token. |
| `GET`  | `/accounts` | List accounts with pagination. |
| `POST` | `/accounts` | Create a new financial account. |
| `POST` | `/transactions` | Perform a financial transaction (deposit/withdrawal). |
| `GET`  | `/accounts/{id}/transactions` | Retrieve transaction history for a specific account. |

## 🗄️ Data Model

-   **User**: `id`, `username`, `password` (hashed).
-   **Account**: `id`, `user_id` (FK), `balance`.
-   **Transaction**: `id`, `account_id` (FK), `type`, `amount`, `created_at`.

## 🧹 Maintenance & Best Practices

-   **Environment Isolation**: The `venv/` directory is ignored by Git to keep the repository lightweight and cross-platform compatible. Dependencies are managed via `requirements.txt`.
-   **Local Database**: The `bank.db` file is ignored to prevent local test data from being committed.
-   **Security**: Always ensure sensitive files like `.env` are listed in `.gitignore`.
-   **Error Handling**: Global exception handlers in `main.py` catch `BusinessError` and `AccountNotFoundError` to return standardized JSON responses.

## ⚠️ Important Notes

-   **Security**: The `SECRET_KEY` in `auth.py` is currently set to a default value. For production environments, this should be moved to an environment variable.
-   **Modular Imports**: The project uses absolute imports prefixed with `src.` to maintain compatibility with the modular structure.
-   **Concurrency**: The project uses `aiosqlite` and `AsyncSession` to ensure that database I/O does not block the event loop, allowing for high-performance request handling.
-   **Database Lifecycle**: The system automatically creates database tables on startup and manages sessions through an asynchronous dependency (`get_db`).

---
