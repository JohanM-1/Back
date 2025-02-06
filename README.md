# Meta Snake Backend API

A robust Python-based backend API for the Meta Snake project, designed to manage snake information, user authentication, and geolocation data.

## 🚀 Technologies Used

### Core Framework
- **FastAPI** - Modern, fast web framework for building APIs with Python
- **Uvicorn** - Lightning-fast ASGI server implementation

### Database & ORM
- **PostgreSQL** - Primary database for storing application data
- **SQLAlchemy** - Powerful SQL toolkit and ORM
  - Using async SQLAlchemy for non-blocking database operations
  - Custom models and relationships
  - Migration support

### Authentication & Security
- **Firebase Authentication** - For secure user authentication
- **JWT (JSON Web Tokens)** - For secure API authorization
- **OAuth2** - Implementation for token-based security
- **Passlib** - Password hashing and verification

### Additional Features
- **CORS Middleware** - Cross-Origin Resource Sharing support
- **Pydantic** - Data validation using Python type annotations
- **Async Support** - Asynchronous operations throughout the application

## 🏗 Project Structure

The project follows a modular architecture:

## 🔑 Key Features

- User Authentication (Firebase + JWT)
- Snake Information Management
- Geolocation Tracking
- User Reports & Comments
- Role-based Access Control
- Image Storage Support
- Secure Password Handling

## 🛠 Setup & Installation

1. Clone the repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```
3. Set up environment variables in `.env`
4. Initialize the database
5. Run the server:
```bash
uvicorn main:app --reload
```

## 🔒 Environment Variables

Required environment variables:
- `DB_HOST`
- `DB_PORT`
- `DB_USER`
- `DB_PASSWORD`
- `DB_NAME`
- Firebase configuration variables

## 📚 API Documentation

Once running, access the API documentation at:
- Swagger UI: `/docs`
- ReDoc: `/redoc`

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.
