"""
Script to help configure SQL database connection
"""
import os
from dotenv import load_dotenv

load_dotenv()

def setup_sql_config():
    """Interactive setup for SQL database configuration"""
    print("=" * 80)
    print("SQL Database Configuration Setup")
    print("=" * 80)
    print("\nThis script will help you configure the SQL database connection.")
    print("The actual datasets will be loaded from your SQL database.\n")
    
    # Database type
    print("Database types supported:")
    print("  1. MySQL")
    print("  2. PostgreSQL")
    print("  3. SQL Server")
    print("  4. SQLite")
    
    db_choice = input("\nSelect database type (1-4) [default: 1 (MySQL)]: ").strip() or "1"
    db_types = {"1": "mysql", "2": "postgresql", "3": "sqlserver", "4": "sqlite"}
    db_type = db_types.get(db_choice, "mysql")
    
    # Connection details
    if db_type != "sqlite":
        host = input("Database host [default: localhost]: ").strip() or "localhost"
        port = input("Database port [default: 3306 for MySQL, 5432 for PostgreSQL]: ").strip()
        user = input("Database user [default: root]: ").strip() or "root"
        password = input("Database password: ").strip()
        database = input("Database name: ").strip()
    else:
        host = ""
        port = ""
        user = ""
        password = ""
        database = input("SQLite database file path: ").strip()
    
    # Table names
    table1 = input(f"Table name for Dataset 1 [default: health_dataset_1]: ").strip() or "health_dataset_1"
    table2 = input(f"Table name for Dataset 2 [default: health_dataset_2]: ").strip() or "health_dataset_2"
    
    # Write to .env file
    env_content = []
    if os.path.exists(".env"):
        with open(".env", "r") as f:
            env_content = f.readlines()
    
    # Update or add SQL configuration
    sql_vars = {
        "SQL_DB_TYPE": db_type,
        "SQL_HOST": host,
        "SQL_PORT": port,
        "SQL_USER": user,
        "SQL_PASSWORD": password,
        "SQL_DATABASE": database,
        "SQL_TABLE_1": table1,
        "SQL_TABLE_2": table2
    }
    
    # Remove old SQL config lines
    env_content = [line for line in env_content if not line.startswith("SQL_")]
    
    # Add new SQL config
    env_content.append("\n# SQL Database Configuration\n")
    for key, value in sql_vars.items():
        env_content.append(f"{key}={value}\n")
    
    with open(".env", "w") as f:
        f.writelines(env_content)
    
    print("\n✓ Configuration saved to .env file")
    print("\nConfiguration summary:")
    print(f"  Database Type: {db_type}")
    if db_type != "sqlite":
        print(f"  Host: {host}")
        print(f"  Port: {port}")
        print(f"  User: {user}")
        print(f"  Database: {database}")
    else:
        print(f"  Database File: {database}")
    print(f"  Table 1: {table1}")
    print(f"  Table 2: {table2}")
    print("\nYou can now run the data preprocessing script to load data from SQL.")

if __name__ == "__main__":
    setup_sql_config()

