from sqlalchemy.orm import Session
from typing import Optional, List
from models import (
    Admin, Employee, Manager, LeaveType, Leave, 
    Approval, LeaveBalance, AuditLog
)
from auth import get_password_hash
from datetime import datetime


# ============== Admin CRUD ==============
def create_admin(db: Session, name: str, email: str, password: str) -> Admin:
    hashed_password = get_password_hash(password)
    admin = Admin(name=name, email=email, password_hash=hashed_password)
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin


def get_admin_by_email(db: Session, email: str) -> Optional[Admin]:
    return db.query(Admin).filter(Admin.email == email).first()


def get_admin_by_id(db: Session, admin_id: int) -> Optional[Admin]:
    return db.query(Admin).filter(Admin.id == admin_id).first()


def get_all_admins(db: Session, skip: int = 0, limit: int = 100) -> List[Admin]:
    return db.query(Admin).offset(skip).limit(limit).all()


# ============== Employee CRUD ==============
def create_employee(db: Session, name: str, email: str, password: str) -> Employee:
    hashed_password = get_password_hash(password)
    employee = Employee(name=name, email=email, password_hash=hashed_password)
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


def get_employee_by_email(db: Session, email: str) -> Optional[Employee]:
    return db.query(Employee).filter(Employee.email == email).first()


def get_employee_by_id(db: Session, employee_id: int) -> Optional[Employee]:
    return db.query(Employee).filter(Employee.id == employee_id).first()


def get_all_employees(db: Session, skip: int = 0, limit: int = 100) -> List[Employee]:
    return db.query(Employee).offset(skip).limit(limit).all()


def update_employee(db: Session, employee_id: int, name: Optional[str] = None, email: Optional[str] = None) -> Optional[Employee]:
    employee = get_employee_by_id(db, employee_id)
    if not employee:
        return None
    
    if name:
        employee.name = name
    if email:
        employee.email = email
    
    db.commit()
    db.refresh(employee)
    return employee


def delete_employee(db: Session, employee_id: int) -> bool:
    employee = get_employee_by_id(db, employee_id)
    if not employee:
        return False
    
    db.delete(employee)
    db.commit()
    return True


# ============== Manager CRUD ==============
def create_manager(db: Session, name: str, email: str, password: str) -> Manager:
    hashed_password = get_password_hash(password)
    manager = Manager(name=name, email=email, password_hash=hashed_password)
    db.add(manager)
    db.commit()
    db.refresh(manager)
    return manager


def get_manager_by_email(db: Session, email: str) -> Optional[Manager]:
    return db.query(Manager).filter(Manager.email == email).first()


def get_manager_by_id(db: Session, manager_id: int) -> Optional[Manager]:
    return db.query(Manager).filter(Manager.id == manager_id).first()


def get_all_managers(db: Session, skip: int = 0, limit: int = 100) -> List[Manager]:
    return db.query(Manager).offset(skip).limit(limit).all()


def delete_manager(db: Session, manager_id: int) -> bool:
    manager = get_manager_by_id(db, manager_id)
    if not manager:
        return False
    
    db.delete(manager)
    db.commit()
    return True


# ============== Leave Type CRUD ==============
def create_leave_type(db: Session, name: str) -> LeaveType:
    leave_type = LeaveType(name=name)
    db.add(leave_type)
    db.commit()
    db.refresh(leave_type)
    return leave_type


def get_leave_type_by_id(db: Session, type_id: int) -> Optional[LeaveType]:
    return db.query(LeaveType).filter(LeaveType.id == type_id).first()


def get_all_leave_types(db: Session) -> List[LeaveType]:
    return db.query(LeaveType).all()


def delete_leave_type(db: Session, type_id: int) -> bool:
    leave_type = get_leave_type_by_id(db, type_id)
    if not leave_type:
        return False
    
    db.delete(leave_type)
    db.commit()
    return True


# ============== Leave CRUD ==============
def create_leave(
    db: Session, 
    employee_id: int, 
    type_id: int, 
    start_time: datetime, 
    end_time: datetime, 
    reason: Optional[str] = None
) -> Leave:
    leave = Leave(
        employee_id=employee_id,
        type_id=type_id,
        start_time=start_time,
        end_time=end_time,
        reason=reason,
        status="pending"
    )
    db.add(leave)
    db.commit()
    db.refresh(leave)
    return leave


