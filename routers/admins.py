from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from schemas import AdminCreate, AdminResponse
import crud

router = APIRouter(prefix="/admins", tags=["Admins"])


@router.post("/", response_model=AdminResponse, status_code=status.HTTP_201_CREATED)
def create_admin(admin: AdminCreate, db: Session = Depends(get_db)):
    """Create a new admin"""
    # Check if admin already exists
    existing_admin = crud.get_admin_by_email(db, admin.email)
    if existing_admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admin with this email already exists"
        )
    
    new_admin = crud.create_admin(db, admin.name, admin.email, admin.password)
    
    # Create audit log
    crud.create_audit_log(
        db,
        actor_type="admin",
        actor_id=new_admin.id,
        action="Created admin account",
        target_table="admins",
        target_id=new_admin.id
    )
    
    return new_admin


@router.get("/", response_model=List[AdminResponse])
def get_all_admins(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all admins"""
    admins = crud.get_all_admins(db, skip=skip, limit=limit)
    return admins


@router.get("/{admin_id}", response_model=AdminResponse)
def get_admin(admin_id: int, db: Session = Depends(get_db)):
    """Get admin by ID"""
    admin = crud.get_admin_by_id(db, admin_id)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Admin not found"
        )
    return admin
