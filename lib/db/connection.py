import sqlite3
from pathlib import Path

CONN = None

def get_connection():
    global CONN
    if CONN is None:
        db_path = Path(__file__).parent.parent.parent / "articles.db"
        CONN = sqlite3.connect(str(db_path))
        CONN.row_factory = sqlite3.Row
    return CONN

def init_db():
    """Initialize the database with schema"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Read and execute schema file
    schema_path = Path(__file__).parent.parent.parent / "schema.sql"
    with open(schema_path) as f:
        schema_sql = f.read()
    
    cursor.executescript(schema_sql)
    conn.commit()