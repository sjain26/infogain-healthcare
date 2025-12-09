# SQL Database Setup Guide

## Overview

The Healthcare GenAI Analytics System is designed to load actual datasets from your SQL database. The system supports multiple database types and automatically falls back to Excel/CSV files if SQL connection is not configured.

## Supported Databases

- **MySQL** (default)
- **PostgreSQL**
- **SQL Server**
- **SQLite**

## Quick Setup

### Option 1: Interactive Setup (Recommended)

```bash
python setup_sql.py
```

This will guide you through the configuration process interactively.

### Option 2: Manual Configuration

1. Copy the example environment file:
   ```bash
   cp ENV_EXAMPLE.txt .env
   ```

2. Edit `.env` file and add your SQL connection details:

   **For MySQL:**
   ```env
   SQL_DB_TYPE=mysql
   SQL_HOST=localhost
   SQL_PORT=3306
   SQL_USER=your_username
   SQL_PASSWORD=your_password
   SQL_DATABASE=healthcare
   SQL_TABLE_1=health_dataset_1
   SQL_TABLE_2=health_dataset_2
   ```

   **For PostgreSQL:**
   ```env
   SQL_DB_TYPE=postgresql
   SQL_HOST=localhost
   SQL_PORT=5432
   SQL_USER=postgres
   SQL_PASSWORD=your_password
   SQL_DATABASE=healthcare
   SQL_TABLE_1=health_dataset_1
   SQL_TABLE_2=health_dataset_2
   ```

   **For SQL Server:**
   ```env
   SQL_DB_TYPE=sqlserver
   SQL_HOST=localhost
   SQL_PORT=1433
   SQL_USER=sa
   SQL_PASSWORD=your_password
   SQL_DATABASE=healthcare
   SQL_TABLE_1=health_dataset_1
   SQL_TABLE_2=health_dataset_2
   ```

   **For SQLite:**
   ```env
   SQL_DB_TYPE=sqlite
   SQL_HOST=
   SQL_PORT=
   SQL_USER=
   SQL_PASSWORD=
   SQL_DATABASE=/path/to/your/database.db
   SQL_TABLE_1=health_dataset_1
   SQL_TABLE_2=health_dataset_2
   ```

## Data Loading Priority

The system loads data in the following priority order:

1. **SQL Database** (if configured in `.env`)
2. **Excel File** (`lu1828272yg3dhb.xlsm` - sample data)
3. **CSV Files** (`data/health_dataset_1.csv`, `data/health_dataset_2.csv`)

## Table Structure Requirements

### Dataset 1 Table (health_dataset_1)

Your SQL table should have the following columns:

- `Patient_Number` - Patient identifier (can be INT or VARCHAR)
- `Blood_Pressure_Abnormality` - 0 or 1
- `Level_of_Hemoglobin` - Numeric (g/dl)
- `Genetic_Pedigree_Coefficient` - Numeric (0-1)
- `Age` - Integer
- `BMI` - Numeric
- `Sex` - 0 (Male) or 1 (Female)
- `Pregnancy` - 0 or 1
- `Smoking` - 0 or 1
- `salt_content_in_the_diet` - Numeric (mg/day)
- `alcohol_consumption_per_day` - Numeric (ml/day)
- `Level_of_Stress` - 1 (Low), 2 (Normal), or 3 (High)
- `Chronic_kidney_disease` - 0 or 1
- `Adrenal_and_thyroid_disorders` - 0 or 1

### Dataset 2 Table (health_dataset_2)

Your SQL table should have the following columns:

- `Patient_Number` - Patient identifier (must match Dataset 1)
- `Day_Number` - Integer (1-10)
- `Physical_activity` - Integer (steps per day)

## Testing the Connection

After configuring your SQL connection, test it:

```bash
python data_preprocessing.py
```

You should see:
```
✓ Loaded Dataset 1 from SQL table 'health_dataset_1': X records
✓ Loaded Dataset 2 from SQL table 'health_dataset_2': Y records
```

## Troubleshooting

### Connection Refused

**Error:** `Can't connect to MySQL server on 'localhost'`

**Solutions:**
- Verify your database server is running
- Check host and port are correct
- Verify firewall settings
- Test connection with database client

### Table Not Found

**Error:** `Table 'healthcare.health_dataset_1' doesn't exist`

**Solutions:**
- Verify table names in `.env` match your actual table names
- Check database name is correct
- Ensure you have SELECT permissions on the tables

### Authentication Failed

**Error:** `Access denied for user`

**Solutions:**
- Verify username and password
- Check user has access to the database
- Ensure user has SELECT permissions

### Missing Database Driver

**Error:** `No module named 'pymysql'` or similar

**Solutions:**
```bash
# Install MySQL driver
pip install pymysql

# Install PostgreSQL driver
pip install psycopg2-binary

# Install SQL Server driver (if needed)
pip install pyodbc
```

## Notes

- The system automatically handles missing values and data cleaning
- Column names are case-sensitive - ensure they match exactly
- The system creates a local SQLite database (`data/healthcare.db`) for query execution, regardless of your source database
- Your original SQL database is only used for data loading, not for query execution

## Security Considerations

- Never commit your `.env` file to version control
- Use strong passwords for database connections
- Consider using connection pooling for production environments
- Use read-only database users if possible

