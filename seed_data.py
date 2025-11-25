"""
Seed Data Generator for Employee Leave Management System
Generates professional dummy data for testing and development purposes.
"""

import bcrypt
from datetime import datetime, timedelta
import random
from database import SessionLocal, engine
from models import (
    Base, Admin, Employee, Manager, LeaveType, 
    Leave, Approval, LeaveBalance, AuditLog
)

# Password hashing function
def get_password_hash(password: str) -> str:
    """Hash a password"""
    password_bytes = password.encode('utf-8')[:72]
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode('utf-8')

# Default password for all dummy users (for testing)
DEFAULT_PASSWORD = "Password@123"

# =============================================================================
# PROFESSIONAL DUMMY DATA
# =============================================================================

# Admin Data
ADMINS_DATA = [
    {"name": "Rajesh Kumar", "email": "rajesh.kumar@elmcorp.com"},
    {"name": "Priya Sharma", "email": "priya.sharma@elmcorp.com"},
    {"name": "Amit Verma", "email": "amit.verma@elmcorp.com"},
    {"name": "Sunita Patel", "email": "sunita.patel@elmcorp.com"},
    {"name": "Vikram Singh", "email": "vikram.singh@elmcorp.com"},
]

# Manager Data
MANAGERS_DATA = [
    {"name": "Ananya Desai", "email": "ananya.desai@elmcorp.com"},
    {"name": "Rahul Mehta", "email": "rahul.mehta@elmcorp.com"},
    {"name": "Neha Gupta", "email": "neha.gupta@elmcorp.com"},
    {"name": "Sanjay Reddy", "email": "sanjay.reddy@elmcorp.com"},
    {"name": "Kavita Nair", "email": "kavita.nair@elmcorp.com"},
    {"name": "Arjun Malhotra", "email": "arjun.malhotra@elmcorp.com"},
    {"name": "Deepika Joshi", "email": "deepika.joshi@elmcorp.com"},
    {"name": "Manish Agarwal", "email": "manish.agarwal@elmcorp.com"},
    {"name": "Pooja Iyer", "email": "pooja.iyer@elmcorp.com"},
    {"name": "Rohit Kapoor", "email": "rohit.kapoor@elmcorp.com"},
]

