-- Employee Leave Management System Database Schema
-- PostgreSQL Database Schema

-- Drop tables if they exist (in correct order due to foreign keys)
DROP TABLE IF EXISTS audit_logs CASCADE;
DROP TABLE IF EXISTS leave_balance CASCADE;
DROP TABLE IF EXISTS approvals CASCADE;
DROP TABLE IF EXISTS leaves CASCADE;
DROP TABLE IF EXISTS leave_types CASCADE;
DROP TABLE IF EXISTS managers CASCADE;
DROP TABLE IF EXISTS employees CASCADE;
DROP TABLE IF EXISTS admins CASCADE;

-- Create admins table
CREATE TABLE admins (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Create employees table
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Create managers table
CREATE TABLE managers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Create leave_types table
CREATE TABLE leave_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

-- Create leaves table
CREATE TABLE leaves (
    id SERIAL PRIMARY KEY,
    employee_id INT NOT NULL REFERENCES employees(id) ON DELETE CASCADE,
    type_id INT NOT NULL REFERENCES leave_types(id) ON DELETE CASCADE,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    reason TEXT,
    status VARCHAR(20) DEFAULT 'pending' NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT check_dates CHECK (end_time > start_time),
    CONSTRAINT check_status CHECK (status IN ('pending', 'approved', 'rejected'))
);

-- Create approvals table
CREATE TABLE approvals (
    id SERIAL PRIMARY KEY,
    leave_id INT NOT NULL REFERENCES leaves(id) ON DELETE CASCADE,
    approved_by INT NOT NULL REFERENCES managers(id) ON DELETE CASCADE,
    approved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    decision VARCHAR(20) NOT NULL,
    CONSTRAINT check_decision CHECK (decision IN ('approved', 'rejected'))
);

-- Create leave_balance table
CREATE TABLE leave_balance (
    id SERIAL PRIMARY KEY,
    employee_id INT NOT NULL REFERENCES employees(id) ON DELETE CASCADE,
    type_id INT NOT NULL REFERENCES leave_types(id) ON DELETE CASCADE,
    total_allocated INT NOT NULL DEFAULT 0 CHECK (total_allocated >= 0),
    total_used INT NOT NULL DEFAULT 0 CHECK (total_used >= 0),
    remaining INT NOT NULL DEFAULT 0 CHECK (remaining >= 0),
    CONSTRAINT unique_employee_leave_type UNIQUE (employee_id, type_id)
);

-- Create audit_logs table
CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    actor_type VARCHAR(20) NOT NULL,
    actor_id INT NOT NULL,
    action TEXT NOT NULL,
    target_table VARCHAR(50) NOT NULL,
    target_id INT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT check_actor_type CHECK (actor_type IN ('admin', 'manager', 'employee'))
);

-- Create indexes for better query performance
CREATE INDEX idx_employees_email ON employees(email);
CREATE INDEX idx_managers_email ON managers(email);
CREATE INDEX idx_admins_email ON admins(email);
CREATE INDEX idx_leaves_employee_id ON leaves(employee_id);
CREATE INDEX idx_leaves_status ON leaves(status);
CREATE INDEX idx_approvals_leave_id ON approvals(leave_id);
CREATE INDEX idx_approvals_manager_id ON approvals(approved_by);
CREATE INDEX idx_leave_balance_employee_id ON leave_balance(employee_id);
CREATE INDEX idx_audit_logs_actor ON audit_logs(actor_type, actor_id);
CREATE INDEX idx_audit_logs_timestamp ON audit_logs(timestamp DESC);

-- Insert default leave types
INSERT INTO leave_types (name) VALUES
    ('Sick Leave'),
    ('Casual Leave'),
    ('Annual Leave'),
    ('Maternity Leave'),
    ('Paternity Leave'),
    ('Unpaid Leave');

-- Comments for documentation
COMMENT ON TABLE admins IS 'Stores admin user accounts';
COMMENT ON TABLE employees IS 'Stores employee user accounts';
COMMENT ON TABLE managers IS 'Stores manager user accounts';
COMMENT ON TABLE leave_types IS 'Defines types of leave available';
COMMENT ON TABLE leaves IS 'Stores all leave requests';
COMMENT ON TABLE approvals IS 'Stores manager approval decisions for leave requests';
COMMENT ON TABLE leave_balance IS 'Tracks leave balances for each employee by leave type';
COMMENT ON TABLE audit_logs IS 'Audit trail of all actions in the system';
