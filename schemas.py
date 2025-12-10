from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


# ============== Auth Schemas ==============
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
    user_type: Optional[str] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# ============== Admin Schemas ==============
class AdminBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr


class AdminCreate(AdminBase):
    password: str = Field(..., min_length=6)


class AdminResponse(AdminBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ============== Employee Schemas ==============
class EmployeeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr


class EmployeeCreate(EmployeeBase):
    password: str = Field(..., min_length=6)


class EmployeeUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None


class EmployeeResponse(EmployeeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============== Manager Schemas ==============
class ManagerBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr


class ManagerCreate(ManagerBase):
    password: str = Field(..., min_length=6)


class ManagerResponse(ManagerBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ============== Leave Type Schemas ==============
class LeaveTypeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)


class LeaveTypeCreate(LeaveTypeBase):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_name
    
    @classmethod
    def validate_name(cls, v):
        if isinstance(v, dict) and 'name' in v:
            name = v['name']
            if name.isdigit():
                raise ValueError('Leave type name cannot be only numbers')
        return v


class LeaveTypeResponse(LeaveTypeBase):
    id: int

    class Config:
        from_attributes = True


# ============== Leave Schemas ==============
class LeaveBase(BaseModel):
    type_id: int
    start_time: datetime
    end_time: datetime
    reason: Optional[str] = None


class LeaveCreate(LeaveBase):
    pass


class LeaveUpdate(BaseModel):
    type_id: Optional[int] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    reason: Optional[str] = None


class LeaveResponse(LeaveBase):
    id: int
    employee_id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


# ============== Approval Schemas ==============
class ApprovalCreate(BaseModel):
    leave_id: int
    decision: str = Field(..., pattern="^(approved|rejected)$")


class ApprovalResponse(BaseModel):
    id: int
    leave_id: int
    approved_by: int
    approved_at: datetime
    decision: str

    class Config:
        from_attributes = True


# ============== Leave Balance Schemas ==============
class LeaveBalanceBase(BaseModel):
    employee_id: int
    type_id: int
    total_allocated: int = Field(..., ge=0)
    total_used: int = Field(default=0, ge=0)
    remaining: int = Field(default=0, ge=0)


class LeaveBalanceCreate(LeaveBalanceBase):
    pass


class LeaveBalanceUpdate(BaseModel):
    total_allocated: Optional[int] = Field(None, ge=0)
    total_used: Optional[int] = Field(None, ge=0)
    remaining: Optional[int] = Field(None, ge=0)


class LeaveBalanceResponse(LeaveBalanceBase):
    id: int

    class Config:
        from_attributes = True


# ============== Audit Log Schemas ==============
class AuditLogCreate(BaseModel):
    actor_type: str = Field(..., pattern="^(admin|manager|employee)$")
    actor_id: int
    action: str
    target_table: str
    target_id: int


class AuditLogResponse(AuditLogCreate):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True
