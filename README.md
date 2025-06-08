# FastAPI Blog API

A modern blog API built with FastAPI, featuring JWT authentication and post management.

## Features

- 🔐 JWT Authentication (signup/login)
- 📝 Post Management (CRUD operations)
- 💾 SQLAlchemy with async support
- 🗄️ Database migrations with Alembic
- ⚡ In-memory caching (5 minutes)
- 📏 Request size limiting (1MB)
- 🛡️ Password hashing with bcrypt
- 📚 Auto-generated API documentation

## Quick Start
git clone https://github.com/Andrey1224/TestTask.git
cd TestTask
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

alembic upgrade head

uvicorn app.main:app --reload

.env file 
MYSQL_URL="sqlite+aiosqlite:///./test.db"
JWT_SECRET="my_super_secret_key"
JWT_ALG="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=60


Open documentation:
Swagger UI: http://127.0.0.1:8000/docs
ReDoc: http://127.0.0.1:8000/redoc

API Endpoints
Authentication
POST /auth/signup - Register new user
POST /auth/login - User authentication
Posts (Protected Routes)
POST /posts/ - Create new post
GET /posts/ - Get user posts (cached for 5 minutes)
DELETE /posts/{id} - Delete specific post
System
GET / - API information
GET /health - Health check

Register a new user
curl -X POST http://127.0.0.1:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"strongpass123"}'

Login and get token
curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"strongpass123"}'

Create a post (with token)
curl -X POST http://127.0.0.1:8000/posts/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"text":"My first blog post!"}'

Get all posts  
curl http://127.0.0.1:8000/posts/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

Delete a post
curl -X DELETE http://127.0.0.1:8000/posts/1 \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"  