# Employee Data - 50 Professional Employees
EMPLOYEES_DATA = [
    # Engineering Department
    {"name": "Vanshiki Singh", "email": "vanshiki.singh@elmcorp.com"},
    {"name": "Aarav Patel", "email": "aarav.patel@elmcorp.com"},
    {"name": "Diya Sharma", "email": "diya.sharma@elmcorp.com"},
    {"name": "Ishaan Gupta", "email": "ishaan.gupta@elmcorp.com"},
    {"name": "Aisha Khan", "email": "aisha.khan@elmcorp.com"},
    {"name": "Rohan Verma", "email": "rohan.verma@elmcorp.com"},
    {"name": "Anvi Reddy", "email": "anvi.reddy@elmcorp.com"},
    {"name": "Vihaan Nair", "email": "vihaan.nair@elmcorp.com"},
    {"name": "Saanvi Joshi", "email": "saanvi.joshi@elmcorp.com"},
    {"name": "Aryan Malhotra", "email": "aryan.malhotra@elmcorp.com"},
    
    # Product Team
    {"name": "Kiara Kapoor", "email": "kiara.kapoor@elmcorp.com"},
    {"name": "Reyansh Agarwal", "email": "reyansh.agarwal@elmcorp.com"},
    {"name": "Myra Iyer", "email": "myra.iyer@elmcorp.com"},
    {"name": "Kabir Desai", "email": "kabir.desai@elmcorp.com"},
    {"name": "Anaya Mehta", "email": "anaya.mehta@elmcorp.com"},
    {"name": "Vivaan Choudhury", "email": "vivaan.choudhury@elmcorp.com"},
    {"name": "Pari Saxena", "email": "pari.saxena@elmcorp.com"},
    {"name": "Aditya Bose", "email": "aditya.bose@elmcorp.com"},
    {"name": "Avni Mukherjee", "email": "avni.mukherjee@elmcorp.com"},
    {"name": "Dhruv Chatterjee", "email": "dhruv.chatterjee@elmcorp.com"},
    
    # Finance Team
    {"name": "Zara Banerjee", "email": "zara.banerjee@elmcorp.com"},
    {"name": "Krishna Das", "email": "krishna.das@elmcorp.com"},
    {"name": "Tara Ghosh", "email": "tara.ghosh@elmcorp.com"},
    {"name": "Advait Sen", "email": "advait.sen@elmcorp.com"},
    {"name": "Ira Roy", "email": "ira.roy@elmcorp.com"},
    {"name": "Arnav Dutta", "email": "arnav.dutta@elmcorp.com"},
    {"name": "Nisha Pal", "email": "nisha.pal@elmcorp.com"},
    {"name": "Yash Mondal", "email": "yash.mondal@elmcorp.com"},
    {"name": "Riya Bhattacharya", "email": "riya.bhattacharya@elmcorp.com"},
    {"name": "Shaurya Saha", "email": "shaurya.saha@elmcorp.com"},
    
    # HR Team
    {"name": "Amaira Singh", "email": "amaira.singh@elmcorp.com"},
    {"name": "Veer Thakur", "email": "veer.thakur@elmcorp.com"},
    {"name": "Naina Yadav", "email": "naina.yadav@elmcorp.com"},
    {"name": "Rehan Chauhan", "email": "rehan.chauhan@elmcorp.com"},
    {"name": "Aditi Rawat", "email": "aditi.rawat@elmcorp.com"},
    {"name": "Pranav Bisht", "email": "pranav.bisht@elmcorp.com"},
    {"name": "Ishita Negi", "email": "ishita.negi@elmcorp.com"},
    {"name": "Siddharth Jain", "email": "siddharth.jain@elmcorp.com"},
    {"name": "Kavya Goyal", "email": "kavya.goyal@elmcorp.com"},
    {"name": "Atharv Mittal", "email": "atharv.mittal@elmcorp.com"},
    
    # Marketing Team
    {"name": "Shreya Singhal", "email": "shreya.singhal@elmcorp.com"},
    {"name": "Laksh Garg", "email": "laksh.garg@elmcorp.com"},
    {"name": "Navya Khurana", "email": "navya.khurana@elmcorp.com"},
    {"name": "Om Bajaj", "email": "om.bajaj@elmcorp.com"},
    {"name": "Anika Tandon", "email": "anika.tandon@elmcorp.com"},
    {"name": "Rudra Bhatia", "email": "rudra.bhatia@elmcorp.com"},
    {"name": "Siya Kohli", "email": "siya.kohli@elmcorp.com"},
    {"name": "Ayaan Sethi", "email": "ayaan.sethi@elmcorp.com"},
    {"name": "Pihu Khanna", "email": "pihu.khanna@elmcorp.com"},
    {"name": "Neil Arora", "email": "neil.arora@elmcorp.com"},
]

# Leave Reasons - Professional and Realistic
SICK_LEAVE_REASONS = [
    "Suffering from seasonal flu and fever",
    "Severe migraine, need rest",
    "Food poisoning, unable to work",
    "Dental surgery scheduled",
    "Eye infection, doctor advised rest",
    "Back pain flare-up, physiotherapy needed",
    "Stomach infection, medical leave advised",
    "High fever with body ache",
    "Viral infection, need complete rest",
    "Scheduled health checkup and tests",
]

CASUAL_LEAVE_REASONS = [
    "Personal work at bank",
    "Family function to attend",
    "Home repairs and maintenance",
    "Passport/document work",
    "Visiting relatives",
    "Personal errands",
    "Moving to new apartment",
    "Vehicle registration work",
    "Property documentation",
    "Personal appointment",
]

ANNUAL_LEAVE_REASONS = [
    "Family vacation to Goa",
    "Planned trip to Himachal",
    "Visiting hometown for Diwali",
    "International travel - Singapore",
    "Wedding in family",
    "Beach vacation in Kerala",
    "Hill station trip with family",
    "Annual family gathering",
    "Planned vacation to Rajasthan",
    "Holiday trip to Northeast",
]

MATERNITY_LEAVE_REASONS = [
    "Maternity leave as per company policy",
    "Expected delivery date approaching",
    "Pre-natal care and delivery",
]

PATERNITY_LEAVE_REASONS = [
    "Wife's delivery scheduled",
    "Paternity leave for newborn care",
    "New baby arrival - paternity leave",
]

UNPAID_LEAVE_REASONS = [
    "Extended personal emergency",
    "Family medical emergency abroad",
    "Higher studies examination",
    "Personal project work",
    "Extended travel plans",
]

# Audit Log Actions
AUDIT_ACTIONS = [
    "Created new leave request",
    "Updated leave request status",
    "Approved leave request",
    "Rejected leave request",
    "Modified employee profile",
    "Updated leave balance",
    "Added new employee",
    "Deleted leave request",
    "Changed leave type",
    "System configuration updated",
]


