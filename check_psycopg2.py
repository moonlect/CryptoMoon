"""Check psycopg2 version and environment."""
import psycopg2
import os

print(f"psycopg2 version: {psycopg2.__version__}")
print("\nPostgreSQL environment variables:")
env_vars = ['PGHOST', 'PGPORT', 'PGDATABASE', 'PGUSER', 'PGPASSWORD', 'DATABASE_URL', 'DATABASE_URL_SYNC']
for var in env_vars:
    value = os.environ.get(var, "NOT SET")
    if value != "NOT SET":
        # Check encoding
        try:
            if isinstance(value, str):
                value.encode('utf-8')
                print(f"  {var}: OK (UTF-8), length={len(value)}")
            else:
                print(f"  {var}: {type(value)}")
        except UnicodeEncodeError as e:
            print(f"  {var}: ENCODING ERROR - {e}")
    else:
        print(f"  {var}: NOT SET")

