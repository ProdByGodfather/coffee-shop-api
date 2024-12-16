# Coffee Shop Backend Project

This is a **FastAPI** project that serves as the backend for a coffee shop application. The project includes account management, token-based authentication using **JWT**, and CRUD operations for coffee and cart management. The [**AbarORM**](https://prodbygodfather.github.io/abarorm/) library is used as the ORM with **SQLite** as the database.

This project has only educational and evaluation value and probably does not work as a powerful and complete project.

---


## Features

### Authentication and Authorization
- **JWT Token-based Authentication**:
  - Login and register functionality for users.
  - Token creation for secure access to protected endpoints.
- **Access Levels**:
  - **Superuser**: Can create, update, and delete coffee items.
  - **Regular User**: Can browse coffee items and add them to their cart.

### Coffee Management
- CRUD operations for coffee items:
  - **Create**: Superusers can add new coffee items.
  - **Read**: All users can view the list of available coffee items.
  - **Update**: Superusers can edit existing coffee items.
  - **Delete**: Superusers can remove coffee items.

### Cart Management
- Users can add coffee items to their cart.
- Users can view and manage items in their cart.

### Database
- **SQLite** as the database.
- **AbarORM** for ORM functionality, simplifying database operations.

---

## Setup and Installation

### Prerequisites
- Python 3.8 or higher

### Installation Steps
1. Clone the repository:
   ```bash
   git clone git@github.com:ProdByGodfather/coffee-shop-api.git
   cd coffee-shop-api
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the FastAPI server:
   ```bash
   python main.py
   ```

5. Open your browser and navigate to:
   - **API Documentation**: [http://127.0.0.1:8765/docs](http://127.0.0.1:8000/docs)
   - **ReDoc Documentation**: [http://127.0.0.1:8765/redoc](http://127.0.0.1:8000/redoc)

---


## Environment Variables

The following environment variables can be configured in a `.env` file:

| Variable       | Description                | Default Value |
|----------------|----------------------------|---------------|
| `UPLOAD_DIR`   | Upload Folder for images   | `uploads`     |
| `USERNAME`     | Default Superuser Username | `godfather`   |
| `PASSWORD`     | Default Superuser Password | `123`         |
| `DB_NAME`      | Database Name              | `coffee.db`   |
| `HOST`         | Project executive host     | `localhost`   |
| `DB_PATH`      | Project executive port     | `8765`        |

---

## Dependencies

The project relies on the following libraries:
- **FastAPI**: Web framework for building APIs.
- **AbarORM**: ORM for database management.
- **SQLite**: Lightweight database solution.
- **Pydantic**: Data validation and settings management.

Install all dependencies using the `requirements.txt` file.

---

## Project Structure

```
.
├── account
│   ├── models.py        # Database models for account management
│   ├── schemas.py       # Pydantic schemas for account-related data validation
│   └── views.py         # Account-related API endpoints
├── cart
│   ├── models.py        # Database models for the cart
│   ├── schemas.py       # Pydantic schemas for cart-related data validation
│   └── views.py         # Cart-related API endpoints
├── coffee
│   ├── models.py        # Database models for coffee items
│   ├── schemas.py       # Pydantic schemas for coffee-related data validation
│   └── views.py         # Coffee-related API endpoints
├── coffee.db            # SQLite database file
├── config
│   ├── db.py            # Database configuration
│   ├── events.py        # Application event handlers (e.g., startup/shutdown)
│   ├── settings.py      # Application settings and configurations
│   └── urls.py          # URL routing for the project
├── extensions
│   └── password_hasher.py  # Utility for hashing passwords
├── main.py              # Main entry point of the application
├── requirements.txt     # Python dependencies
├── token_config
│   ├── config.py        # JWT configuration
│   ├── creator.py       # JWT token creation utilities
│   ├── urls.py          # URL routing for token-related endpoints
│   └── views/main.py    # Token-related API endpoints
└── uploads              # Directory for image uploads
```

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## Contributing

Contributions are welcome! Feel free to submit a pull request or open an issue to discuss changes.

---

## Author

[**Dokey (دکتر)**](https://github.com/ProdByGodfather/)

