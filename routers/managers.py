from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from schemas import ManagerCreate, ManagerResponse
import crud

router = APIRouter(prefix="/managers", tags=["Managers"])


@router.post("/", response_model=ManagerResponse, status_code=status.HTTP_201_CREATED)
def create_manager(manager: ManagerCreate, db: Session = Depends(get_db)):
    """Create a new manager"""
    # Check if manager already exists
    existing_manager = crud.get_manager_by_email(db, manager.email)
    if existing_manager:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Manager with this email already exists"
        )
    
    new_manager = crud.create_manager(db, manager.name, manager.email, manager.password)
    
    # Create audit log
    crud.create_audit_log(
        db,
        actor_type="manager",
        actor_id=new_manager.id,
        action="Created manager account",
        target_table="managers",
        target_id=new_manager.id
    )
    
    return new_manager


@router.get("/", response_model=List[ManagerResponse])
def get_all_managers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all managers"""
    managers = crud.get_all_managers(db, skip=skip, limit=limit)
    return managers


@router.get("/{manager_id}", response_model=ManagerResponse)
def get_manager(manager_id: int, db: Session = Depends(get_db)):
    """Get manager by ID"""
    manager = crud.get_manager_by_id(db, manager_id)
    if not manager:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Manager not found"
        )
    return manager
