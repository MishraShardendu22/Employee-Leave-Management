# Employee Leave Management System

> **🎨 Development Note**: This application was vibe-coded! The database schema, API routes, frontend design, UI components, and theme palette were crafted manually without AI assistance. The rest of the codebase was developed with AI assistance and thoroughly reviewed by a human developer.

A comprehensive RESTful API for managing employee leave requests, approvals, and balances built with FastAPI and PostgreSQL.

## Features

- **Authentication & Authorization**: JWT-based authentication for admins, managers, and employees
- **User Management**: Separate roles for admins, managers, and employees
- **Leave Management**: Create, view, update, and delete leave requests
- **Approval Workflow**: Managers can approve or reject leave requests
- **Leave Balance Tracking**: Track allocated, used, and remaining leave balances
- **Audit Logging**: Complete audit trail of all system actions
- **Multiple Leave Types**: Support for various leave types (sick, casual, annual, etc.)

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **PostgreSQL**: Robust relational database
- **Pydantic**: Data validation using Python type annotations
- **JWT**: Secure token-based authentication
- **Passlib**: Password hashing and verification

## Database Schema

The system includes the following tables:

- `admins`: System administrators
- `employees`: Regular employees
- `managers`: Managers who approve leave requests
- `leave_types`: Types of leave (sick, casual, annual, etc.)
- `leaves`: Leave requests
- `approvals`: Manager approval/rejection decisions
- `leave_balance`: Employee leave balance tracking
- `audit_logs`: System audit trail

## Installation

1.**Clone the repository**

```bash
git clone <repository-url>
cd EmployeeLeaveManagement
```

2.**Install dependencies using uv**

```bash
uv sync
```

3.**Set up PostgreSQL database**

```bash
# Create database
createdb leave_management

# Or use the SQL schema
psql -U postgres -d leave_management -f schema.sql
```

4.**Configure environment variables**

```bash
cp .env.example .env
# Edit .env with your database credentials and secret key
```

5.**Initialize the database**

```bash
python init_db.py
```

## Running the Application

Start the development server:

```bash
uvicorn main:app --reload
```

Or run directly:

```bash
python main.py
```

The API will be available at: `http://localhost:8000`

## API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: <http://localhost:8000/docs>
- **ReDoc**: <http://localhost:8000/redoc>

## API Endpoints

### Authentication

- `POST /auth/login/admin` - Admin login
- `POST /auth/login/employee` - Employee login
- `POST /auth/login/manager` - Manager login

### Admins

- `POST /admins/` - Create admin
- `GET /admins/` - Get all admins
- `GET /admins/{admin_id}` - Get admin by ID

### Employees

- `POST /employees/` - Create employee
- `GET /employees/` - Get all employees
- `GET /employees/{employee_id}` - Get employee by ID
- `PUT /employees/{employee_id}` - Update employee
- `DELETE /employees/{employee_id}` - Delete employee

### Managers

- `POST /managers/` - Create manager
- `GET /managers/` - Get all managers
- `GET /managers/{manager_id}` - Get manager by ID

### Leave Types

- `POST /leave-types/` - Create leave type
- `GET /leave-types/` - Get all leave types
- `GET /leave-types/{type_id}` - Get leave type by ID

### Leaves

- `POST /leaves/` - Create leave request
- `GET /leaves/` - Get all leaves
- `GET /leaves/pending` - Get pending leaves
- `GET /leaves/employee/{employee_id}` - Get employee's leaves
- `GET /leaves/{leave_id}` - Get leave by ID
- `DELETE /leaves/{leave_id}` - Delete leave request

### Approvals

- `POST /approvals/` - Create approval decision
- `GET /approvals/manager/{manager_id}` - Get manager's approvals
- `GET /approvals/leave/{leave_id}` - Get leave approval

### Leave Balances

- `POST /leave-balances/` - Create leave balance
- `GET /leave-balances/employee/{employee_id}` - Get employee's balances
- `GET /leave-balances/{balance_id}` - Get balance by ID

### Audit Logs

- `GET /audit-logs/` - Get all audit logs
- `GET /audit-logs/actor/{actor_type}/{actor_id}` - Get logs by actor

## Example Usage

### 1.Create an Employee

```bash
curl -X POST "http://localhost:8000/employees/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "password123"
  }'
```

### 2.Login as Employee

```bash
curl -X POST "http://localhost:8000/auth/login/employee" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "password123"
  }'
```

### 3.Create Leave Request

```bash
curl -X POST "http://localhost:8000/leaves/?employee_id=1" \
  -H "Content-Type: application/json" \
  -d '{
    "type_id": 1,
    "start_time": "2025-12-01T00:00:00",
    "end_time": "2025-12-05T00:00:00",
    "reason": "Medical appointment"
  }'
```

### 4.Manager Approves Leave

```bash
curl -X POST "http://localhost:8000/approvals/?manager_id=1" \
  -H "Content-Type: application/json" \
  -d '{
    "leave_id": 1,
    "decision": "approved"
  }'
```

## Database Schema Improvements

The schema includes several enhancements:

- Foreign key constraints with CASCADE delete
- Proper indexes for performance optimization
- Check constraints for data validation
- Unique constraints to prevent duplicates
- Default values and NOT NULL constraints
- Automatic timestamp tracking

## Security Features

- Password hashing using bcrypt
- JWT token-based authentication
- Email validation
- SQL injection prevention through ORM
- Input validation using Pydantic

## Project Structure

```md
EmployeeLeaveManagement/
├── main.py                 # FastAPI application entry point
├── models.py              # SQLAlchemy models
├── schemas.py             # Pydantic schemas
├── database.py            # Database configuration
├── auth.py                # Authentication utilities
├── crud.py                # Database operations
├── init_db.py             # Database initialization script
├── schema.sql             # PostgreSQL schema
├── pyproject.toml         # Project dependencies
├── .env.example           # Environment variables template
├── README.md              # This file
└── routers/               # API route handlers
    ├── __init__.py
    ├── auth.py
    ├── admins.py
    ├── employees.py
    ├── managers.py
    ├── leaves.py
    ├── approvals.py
    ├── leave_types.py
    ├── leave_balances.py
    └── audit_logs.py
```

## Default Credentials (After running init_db.py)

- **Admin**: <admin@example.com> / admin123
- **Manager**: <manager@example.com> / manager123
- **Employee**: <employee@example.com> / employee123

**Change these credentials in production!**

## Contributing

1.Fork the repository
2.Create a feature branch
3.Commit your changes
4.Push to the branch
5.Create a Pull Request

## License

MIT License

## Support

For issues and questions, please open an issue on GitHub.
