from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from schemas import LeaveCreate, LeaveResponse, LeaveUpdate
import crud

router = APIRouter(prefix="/leaves", tags=["Leaves"])


@router.post("/", response_model=LeaveResponse, status_code=status.HTTP_201_CREATED)
def create_leave(leave: LeaveCreate, employee_id: int, db: Session = Depends(get_db)):
    """Create a new leave request"""
    # Verify employee exists
    employee = crud.get_employee_by_id(db, employee_id)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    
    # Verify leave type exists
    leave_type = crud.get_leave_type_by_id(db, leave.type_id)
    if not leave_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Leave type not found"
        )
    
    # Validate dates
    if leave.start_time >= leave.end_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Start time must be before end time"
        )
    
    new_leave = crud.create_leave(
        db,
        employee_id=employee_id,
        type_id=leave.type_id,
        start_time=leave.start_time,
        end_time=leave.end_time,
        reason=leave.reason
    )
    
    # Create audit log
    crud.create_audit_log(
        db,
        actor_type="employee",
        actor_id=employee_id,
        action="Created leave request",
        target_table="leaves",
        target_id=new_leave.id
    )
    
    return new_leave


@router.get("/", response_model=List[LeaveResponse])
def get_all_leaves(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all leave requests"""
    leaves = crud.get_all_leaves(db, skip=skip, limit=limit)
    return leaves


@router.get("/pending", response_model=List[LeaveResponse])
def get_pending_leaves(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all pending leave requests"""
    leaves = crud.get_pending_leaves(db, skip=skip, limit=limit)
    return leaves


@router.get("/employee/{employee_id}", response_model=List[LeaveResponse])
def get_employee_leaves(employee_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all leaves for a specific employee"""
    leaves = crud.get_leaves_by_employee(db, employee_id, skip=skip, limit=limit)
    return leaves


@router.get("/{leave_id}", response_model=LeaveResponse)
def get_leave(leave_id: int, db: Session = Depends(get_db)):
    """Get leave by ID"""
    leave = crud.get_leave_by_id(db, leave_id)
    if not leave:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Leave not found"
        )
    return leave


@router.delete("/{leave_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_leave(leave_id: int, db: Session = Depends(get_db)):
    """Delete a leave request"""
    leave = crud.get_leave_by_id(db, leave_id)
    if not leave:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Leave not found"
        )
    
    # Only allow deletion of pending leaves
    if leave.status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete non-pending leave requests"
        )
    
    crud.delete_leave(db, leave_id)
    
    # Create audit log
    crud.create_audit_log(
        db,
        actor_type="employee",
        actor_id=leave.employee_id,
        action="Deleted leave request",
        target_table="leaves",
        target_id=leave_id
    )
    
    return None
