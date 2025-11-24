from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from schemas import ApprovalCreate, ApprovalResponse
import crud

router = APIRouter(prefix="/approvals", tags=["Approvals"])


@router.post("/", response_model=ApprovalResponse, status_code=status.HTTP_201_CREATED)
def create_approval(approval: ApprovalCreate, manager_id: int, db: Session = Depends(get_db)):
    """Create an approval decision for a leave request"""
    # Verify manager exists
    manager = crud.get_manager_by_id(db, manager_id)
    if not manager:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Manager not found"
        )
    
    # Verify leave exists
    leave = crud.get_leave_by_id(db, approval.leave_id)
    if not leave:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Leave request not found"
        )
    
    # Check if leave is still pending
    if leave.status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Leave request has already been processed"
        )
    
    # Validate decision
    if approval.decision not in ["approved", "rejected"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Decision must be 'approved' or 'rejected'"
        )
    
    # Create approval
    new_approval = crud.create_approval(
        db,
        leave_id=approval.leave_id,
        manager_id=manager_id,
        decision=approval.decision
    )
    
    # If approved, update leave balance
    if approval.decision == "approved":
        days = (leave.end_time - leave.start_time).days + 1
        crud.update_leave_balance(db, leave.employee_id, leave.type_id, days)
    
    # Create audit log
    crud.create_audit_log(
        db,
        actor_type="manager",
        actor_id=manager_id,
        action=f"{approval.decision.capitalize()} leave request",
        target_table="approvals",
        target_id=new_approval.id
    )
    
    return new_approval


@router.get("/manager/{manager_id}", response_model=List[ApprovalResponse])
def get_manager_approvals(manager_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all approvals made by a specific manager"""
    approvals = crud.get_approvals_by_manager(db, manager_id, skip=skip, limit=limit)
    return approvals


@router.get("/leave/{leave_id}", response_model=ApprovalResponse)
def get_leave_approval(leave_id: int, db: Session = Depends(get_db)):
    """Get approval for a specific leave request"""
    approval = crud.get_approval_by_leave_id(db, leave_id)
    if not approval:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No approval found for this leave request"
        )
    return approval
