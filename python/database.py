import mysql.connector
from config import DB_CONFIG

def get_connection():
    """Create and return a connection to MySQL."""
    return mysql.connector.connect(**DB_CONFIG)

def fetch_all(query, params = None):
    """
    Run the SELECT statement and return the entire result as a list of dict.
    Example: [{"UserID": 1, "UserName": "Alex"}, ...]
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary = True) # Return the result as a dictionary.
    cursor.execute(query, params or ())
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def fetch_one(query, params = None):
    """Run the SELECT statement and return a single line."""
    conn = get_connection()
    cursor = conn.cursor(dictionary = True)
    cursor.execute(query, params or ())
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

def execute(query, params = None):
    """
    Execute the INSERT / UPDATE / DELETE statement.
    Returns the ID of the record just created (if it was an INSERT statement).
    """
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    try:
        cursor.execute(query, params or ())
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        print(f"Error executing query: {e}")
        conn.rollback()
        return None
    finally:
        last_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return last_id

def call_procedure(proc_name, params = None):
    """Call the Stored Procedure created in MySQL."""
    conn = get_connection()
    cursor = conn.cursor(dictionary = True)
    cursor.callproc(proc_name, params or [])
    results = []
    for result in cursor.stored_results():
        results.extend(result.fetchall())
    conn.commit() # Save the change into database (if any)
    cursor.close()
    conn.close()
    return results