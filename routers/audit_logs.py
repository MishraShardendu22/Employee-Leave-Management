from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from schemas import AuditLogResponse
import crud

router = APIRouter(prefix="/audit-logs", tags=["Audit Logs"])


@router.get("/", response_model=List[AuditLogResponse])
def get_all_audit_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all audit logs"""
    logs = crud.get_audit_logs(db, skip=skip, limit=limit)
    return logs


@router.get("/actor/{actor_type}/{actor_id}", response_model=List[AuditLogResponse])
def get_audit_logs_by_actor(
    actor_type: str, 
    actor_id: int, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """Get audit logs for a specific actor"""
    if actor_type not in ["admin", "manager", "employee"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid actor type. Must be 'admin', 'manager', or 'employee'"
        )
    
    logs = crud.get_audit_logs_by_actor(db, actor_type, actor_id, skip=skip, limit=limit)
    return logs
