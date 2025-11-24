from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from schemas import LeaveBalanceCreate, LeaveBalanceResponse, LeaveBalanceUpdate
import crud

router = APIRouter(prefix="/leave-balances", tags=["Leave Balances"])


@router.post("/", response_model=LeaveBalanceResponse, status_code=status.HTTP_201_CREATED)
def create_leave_balance(balance: LeaveBalanceCreate, db: Session = Depends(get_db)):
    """Create a new leave balance for an employee"""
    # Verify employee exists
    employee = crud.get_employee_by_id(db, balance.employee_id)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    
    # Verify leave type exists
    leave_type = crud.get_leave_type_by_id(db, balance.type_id)
    if not leave_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Leave type not found"
        )
    
    new_balance = crud.create_leave_balance(
        db,
        employee_id=balance.employee_id,
        type_id=balance.type_id,
        total_allocated=balance.total_allocated
    )
    
    # Create audit log
    crud.create_audit_log(
        db,
        actor_type="admin",
        actor_id=1,  # This should come from authenticated admin
        action="Created leave balance",
        target_table="leave_balance",
        target_id=new_balance.id
    )
    
    return new_balance


@router.get("/employee/{employee_id}", response_model=List[LeaveBalanceResponse])
def get_employee_leave_balances(employee_id: int, db: Session = Depends(get_db)):
    """Get all leave balances for a specific employee"""
    balances = crud.get_leave_balances_by_employee(db, employee_id)
    return balances


@router.get("/{balance_id}", response_model=LeaveBalanceResponse)
def get_leave_balance(balance_id: int, db: Session = Depends(get_db)):
    """Get leave balance by ID"""
    balance = crud.get_leave_balance_by_id(db, balance_id)
    if not balance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Leave balance not found"
        )
    return balance