def clear_existing_data(db):
    """Clear existing data from tables (except leave_types)"""
    print("🗑️  Clearing existing data...")
    db.query(AuditLog).delete()
    db.query(Approval).delete()
    db.query(LeaveBalance).delete()
    db.query(Leave).delete()
    db.query(Manager).delete()
    db.query(Employee).delete()
    db.query(Admin).delete()
    db.commit()
    print("✅ Existing data cleared!")


def seed_admins(db):
    """Seed admin users"""
    print("\n👨‍💼 Seeding Admins...")
    admins = []
    password_hash = get_password_hash(DEFAULT_PASSWORD)
    
    for admin_data in ADMINS_DATA:
        admin = Admin(
            name=admin_data["name"],
            email=admin_data["email"],
            password_hash=password_hash,
            created_at=datetime.now() - timedelta(days=random.randint(30, 365))
        )
        admins.append(admin)
    
    db.add_all(admins)
    db.commit()
    print(f"✅ Created {len(admins)} admins")
    return admins


def seed_managers(db):
    """Seed manager users"""
    print("\n👔 Seeding Managers...")
    managers = []
    password_hash = get_password_hash(DEFAULT_PASSWORD)
    
    for manager_data in MANAGERS_DATA:
        manager = Manager(
            name=manager_data["name"],
            email=manager_data["email"],
            password_hash=password_hash,
            created_at=datetime.now() - timedelta(days=random.randint(30, 365))
        )
        managers.append(manager)
    
    db.add_all(managers)
    db.commit()
    print(f"✅ Created {len(managers)} managers")
    return managers


def seed_employees(db):
    """Seed employee users"""
    print("\n👥 Seeding Employees...")
    employees = []
    password_hash = get_password_hash(DEFAULT_PASSWORD)
    
    for emp_data in EMPLOYEES_DATA:
        employee = Employee(
            name=emp_data["name"],
            email=emp_data["email"],
            password_hash=password_hash,
            created_at=datetime.now() - timedelta(days=random.randint(30, 730)),
            updated_at=datetime.now() - timedelta(days=random.randint(0, 30))
        )
        employees.append(employee)
    
    db.add_all(employees)
    db.commit()
    print(f"✅ Created {len(employees)} employees")
    return employees


