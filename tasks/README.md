# Task Manager API

## Project Overview
This is a **Task Manager API** built with **Django** and **Django REST Framework (DRF)**. The API allows users to:
- Register and log in using Django's authentication system.
- Create tasks with descriptions, deadlines, and statuses.
- Assign tasks to multiple users.
- Retrieve all tasks assigned to a specific user.

---

## Features
- **User Authentication** (Signup & Login using Django Auth)
- **Task Management** (Create, Assign, and Retrieve Tasks)
- **Token-Based Authentication** for Secure API Calls
- **User Role Management** (Assignee)

---

## 📁 Project Structure
```
task_manager/
│-- manage.py
│-- README.md  # Documentation
│-- requirements.txt  # Dependencies
│
├── config/  # Project settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│
│
├── tasks/  # Task management module
│   ├── models.py
|   ├──api
|   │   ├── serializers.py
|   │   ├── views.py
│   ├── urls.py
│   ├── app.py
│   ├── test.py
│   ├── admin.py
│   ├── models.py
```

---

## 🛠 Installation & Setup

### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/shah5fahad/taskmanager
cd taskmanager
```

### **2️⃣ Create a Virtual Environment & Activate It**
```sh
python -m venv venv  # Create virtual environment
source venv/bin/activate  # Activate on macOS/Linux
venv\Scripts\activate  # Activate on Windows
```

### **3️⃣ Install Dependencies**
```sh
pip install -r requirements.txt
```

### **4️⃣ Configure Environment Variables**
Create a `.env` file in the root directory and set up the required environment variables. Use `.env.example` as a reference:
```sh
cp .env.example .env
```
Update the `.env` file with your database and secret key settings.

### **5️⃣ Apply Database Migrations**
```sh
python manage.py makemigrations
python manage.py migrate
```

### **6️⃣ Create a Superuser** (For Admin Access)
```sh
python manage.py createsuperuser
```
Follow the prompts to set up your admin credentials.

### **7️⃣ Run the Server**
```sh
python manage.py runserver
```
Access the API at: `http://127.0.0.1:8000/`

---

## 🔐 Authentication & API Usage
This project uses **Token-Based Authentication**.

### **1️⃣ Register a New User**
**Endpoint:** `POST /api/register/`
```json
{
    "email": "user@example.com",
    "password": "SecurePassword123",
    "name": "John Doe",
    "phone_number": "1234567890",
}
```

### **2️⃣ Login & Get Access Token**
**Endpoint:** `POST /api/login/`
```json
{
    "email": "user@example.com",
    "password": "SecurePassword123"
}
```
_Response:_
```json
{
    "token": "your_access_token_here",
    "user": {
        "id": 1,
        "email": "user@example.com",
        "name": "John Doe"
    }
}
```

**🔹 Note:** Use the token received from the login response in every authenticated API request.

### **3️⃣ Use Token for Authentication**
Pass the token in the `Authorization` header for all authenticated requests:
```sh
Authorization: Token your_access_token_here
```

### **4️⃣ Create a Task** (Authenticated API)
**Endpoint:** `POST /api/tasks/`
```json
{
    "name": "Fix Bug #123",
    "description": "Resolve issue in authentication module",
    "task_type": "BUG",
    "status": "PENDING"
}
```

### **5️⃣ Assign a Task to a User** (Authenticated API)
**Endpoint:** `POST /api/tasks/<task_id>/assign/`
```json
{
    "email": "user email",
}
```

### **6️⃣ Retrieve Tasks Assigned to a User** (Authenticated API)
**Endpoint:** `GET /api/users/tasks/?email="assignee email"`
_Response:_
```json
[
    {
        "id": 1,
        "name": "Fix Bug #123",
        "status": "Pending",
        "assignees": [
            { "id": 1, "name": "John Doe" },
            { "id": 2, "name": "Jane Doe" }
        ]
    }
]
```

---

## 🧪 Running Tests
To ensure everything works correctly, run tests:
```sh
python manage.py test
```

---

## 📜 API Endpoints
| Method | Endpoint               | Description |
|--------|------------------------|-------------|
| `POST` | `/api/register/` | Register a new user |
| `POST` | `/api/login/` | Login & get auth token |
| `POST` | `/api/tasks/` | Create a new task |
| `POST` | `/api/tasks/<mention_task_id>/assign/` | Assign a task to a user |
| `GET` | `/api/users/tasks/` | Get all tasks for a specific user |

---

## 🛠 Python Version
This project was developed using **Python 3.12.4**.

---

## 🔗 Useful Links
- [Django Documentation](https://docs.djangoproject.com/en/stable/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [GitHub Repository](https://github.com/shah5fahad/taskmanager)

---

## 👨‍💻 Author
**My Email**  
📧 Email: shahf8604@gmail.com  
