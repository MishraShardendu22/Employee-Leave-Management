from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from schemas import LeaveTypeCreate, LeaveTypeResponse
import crud

router = APIRouter(prefix="/leave-types", tags=["Leave Types"])


@router.post("/", response_model=LeaveTypeResponse, status_code=status.HTTP_201_CREATED)
def create_leave_type(leave_type: LeaveTypeCreate, db: Session = Depends(get_db)):
    """Create a new leave type"""
    # Validate that name is not only numbers
    if leave_type.name.isdigit():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Leave type name cannot be only numbers"
        )
    
    new_leave_type = crud.create_leave_type(db, leave_type.name)
    
    # Create audit log
    crud.create_audit_log(
        db,
        actor_type="admin",
        actor_id=1,  # This should come from authenticated admin
        action="Created leave type",
        target_table="leave_types",
        target_id=new_leave_type.id
    )
    
    return new_leave_type


@router.get("/", response_model=List[LeaveTypeResponse])
def get_all_leave_types(db: Session = Depends(get_db)):
    """Get all leave types"""
    leave_types = crud.get_all_leave_types(db)
    return leave_types


@router.get("/{type_id}", response_model=LeaveTypeResponse)
def get_leave_type(type_id: int, db: Session = Depends(get_db)):
    """Get leave type by ID"""
    leave_type = crud.get_leave_type_by_id(db, type_id)
    if not leave_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Leave type not found"
        )
    return leave_type


@router.delete("/{type_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_leave_type(type_id: int, db: Session = Depends(get_db)):
    """Delete a leave type"""
    leave_type = crud.get_leave_type_by_id(db, type_id)
    if not leave_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Leave type not found"
        )
    
    success = crud.delete_leave_type(db, type_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to delete leave type"
        )
    
    # Create audit log
    crud.create_audit_log(
        db,
        actor_type="admin",
        actor_id=1,  # This should come from authenticated admin
        action="Deleted leave type",
        target_table="leave_types",
        target_id=type_id
    )
    
    return None
