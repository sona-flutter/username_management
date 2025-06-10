# User Management API

A Flask-based REST API for managing users with CRUD operations, SQLite database, and Swagger UI documentation.

## 🚀 Quick Start

### Option 1: Automatic Setup (Windows)
1. Copy this entire folder to your machine
2. Double-click `setup.bat`
3. The script will automatically install dependencies and start the server

### Option 2: Manual Setup
1. Ensure Python 3.12+ is installed
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python app.py
   ```

## 📋 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/users` | Get all users |
| POST | `/users` | Create a new user |
| GET | `/users/{id}` | Get user by ID |
| PUT | `/users/{id}` | Update user by ID |
| DELETE | `/users/{id}` | Delete user by ID |

## 🌐 Access URLs

- **Local**: http://localhost:5000
- **Network**: http://[YOUR_IP]:5000
- **Swagger UI**: http://localhost:5000/swagger/
- **API Docs**: http://localhost:5000/static/swagger.json

## 📖 Swagger Documentation

Access the interactive API documentation at:
http://localhost:5000/swagger/

## 🗄️ Database

Uses SQLite database (`user_management.db`) - no additional database setup required.

## 📝 User Schema

```json
{
  "user_name": "string",
  "user_nick_name": "string", 
  "phone_no": "string",
  "user_address": "string",
  "user_email": "string",
  "user_bio": "string",
  "user_date_of_birth": "2025-06-10",
  "user_age": 30
}
```

## 🔧 Configuration

The application runs on:
- **Host**: 0.0.0.0 (accessible from network)
- **Port**: 5000
- **Debug**: Enabled

## 📦 Dependencies

- Flask 2.3.3
- Flask-SQLAlchemy 3.1.1
- Flask-Marshmallow 0.15.0
- Flask-CORS 4.0.0
- Flask-Swagger-UI 4.11.1
- Marshmallow-SQLAlchemy 0.29.0
- PyMySQL 1.1.0
- Python-dotenv 1.0.0

## 🚨 Troubleshooting

1. **CORS Errors**: Fixed with Flask-CORS
2. **Database Errors**: Uses SQLite (no MySQL required)
3. **Network Access**: Runs on 0.0.0.0 for network accessibility
4. **Port Conflicts**: Change port in `app.py` if needed

## 📱 Testing the API

### Create a User (POST /users)
```bash
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{"user_name": "John Doe", "user_email": "john@example.com", "user_age": 30}'
```

### Get All Users (GET /users)
```bash
curl http://localhost:5000/users
```

### Get User by ID (GET /users/1)
```bash
curl http://localhost:5000/users/1
``` 