def seed_leave_balances(db, employees):
    """Seed leave balances for all employees"""
    print("\n📊 Seeding Leave Balances...")
    leave_types = db.query(LeaveType).all()
    leave_balances = []
    
    # Leave allocation config: (type_name, total_allocated)
    LEAVE_ALLOCATION = {
        "Sick Leave": 12,
        "Casual Leave": 10,
        "Annual Leave": 20,
        "Maternity Leave": 180,
        "Paternity Leave": 15,
        "Unpaid Leave": 30,
    }
    
    for employee in employees:
        for leave_type in leave_types:
            allocated = LEAVE_ALLOCATION.get(leave_type.name, 10)
            used = random.randint(0, min(allocated // 2, 5))  # Some random usage
            
            balance = LeaveBalance(
                employee_id=employee.id,
                type_id=leave_type.id,
                total_allocated=allocated,
                total_used=used,
                remaining=allocated - used
            )
            leave_balances.append(balance)
    
    db.add_all(leave_balances)
    db.commit()
    print(f"✅ Created {len(leave_balances)} leave balance records")
    return leave_balances


def seed_leaves(db, employees):
    """Seed leave requests"""
    print("\n📝 Seeding Leave Requests...")
    leave_types = db.query(LeaveType).all()
    leave_type_map = {lt.name: lt.id for lt in leave_types}
    
    REASON_MAP = {
        "Sick Leave": SICK_LEAVE_REASONS,
        "Casual Leave": CASUAL_LEAVE_REASONS,
        "Annual Leave": ANNUAL_LEAVE_REASONS,
        "Maternity Leave": MATERNITY_LEAVE_REASONS,
        "Paternity Leave": PATERNITY_LEAVE_REASONS,
        "Unpaid Leave": UNPAID_LEAVE_REASONS,
    }
    
    leaves = []
    statuses = ["pending", "approved", "rejected"]
    
    # Generate 100+ leave requests
    for _ in range(120):
        employee = random.choice(employees)
        leave_type_name = random.choices(
            list(leave_type_map.keys()),
            weights=[30, 25, 25, 5, 5, 10]  # Weighted probability
        )[0]
        
        type_id = leave_type_map[leave_type_name]
        reasons = REASON_MAP.get(leave_type_name, CASUAL_LEAVE_REASONS)
        
        # Generate random dates within the past year
        start_offset = random.randint(1, 300)
        duration = random.randint(1, 5) if leave_type_name not in ["Maternity Leave", "Paternity Leave"] else random.randint(5, 15)
        
        start_time = datetime.now() - timedelta(days=start_offset)
        end_time = start_time + timedelta(days=duration)
        
        status = random.choices(statuses, weights=[20, 60, 20])[0]
        
        leave = Leave(
            employee_id=employee.id,
            type_id=type_id,
            start_time=start_time,
            end_time=end_time,
            reason=random.choice(reasons),
            status=status,
            created_at=start_time - timedelta(days=random.randint(1, 7))
        )
        leaves.append(leave)
    
    db.add_all(leaves)
    db.commit()
    print(f"✅ Created {len(leaves)} leave requests")
    return leaves


def seed_approvals(db, leaves, managers):
    """Seed approvals for approved/rejected leaves"""
    print("\n✅ Seeding Approvals...")
    approvals = []
    
    for leave in leaves:
        if leave.status in ["approved", "rejected"]:
            manager = random.choice(managers)
            approval = Approval(
                leave_id=leave.id,
                approved_by=manager.id,
                approved_at=leave.created_at + timedelta(days=random.randint(1, 3)),
                decision=leave.status
            )
            approvals.append(approval)
    
    db.add_all(approvals)
    db.commit()
    print(f"✅ Created {len(approvals)} approval records")
    return approvals


def seed_audit_logs(db, admins, managers, employees):
    """Seed audit logs"""
    print("\n📋 Seeding Audit Logs...")
    audit_logs = []
    
    actor_pools = [
        ("admin", admins),
        ("manager", managers),
        ("employee", employees),
    ]
    
    target_tables = ["leaves", "employees", "managers", "leave_balance", "approvals"]
    
    for _ in range(200):
        actor_type, actors = random.choice(actor_pools)
        actor = random.choice(actors)
        
        log = AuditLog(
            actor_type=actor_type,
            actor_id=actor.id,
            action=random.choice(AUDIT_ACTIONS),
            target_table=random.choice(target_tables),
            target_id=random.randint(1, 100),
            timestamp=datetime.now() - timedelta(
                days=random.randint(0, 365),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )
        )
        audit_logs.append(log)
    
    db.add_all(audit_logs)
    db.commit()
    print(f"✅ Created {len(audit_logs)} audit log entries")
    return audit_logs


def print_summary(admins, managers, employees, leave_balances, leaves, approvals, audit_logs):
    """Print seeding summary"""
    print("\n" + "=" * 60)
    print("🎉 SEED DATA SUMMARY")
    print("=" * 60)
    print(f"👨‍💼 Admins:         {len(admins)}")
    print(f"👔 Managers:       {len(managers)}")
    print(f"👥 Employees:      {len(employees)}")
    print(f"📊 Leave Balances: {len(leave_balances)}")
    print(f"📝 Leave Requests: {len(leaves)}")
    print(f"✅ Approvals:      {len(approvals)}")
    print(f"📋 Audit Logs:     {len(audit_logs)}")
    print("=" * 60)
    print(f"\n🔑 Default Password for all users: {DEFAULT_PASSWORD}")
    print("\n📧 Sample Login Credentials:")
    print("-" * 40)
    print(f"Admin:    {ADMINS_DATA[0]['email']}")
    print(f"Manager:  {MANAGERS_DATA[0]['email']}")
    print(f"Employee: {EMPLOYEES_DATA[0]['email']}")
    print("=" * 60)


def seed_all():
    """Main function to seed all data"""
    print("\n" + "=" * 60)
    print("🌱 EMPLOYEE LEAVE MANAGEMENT - DATA SEEDER")
    print("=" * 60)
    
    db = SessionLocal()
    
    try:
        # Clear existing data
        clear_existing_data(db)
        
        # Seed data in order
        admins = seed_admins(db)
        managers = seed_managers(db)
        employees = seed_employees(db)
        leave_balances = seed_leave_balances(db, employees)
        leaves = seed_leaves(db, employees)
        approvals = seed_approvals(db, leaves, managers)
        audit_logs = seed_audit_logs(db, admins, managers, employees)
        
        # Print summary
        print_summary(admins, managers, employees, leave_balances, leaves, approvals, audit_logs)
        
        print("\n✅ All seed data created successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Error seeding data: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_all()
