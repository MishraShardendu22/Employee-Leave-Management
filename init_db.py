"""
Database initialization script to create and populate initial data
"""
from database import init_db, get_db
import crud

def seed_data():
    """Seed initial data into the database"""
    db = next(get_db())
    
    print("Seeding initial data...")
    
    # Create leave types
    leave_types = [
        "Sick Leave",
        "Casual Leave",
        "Annual Leave",
        "Maternity Leave",
        "Paternity Leave",
        "Unpaid Leave"
    ]
    
    for lt_name in leave_types:
        try:
            crud.create_leave_type(db, lt_name)
            print(f"Created leave type: {lt_name}")
        except Exception as e:
            print(f"Error creating {lt_name}: {e}")
    
    # Create a sample admin
    try:
        admin = crud.create_admin(db, "Admin User", "admin@example.com", "admin123")
        print(f"Created admin: {admin.email}")
    except Exception as e:
        print(f"Error creating admin: {e}")
    
    # Create a sample manager
    try:
        manager = crud.create_manager(db, "Manager User", "manager@example.com", "manager123")
        print(f"Created manager: {manager.email}")
    except Exception as e:
        print(f"Error creating manager: {e}")
    
    # Create a sample employee
    try:
        employee = crud.create_employee(db, "Employee User", "employee@example.com", "employee123")
        print(f"Created employee: {employee.email}")
        
        # Create leave balances for the employee
        leave_type_casual = crud.get_all_leave_types(db)[1]  # Casual Leave
        leave_type_annual = crud.get_all_leave_types(db)[2]  # Annual Leave
        
        crud.create_leave_balance(db, employee.id, leave_type_casual.id, 12)
        crud.create_leave_balance(db, employee.id, leave_type_annual.id, 20)
        print(f"Created leave balances for employee")
        
    except Exception as e:
        print(f"Error creating employee: {e}")
    
    db.close()
    print("Seeding completed!")


if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("Database initialized!")
    
    seed_data()
