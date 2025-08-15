import configparser
import mysql.connector
from datetime import datetime, date

# ===== Date parsing helper =====
def parse_iso_date(date_str):
    """
    Ensure the date is in YYYY-MM-DD format and return a datetime.date object.
    Raises ValueError if invalid.
    """
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError(f"Invalid date format: {date_str}. Use YYYY-MM-DD.")

# ===== Load MySQL config =====
def load_config(path="config.ini"):
    config = configparser.ConfigParser()
    config.read(path)
    return config["mysql"]

# ===== Create DB, Tables, and Insert Default Manager =====
def create_tables_and_insert_manager():
    cfg = load_config()

    # Connect without selecting database to create it if needed
    conn = mysql.connector.connect(
        host=cfg["host"],
        user=cfg["user"],
        password=cfg["password"],
        port=int(cfg.get("port", 3306))
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ecofriendly")
    conn.commit()
    conn.close()

    # Reconnect to the ecofriendly database
    conn = mysql.connector.connect(
        host=cfg["host"],
        user=cfg["user"],
        password=cfg["password"],
        database="ecofriendly",
        port=int(cfg.get("port", 3306))
    )
    cursor = conn.cursor()

    # ===== Table creation SQL =====
    tables = [

        # employees
        """
        CREATE TABLE IF NOT EXISTS employees (
            identity VARCHAR(20) PRIMARY KEY UNIQUE NOT NULL,
            name VARCHAR(100) NOT NULL,
            phone VARCHAR(15),
            location VARCHAR(100),
            joining_date DATE,
            worker_type ENUM('Driver', 'Cleaner', 'Maintenance Worker') DEFAULT NULL,
            role ENUM('manager','worker') NOT NULL,
            hashed_password VARCHAR(256) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,

        # vehicles
        """
        CREATE TABLE IF NOT EXISTS vehicles (
            licensePlate VARCHAR(10) PRIMARY KEY,
            type VARCHAR(50) NOT NULL,
            status VARCHAR(50) NOT NULL,
            location VARCHAR(100) NOT NULL,
            lastMaintenance DATE NOT NULL
        )
        """,

        # bins (fixed syntax)
        """
        CREATE TABLE IF NOT EXISTS bins (
            binId VARCHAR(50) PRIMARY KEY,
            location VARCHAR(100) NOT NULL,
            address VARCHAR(255) NOT NULL,
            status ENUM('Full', 'Mid', 'Empty') NOT NULL DEFAULT 'Empty',
            lat FLOAT NOT NULL DEFAULT 0,
            lon FLOAT NOT NULL DEFAULT 0,
            capacity FLOAT NOT NULL DEFAULT 0
        )
        """,

        # shifts
        """
        CREATE TABLE IF NOT EXISTS shifts (
            shift_id VARCHAR(20) PRIMARY KEY,
            worker_id VARCHAR(20) NOT NULL,
            worker_name VARCHAR(100) NOT NULL,
            worker_type VARCHAR(50) NOT NULL,
            date DATE NOT NULL,
            start_time TIME NOT NULL,
            end_time TIME NOT NULL,
            location VARCHAR(100) NOT NULL,
            FOREIGN KEY (worker_id) REFERENCES employees (identity)
        )
        """,

        # shift_proposals
        """
        CREATE TABLE IF NOT EXISTS shift_proposals (
            id VARCHAR(20) PRIMARY KEY,
            worker_id VARCHAR(20) NOT NULL,
            worker_name VARCHAR(100) NOT NULL,
            worker_type VARCHAR(50) NOT NULL,
            date DATE NOT NULL,
            start_time TIME NOT NULL,
            end_time TIME NOT NULL,
            location VARCHAR(100) NOT NULL,
            status VARCHAR(20) NOT NULL DEFAULT 'pending',
            submitted_at DATE NOT NULL,
            FOREIGN KEY (worker_id) REFERENCES employees(identity)
        )
        """,

        # payments
        """
        CREATE TABLE IF NOT EXISTS payments (
            payment_id VARCHAR(20) PRIMARY KEY,
            worker_id VARCHAR(20) NOT NULL,
            worker_name VARCHAR(100) NOT NULL,
            amount FLOAT NOT NULL,
            payment_date DATE NOT NULL,
            status VARCHAR(20) NOT NULL DEFAULT 'Pending',
            notes VARCHAR(255),
            FOREIGN KEY (worker_id) REFERENCES employees(identity)
        )
        """,

        # hardware
        """
        CREATE TABLE IF NOT EXISTS hardware (
            id VARCHAR(50) PRIMARY KEY,
            binId VARCHAR(50) DEFAULT NULL,
            status ENUM('Operational','Needs Maintenance') NOT NULL DEFAULT 'Operational',
            battery FLOAT NOT NULL DEFAULT 100,
            lastChecked VARCHAR(50) NOT NULL
        )
        """
    ]

    # Execute all CREATE TABLE statements
    for table in tables:
        cursor.execute(table)

    conn.commit()
    print("✅ All tables created successfully!")

    # ===== Default Manager Insert =====
    default_id = "207705096"
    default_name = "Admin Manager"
    default_phone = "0500000000"
    default_location = "Haifa"
    default_join = parse_iso_date("2024-01-01")
    default_role = "manager"
    default_password_plain = "123456"
    default_password_hash = "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92"  # SHA256 of 123456

    cursor.execute("SELECT COUNT(*) FROM employees WHERE identity=%s", (default_id,))
    exists = cursor.fetchone()[0] > 0

    if not exists:
        cursor.execute("""
            INSERT INTO employees (identity, name, phone, location, joining_date, role, hashed_password)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, (
            default_id,
            default_name,
            default_phone,
            default_location,
            default_join,
            default_role,
            default_password_hash
        ))
        conn.commit()
        print("👤 Default Manager Added (first time)!")
    else:
        print("👤 Default Manager already exists.")

    # Always print credentials for testing
    print(f"   ID: {default_id}")
    print(f"   Name: {default_name}")
    print(f"   Role: {default_role}")
    print(f"   Temporary Password: {default_password_plain}")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    create_tables_and_insert_manager()
