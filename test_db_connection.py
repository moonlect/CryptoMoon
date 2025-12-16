"""Test database connection directly."""
import psycopg2
import os

# Set encoding
os.environ['PGCLIENTENCODING'] = 'UTF8'

try:
    print("Attempting to connect to database...")
    conn = psycopg2.connect(
        host='localhost',
        port=5432,
        dbname='cryptotracker',
        user='postgres',
        password='postgres',
        client_encoding='UTF8'
    )
    print("Connection successful!")
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    print(f"PostgreSQL version: {version[0]}")
    conn.close()
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

