from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

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

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
