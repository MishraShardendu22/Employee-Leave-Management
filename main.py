from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from database import init_db
from routers import (
    auth, admins, employees, managers, 
    leaves, approvals, leave_types, 
    leave_balances, audit_logs
)

app = FastAPI(
    title="Employee Leave Management System",
    description="A comprehensive API for managing employee leave requests, approvals, and balances",
    version="1.0.0"
)

# CORS configuration
origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3001",
]

# Add environment variable for additional origins
env_origins = os.getenv("CORS_ORIGINS", "")
if env_origins and env_origins != "*":
    origins.extend([origin.strip() for origin in env_origins.split(",")])

print(f"Allowed CORS origins: {origins}")

# CORS middleware - must be added before routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

# Include routers
app.include_router(auth.router)
app.include_router(admins.router)
app.include_router(employees.router)
app.include_router(managers.router)
app.include_router(leaves.router)
app.include_router(approvals.router)
app.include_router(leave_types.router)
app.include_router(leave_balances.router)
app.include_router(audit_logs.router)


@app.get("/")
def root():
    return {
        "message": "Employee Leave Management API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.on_event("startup")
def startup_event():
    """Initialize database on startup"""
    print("Initializing database...")
    init_db()
    print("Database initialized successfully!")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
