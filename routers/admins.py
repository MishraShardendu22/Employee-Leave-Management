from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import os

from database import get_db
from schemas import AdminCreate, AdminResponse
import crud

router = APIRouter(prefix="/admins", tags=["Admins"])


@router.post("/", response_model=AdminResponse, status_code=status.HTTP_201_CREATED)
def create_admin(admin: AdminCreate, db: Session = Depends(get_db)):
    """Admin creation is disabled - only one admin exists using environment credentials"""
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Admin creation is disabled. Only one admin account exists."
    )


@router.get("/me", response_model=dict)
def get_admin_info():
    """Get current admin info from environment"""
    admin_email = os.getenv("EMAIL", "").strip('"')
    return {
        "id": 1,
        "email": admin_email,
        "name": "System Admin"
    }
