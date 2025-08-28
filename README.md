# Django REST API Assessment

A Django REST Framework application with JWT authentication, async notifications using Celery, and user connection management.

## Features

- **User Management**: Registration, login, profile, and search
- **JWT Authentication**: Secure token-based authentication with 15-minute expiration
- **Connection System**: Send/accept/reject connection requests between users
- **Async Notifications**: Background task processing using Celery
- **RESTful APIs**: Full CRUD operations with proper HTTP status codes

## Prerequisites

- Python 3.8+
- Windows OS (for Celery configuration)
- Virtual Environment

## Setup Instructions

### 1. Clone and Navigate to Project
```bash
git clone <repository-url>
cd Assesment
```

### 2. Create and Activate Virtual Environment
```powershell
# Create virtual environment
python -m venv myvenv

# Activate virtual environment
.\myvenv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 4. Database Setup
```powershell
cd backend
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser (Optional)
```powershell
python manage.py createsuperuser
```

### 6. Start Django Server
```powershell
# Terminal 1: Django Server
python manage.py runserver
```

### 7. Start Celery Worker
```powershell
# Terminal 2: Celery Worker (Windows specific)
cd c:\Users\LEGION\Desktop\Assesment
.\myvenv\Scripts\Activate.ps1
cd backend
celery -A backend worker --loglevel=info --pool=gevent --concurrency=1000
```

## API Endpoints

### Base URL
```
http://127.0.0.1:8000/api/
```

### Authentication Endpoints

#### User Registration
- **POST** `/users/register/`
- **Body**: JSON
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepassword123",
  "full_name": "John Doe",
  "contact": "1234567890",
  "company": "Tech Corp",
  "address": "123 Main Street, New York, NY 10001",
  "industry": "Technology"
}
```

#### User Login
- **POST** `/users/login/`
- **Body**: JSON
```json
{
  "username": "john_doe",
  "password": "securepassword123"
}
```

#### Token Refresh
- **POST** `/users/token/refresh/`
- **Body**: JSON
```json
{
  "refresh": "your_refresh_token_here"
}
```

### User Management Endpoints

#### Get User Profile
- **GET** `/users/profile/`
- **Headers**: `Authorization: Bearer <access_token>`

#### Update User Profile
- **PUT** `/users/profile/`
- **Headers**: `Authorization: Bearer <access_token>`
- **Body**: JSON (any user fields to update)

#### Search Users
- **GET** `/users/search/?q=john`
- **Headers**: `Authorization: Bearer <access_token>`

### Connection Endpoints

#### Send Connection Request
- **POST** `/connections/request/`
- **Headers**: `Authorization: Bearer <access_token>`
- **Body**: JSON
```json
{
  "receiver": "target_username",
  "message": "Let's connect!"
}
```

#### List Connections
- **GET** `/connections/`
- **Headers**: `Authorization: Bearer <access_token>`
- **Query Parameters**:
  - `status`: `pending`, `accepted`, `rejected`
  - `type`: `sent`, `received`, `all`

#### Respond to Connection Request
- **POST** `/connections/respond/<connection_id>/`
- **Headers**: `Authorization: Bearer <access_token>`
- **Body**: JSON
```json
{
  "action": "accept"
}
```

### Notification Endpoints

#### List Notifications
- **GET** `/notifications/`
- **Headers**: `Authorization: Bearer <access_token>`

#### Mark Notification as Read
- **POST** `/notifications/<notification_id>/mark-read/`
- **Headers**: `Authorization: Bearer <access_token>`

## Sample Test Data

### Test Users

#### User 1
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepassword123",
  "full_name": "John Doe",
  "contact": "1234567890",
  "company": "Tech Corp",
  "address": "123 Main Street, New York, NY 10001",
  "industry": "Technology"
}
```

#### User 2
```json
{
  "username": "jane_smith",
  "email": "jane@example.com",
  "password": "securepassword456",
  "full_name": "Jane Smith",
  "contact": "0987654321",
  "company": "Digital Solutions",
  "address": "456 Oak Avenue, Los Angeles, CA 90210",
  "industry": "Marketing"
}
```

