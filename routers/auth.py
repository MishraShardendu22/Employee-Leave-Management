from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from schemas import LoginRequest, Token, AdminCreate, AdminResponse
from auth import verify_password, create_access_token
import crud

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login/admin", response_model=Token)
def login_admin(login_data: LoginRequest, db: Session = Depends(get_db)):
    """Admin login endpoint"""
    admin = crud.get_admin_by_email(db, login_data.email)
    
    if not admin or not verify_password(login_data.password, admin.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    access_token = create_access_token(
        data={"sub": admin.email, "user_type": "admin", "user_id": admin.id}
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login/employee", response_model=Token)
def login_employee(login_data: LoginRequest, db: Session = Depends(get_db)):
    """Employee login endpoint"""
    employee = crud.get_employee_by_email(db, login_data.email)
    
    if not employee or not verify_password(login_data.password, employee.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    access_token = create_access_token(
        data={"sub": employee.email, "user_type": "employee", "user_id": employee.id}
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login/manager", response_model=Token)
def login_manager(login_data: LoginRequest, db: Session = Depends(get_db)):
    """Manager login endpoint"""
    manager = crud.get_manager_by_email(db, login_data.email)
    
    if not manager or not verify_password(login_data.password, manager.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    access_token = create_access_token(
        data={"sub": manager.email, "user_type": "manager", "user_id": manager.id}
    )
    
    return {"access_token": access_token, "token_type": "bearer"}
