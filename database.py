import csv
import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "hr_data.db")
EMPLOYEE_CSV = os.path.join(BASE_DIR, "data", "employees.csv")

_connection = None

def get_connection():
    global _connection
    if _connection is None:
        _connection = sqlite3.connect(DB_PATH, check_same_thread=False)
        _connection.row_factory = sqlite3.Row
        _init_db(_connection)
    return _connection

def _init_db(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            employee_id TEXT PRIMARY KEY,
            department TEXT NOT NULL,
            job_title TEXT NOT NULL,
            employment_type TEXT NOT NULL,
            start_date TEXT NOT NULL,
            pto_balance_days REAL NOT NULL,
            status TEXT NOT NULL
        )
    """)
    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM employees")
    if cursor.fetchone()[0] == 0:
        _load_initial_data(conn)

def _load_initial_data(conn):
    with open(EMPLOYEE_CSV, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            conn.execute(
                "INSERT INTO employees VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    row['employee_id'],
                    row['department'],
                    row['job_title'],
                    row['employment_type'],
                    row['start_date'],
                    float(row['pto_balance_days']),
                    row['status'],
                ),
            )
        conn.commit()

if __name__ == "__main__":
    get_connection()
