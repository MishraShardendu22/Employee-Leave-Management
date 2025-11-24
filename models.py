from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Text, func
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
import enum

Base = declarative_base()

class LeaveStatus(enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

class Decision(enum.Enum):
    approved = "approved"
    rejected = "rejected"

class ActorType(enum.Enum):
    admin = "admin"
    manager = "manager"
    employee = "employee"


class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)


class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    leaves = relationship("Leave", back_populates="employee", cascade="all, delete-orphan")
    leave_balances = relationship("LeaveBalance", back_populates="employee", cascade="all, delete-orphan")


class Manager(Base):
    __tablename__ = "managers"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    
    approvals = relationship("Approval", back_populates="manager", cascade="all, delete-orphan")


class LeaveType(Base):
    __tablename__ = "leave_types"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    
    leaves = relationship("Leave", back_populates="leave_type")
    leave_balances = relationship("LeaveBalance", back_populates="leave_type")


class Leave(Base):
    __tablename__ = "leaves"
    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    type_id = Column(Integer, ForeignKey("leave_types.id", ondelete="CASCADE"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    reason = Column(Text)
    status = Column(String(20), default="pending", nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    
    employee = relationship("Employee", back_populates="leaves")
    leave_type = relationship("LeaveType", back_populates="leaves")
    approvals = relationship("Approval", back_populates="leave", cascade="all, delete-orphan")


class Approval(Base):
    __tablename__ = "approvals"
    id = Column(Integer, primary_key=True, autoincrement=True)
    leave_id = Column(Integer, ForeignKey("leaves.id", ondelete="CASCADE"), nullable=False)
    approved_by = Column(Integer, ForeignKey("managers.id", ondelete="CASCADE"), nullable=False)
    approved_at = Column(DateTime, default=func.now(), nullable=False)
    decision = Column(String(20), nullable=False)
    
    leave = relationship("Leave", back_populates="approvals")
    manager = relationship("Manager", back_populates="approvals")


class LeaveBalance(Base):
    __tablename__ = "leave_balance"
    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    type_id = Column(Integer, ForeignKey("leave_types.id", ondelete="CASCADE"), nullable=False)
    total_allocated = Column(Integer, nullable=False, default=0)
    total_used = Column(Integer, nullable=False, default=0)
    remaining = Column(Integer, nullable=False, default=0)
    
    employee = relationship("Employee", back_populates="leave_balances")
    leave_type = relationship("LeaveType", back_populates="leave_balances")


class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    actor_type = Column(String(20), nullable=False)
    actor_id = Column(Integer, nullable=False)
    action = Column(Text, nullable=False)
    target_table = Column(String(50), nullable=False)
    target_id = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=func.now(), nullable=False)