#### User 3
```json
{
  "username": "mike_wilson",
  "email": "mike@example.com",
  "password": "securepassword789",
  "full_name": "Mike Wilson",
  "contact": "5551234567",
  "company": "Innovation Labs",
  "address": "789 Pine Street, Chicago, IL 60601",
  "industry": "Research"
}
```

## Testing Guide with Postman

### Step 1: Register Users
1. **POST** `http://127.0.0.1:8000/api/users/register/`
2. Use the sample user data above
3. Register all three users

### Step 2: Login and Get Tokens
1. **POST** `http://127.0.0.1:8000/api/users/login/`
2. Login with each user to get their access tokens
3. Save the `access` tokens for API calls

### Step 3: Test Connection Requests
1. **POST** `http://127.0.0.1:8000/api/connections/request/`
2. **Headers**: 
   - `Content-Type: application/json`
   - `Authorization: Bearer <john_doe_token>`
3. **Body**:
```json
{
  "receiver": "jane_smith",
  "message": "Hi Jane, let's connect!"
}
```
4. Watch the Celery terminal for async notification processing

### Step 4: Test Connection Response
1. Login as `jane_smith` to get her token
2. **GET** `http://127.0.0.1:8000/api/connections/` to see pending requests
3. **POST** `http://127.0.0.1:8000/api/connections/respond/<connection_id>/`
4. **Body**:
```json
{
  "action": "accept"
}
```

### Step 5: Test Notifications
1. **GET** `http://127.0.0.1:8000/api/notifications/`
2. Check notifications for both users
3. Mark notifications as read using the mark-read endpoint

## Async Functionality Verification

### What to Watch For:
1. **Django Terminal**: Shows API requests and responses
2. **Celery Terminal**: Shows async task processing
3. **Expected Flow**:
   - API call creates connection → immediate response
   - Celery picks up notification task → processes in background
   - Notification created in database

### Sample Celery Output:
```
[2025-08-28 15:13:04,725: INFO/MainProcess] Task notifications.tasks.send_connection_notification[7a48123b-63e5-4704-a087-1b4f875dacd1] received
[2025-08-28 15:13:04,793: INFO/MainProcess] Task notifications.tasks.send_connection_notification[7a48123b-63e5-4704-a087-1b4f875dacd1] succeeded in 0.046s: 'Notification sent for connection_request'
```

## Architecture

### Technology Stack
- **Backend**: Django 5.0.14 + Django REST Framework
- **Authentication**: JWT (django-rest-framework-simplejwt)
- **Database**: SQLite
- **Task Queue**: Celery with SQLite broker
- **Async Pool**: Gevent (Windows compatible)

### Key Models
- **User**: Custom user model with additional fields
- **Connection**: Manages user connections with status tracking
- **Notification**: Stores async notifications

### Security Features
- JWT authentication with short expiration
- User permission checks
- Input validation and sanitization
- CORS configuration for development

## Troubleshooting

### Common Issues

#### Celery Worker Not Starting
```powershell
# Install required packages
pip install eventlet gevent

# Use correct pool for Windows
celery -A backend worker --loglevel=info --pool=gevent --concurrency=1000
```

#### Authentication Errors
- Ensure Bearer token format: `Bearer <token>`
- Check token expiration (15 minutes)
- Verify proper Authorization header

#### Database Issues
```powershell
# Reset database if needed
python manage.py flush
python manage.py migrate
```

## Development Notes

- JWT tokens expire in 15 minutes for security
- Celery uses SQLite broker for simplicity
- Windows requires gevent/eventlet pool for Celery
- CORS is enabled for development only
- All endpoints require authentication except registration/login

## Production Considerations

- Use Redis/RabbitMQ for Celery broker in production
- Configure proper CORS origins
- Use PostgreSQL/MySQL for database
- Set up proper logging and monitoring
- Implement rate limiting
- Use HTTPS in production

## License

This project is for assessment purposes.
