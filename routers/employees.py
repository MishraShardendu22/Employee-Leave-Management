from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from schemas import EmployeeCreate, EmployeeUpdate, EmployeeResponse
import crud

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.post("/", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    """Create a new employee"""
    # Check if employee already exists
    existing_employee = crud.get_employee_by_email(db, employee.email)
    if existing_employee:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee with this email already exists"
        )
    
    new_employee = crud.create_employee(db, employee.name, employee.email, employee.password)
    
    # Create audit log
    crud.create_audit_log(
        db,
        actor_type="employee",
        actor_id=new_employee.id,
        action="Created employee account",
        target_table="employees",
        target_id=new_employee.id
    )
    
    return new_employee


@router.get("/", response_model=List[EmployeeResponse])
def get_all_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all employees"""
    employees = crud.get_all_employees(db, skip=skip, limit=limit)
    return employees


@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    """Get employee by ID"""
    employee = crud.get_employee_by_id(db, employee_id)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    return employee


@router.put("/{employee_id}", response_model=EmployeeResponse)
def update_employee(employee_id: int, employee_data: EmployeeUpdate, db: Session = Depends(get_db)):
    """Update employee information"""
    employee = crud.update_employee(db, employee_id, employee_data.name, employee_data.email)
    
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    
    # Create audit log
    crud.create_audit_log(
        db,
        actor_type="employee",
        actor_id=employee_id,
        action="Updated employee information",
        target_table="employees",
        target_id=employee_id
    )
    
    return employee


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    """Delete employee"""
    success = crud.delete_employee(db, employee_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    
    # Create audit log
    crud.create_audit_log(
        db,
        actor_type="admin",
        actor_id=1,  # This should come from authenticated admin
        action="Deleted employee",
        target_table="employees",
        target_id=employee_id
    )
    
    return None