def get_leave_by_id(db: Session, leave_id: int) -> Optional[Leave]:
    return db.query(Leave).filter(Leave.id == leave_id).first()


def get_leaves_by_employee(db: Session, employee_id: int, skip: int = 0, limit: int = 100) -> List[Leave]:
    return db.query(Leave).filter(Leave.employee_id == employee_id).offset(skip).limit(limit).all()


def get_all_leaves(db: Session, skip: int = 0, limit: int = 100) -> List[Leave]:
    return db.query(Leave).offset(skip).limit(limit).all()


def get_pending_leaves(db: Session, skip: int = 0, limit: int = 100) -> List[Leave]:
    return db.query(Leave).filter(Leave.status == "pending").offset(skip).limit(limit).all()


def update_leave_status(db: Session, leave_id: int, status: str) -> Optional[Leave]:
    leave = get_leave_by_id(db, leave_id)
    if not leave:
        return None
    
    leave.status = status
    db.commit()
    db.refresh(leave)
    return leave


def delete_leave(db: Session, leave_id: int) -> bool:
    leave = get_leave_by_id(db, leave_id)
    if not leave:
        return False
    
    db.delete(leave)
    db.commit()
    return True


# ============== Approval CRUD ==============
def create_approval(db: Session, leave_id: int, manager_id: int, decision: str) -> Approval:
    approval = Approval(
        leave_id=leave_id,
        approved_by=manager_id,
        decision=decision
    )
    db.add(approval)
    
    # Update leave status
    update_leave_status(db, leave_id, decision)
    
    db.commit()
    db.refresh(approval)
    return approval


def get_approval_by_leave_id(db: Session, leave_id: int) -> Optional[Approval]:
    return db.query(Approval).filter(Approval.leave_id == leave_id).first()


def get_approvals_by_manager(db: Session, manager_id: int, skip: int = 0, limit: int = 100) -> List[Approval]:
    return db.query(Approval).filter(Approval.approved_by == manager_id).offset(skip).limit(limit).all()


# ============== Leave Balance CRUD ==============
def create_leave_balance(
    db: Session, 
    employee_id: int, 
    type_id: int, 
    total_allocated: int
) -> LeaveBalance:
    leave_balance = LeaveBalance(
        employee_id=employee_id,
        type_id=type_id,
        total_allocated=total_allocated,
        total_used=0,
        remaining=total_allocated
    )
    db.add(leave_balance)
    db.commit()
    db.refresh(leave_balance)
    return leave_balance


def get_leave_balance_by_id(db: Session, balance_id: int) -> Optional[LeaveBalance]:
    return db.query(LeaveBalance).filter(LeaveBalance.id == balance_id).first()


def get_leave_balances_by_employee(db: Session, employee_id: int) -> List[LeaveBalance]:
    return db.query(LeaveBalance).filter(LeaveBalance.employee_id == employee_id).all()


def update_leave_balance(
    db: Session, 
    employee_id: int, 
    type_id: int, 
    days_used: int
) -> Optional[LeaveBalance]:
    leave_balance = db.query(LeaveBalance).filter(
        LeaveBalance.employee_id == employee_id,
        LeaveBalance.type_id == type_id
    ).first()
    
    if not leave_balance:
        return None
    
    leave_balance.total_used += days_used
    leave_balance.remaining = leave_balance.total_allocated - leave_balance.total_used
    
    db.commit()
    db.refresh(leave_balance)
    return leave_balance


# ============== Audit Log CRUD ==============
def create_audit_log(
    db: Session,
    actor_type: str,
    actor_id: int,
    action: str,
    target_table: str,
    target_id: int
) -> AuditLog:
    audit_log = AuditLog(
        actor_type=actor_type,
        actor_id=actor_id,
        action=action,
        target_table=target_table,
        target_id=target_id
    )
    db.add(audit_log)
    db.commit()
    db.refresh(audit_log)
    return audit_log


def get_audit_logs(db: Session, skip: int = 0, limit: int = 100) -> List[AuditLog]:
    return db.query(AuditLog).order_by(AuditLog.timestamp.desc()).offset(skip).limit(limit).all()


def get_audit_logs_by_actor(db: Session, actor_type: str, actor_id: int, skip: int = 0, limit: int = 100) -> List[AuditLog]:
    return db.query(AuditLog).filter(
        AuditLog.actor_type == actor_type,
        AuditLog.actor_id == actor_id
    ).order_by(AuditLog.timestamp.desc()).offset(skip).limit(limit).all()
