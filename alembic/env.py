"""Alembic environment configuration."""
from logging.config import fileConfig
from sqlalchemy import pool, create_engine
from alembic import context
from app.core.config import settings
from app.core.database import Base
from app.models import user, signal  # Import all models
import sys
import urllib.parse
import os

# Set UTF-8 encoding for environment to avoid encoding issues
os.environ['PYTHONIOENCODING'] = 'utf-8'
os.environ['PGCLIENTENCODING'] = 'UTF8'  # Set PostgreSQL client encoding
if sys.platform == 'win32':
    # On Windows, try to set console encoding to UTF-8
    try:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
        # Also set the console code page to UTF-8
        import subprocess
        subprocess.run(['chcp', '65001'], shell=True, capture_output=True)
    except:
        pass
    # Set locale to avoid encoding issues
    try:
        import locale
        # Try to set UTF-8 locale
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    except:
        try:
            # Fallback to system default
            locale.setlocale(locale.LC_ALL, '')
        except:
            pass

# this is the Alembic Config object
config = context.config

# DEBUG: Print information about database URL
print("=" * 80)
print("DEBUG: Database URL Information")
print("=" * 80)
database_url_raw = settings.database_url_sync
print(f"Type: {type(database_url_raw)}")
print(f"Value (repr): {repr(database_url_raw)}")

# Check if it's bytes
if isinstance(database_url_raw, bytes):
    print(f"Bytes length: {len(database_url_raw)}")
    print(f"First 100 bytes (hex): {database_url_raw[:100].hex()}")
    print(f"First 100 bytes (repr): {repr(database_url_raw[:100])}")
    # Try different encodings
    for encoding in ['utf-8', 'latin-1', 'cp1252', 'cp866']:
        try:
            decoded = database_url_raw.decode(encoding)
            print(f"Successfully decoded as {encoding}: {decoded[:50]}...")
            database_url = decoded
            break
        except UnicodeDecodeError as e:
            print(f"Failed to decode as {encoding}: {e}")
    else:
        # If all fail, use replace
        database_url = database_url_raw.decode('utf-8', errors='replace')
        print(f"Using UTF-8 with errors='replace': {database_url[:50]}...")
elif not isinstance(database_url_raw, str):
    database_url = str(database_url_raw)
    print(f"Converted to string: {database_url[:50]}...")
else:
    database_url = database_url_raw
    print(f"Already a string: {database_url[:50]}...")

# Mask password in URL for safe printing
try:
    parsed = urllib.parse.urlparse(database_url)
    safe_url = f"{parsed.scheme}://{parsed.username}:***@{parsed.hostname}:{parsed.port}{parsed.path}"
    print(f"Safe URL (password hidden): {safe_url}")
except Exception as e:
    print(f"Could not parse URL: {e}")

print(f"Final URL type: {type(database_url)}")
print(f"Final URL length: {len(database_url)}")
print("=" * 80)

# Ensure the URL is properly encoded as UTF-8
if isinstance(database_url, bytes):
    database_url = database_url.decode('utf-8', errors='replace')
elif not isinstance(database_url, str):
    database_url = str(database_url)

# Re-encode to ensure clean UTF-8
database_url = database_url.encode('utf-8', errors='ignore').decode('utf-8')

config.set_main_option("sqlalchemy.url", database_url)

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    """Run migrations with connection."""
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    print("\n" + "=" * 80)
    print("DEBUG: run_migrations_online()")
    print("=" * 80)
    
    # Use the database URL directly to avoid encoding issues
    database_url = settings.database_url_sync
    print(f"Raw database_url type: {type(database_url)}")
    
    if isinstance(database_url, bytes):
        print("Database URL is bytes, attempting decode...")
        # Try multiple encodings
        for encoding in ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252', 'cp866']:
            try:
                database_url = database_url.decode(encoding)
                print(f"Successfully decoded as {encoding}")
                break
            except UnicodeDecodeError as e:
                print(f"Failed to decode as {encoding}: {e}")
        else:
            # If all fail, use replace
            database_url = database_url.decode('utf-8', errors='replace')
            print("Using UTF-8 with errors='replace'")
    elif not isinstance(database_url, str):
        database_url = str(database_url)
        print("Converted to string")
    else:
        print("Database URL is already a string")
    
    # Clean the URL - re-encode to ensure clean UTF-8
    print(f"Before cleaning - type: {type(database_url)}, length: {len(database_url)}")
    original_url = database_url
    
    # Try to parse and reconstruct URL with proper URL encoding
    try:
        parsed = urllib.parse.urlparse(database_url)
        print(f"Parsed URL components:")
        print(f"  scheme: {parsed.scheme}")
        print(f"  username: {parsed.username}")
        print(f"  password: {'***' if parsed.password else 'None'}")
        print(f"  hostname: {parsed.hostname}")
        print(f"  port: {parsed.port}")
        print(f"  path: {parsed.path}")
        
        # Reconstruct URL with proper URL encoding for each component
        # This ensures special characters in password/username are properly encoded
        if parsed.password:
            # Check password encoding
            try:
                parsed.password.encode('utf-8')
                print("  Password is valid UTF-8")
            except UnicodeEncodeError as e:
                print(f"  Password has encoding issue: {e}")
                # URL-encode the password
                password_encoded = urllib.parse.quote(parsed.password, safe='')
                print(f"  Password after URL encoding: {password_encoded[:20]}...")
                # Reconstruct with encoded password
                netloc = f"{parsed.username}:{password_encoded}@{parsed.hostname}"
                if parsed.port:
                    netloc += f":{parsed.port}"
                parsed = parsed._replace(netloc=netloc)
        
        # Reconstruct URL
        database_url = urllib.parse.urlunparse(parsed)
        print(f"Reconstructed URL successfully")
        print(f"Reconstructed URL (first 80 chars): {database_url[:80]}...")
    except Exception as e:
        print(f"Warning: Could not parse/reconstruct URL: {e}")
        import traceback
        traceback.print_exc()
        print(f"Using original URL")
        # Fallback: try to clean the URL
        try:
            database_url = original_url.encode('utf-8', errors='ignore').decode('utf-8')
        except:
            pass
    
    print(f"Final URL type: {type(database_url)}")
    print(f"Final URL length: {len(database_url)}")
    
    # Verify URL can be encoded as UTF-8 bytes
    try:
        url_bytes = database_url.encode('utf-8')
        print(f"URL can be encoded as UTF-8: {len(url_bytes)} bytes")
    except UnicodeEncodeError as e:
        print(f"ERROR: URL cannot be encoded as UTF-8: {e}")
        # Find problematic characters
        for i, char in enumerate(database_url):
            try:
                char.encode('utf-8')
            except UnicodeEncodeError:
                print(f"  Problematic char at position {i}: {repr(char)} (U+{ord(char):04X})")
        raise
    
    print("=" * 80 + "\n")
    
    # Create engine directly to avoid encoding issues
    # Try using connection parameters dict instead of URL string to avoid encoding issues
    try:
        print("Creating SQLAlchemy engine...")
        
        # Parse URL and extract components
        parsed = urllib.parse.urlparse(database_url)
        
        # Build connection parameters dict for psycopg2
        # This avoids passing the URL as a string, which might have encoding issues
        # psycopg2 uses 'dbname' not 'database'
        dbname = parsed.path.lstrip('/') if parsed.path else 'postgres'
        connect_args = {
            'host': parsed.hostname or 'localhost',
            'port': parsed.port or 5432,
            'dbname': dbname,  # psycopg2 uses 'dbname', not 'database'
            'user': parsed.username or 'postgres',
            'password': parsed.password or '',
            'client_encoding': 'UTF8'
        }
        
        print(f"Connection parameters:")
        print(f"  host: {connect_args['host']}")
        print(f"  port: {connect_args['port']}")
        print(f"  dbname: {connect_args['dbname']}")
        print(f"  user: {connect_args['user']}")
        print(f"  password: {'***' if connect_args['password'] else 'None'}")
        
        # Ensure all string parameters are properly encoded as UTF-8
        # Convert to bytes and back to ensure clean UTF-8
        # Also, URL-encode any non-ASCII characters to avoid encoding issues with psycopg2
        for key in ['host', 'dbname', 'user', 'password']:
            if isinstance(connect_args[key], str):
                # Check if string contains only ASCII
                try:
                    connect_args[key].encode('ascii')
                    # All ASCII, no need to encode
                    print(f"  {key} is pure ASCII")
                except UnicodeEncodeError:
                    # Contains non-ASCII, but we'll keep it as is for now
                    # psycopg2 should handle UTF-8 strings
                    print(f"  {key} contains non-ASCII characters")
                    # Force clean UTF-8 encoding
                    try:
                        # Test encoding
                        test_bytes = connect_args[key].encode('utf-8')
                        # Decode back to ensure it's valid
                        connect_args[key] = test_bytes.decode('utf-8')
                    except (UnicodeEncodeError, UnicodeDecodeError):
                        # If there are issues, use replace to fix them
                        connect_args[key] = connect_args[key].encode('utf-8', errors='replace').decode('utf-8')
        
        # Use psycopg2.connect() directly with a connection creator function
        # This gives us full control over the connection and avoids encoding issues
        # Set PostgreSQL environment variables to avoid encoding issues
        # Clear any existing PG* environment variables that might have encoding issues
        pg_env_vars = ['PGHOST', 'PGPORT', 'PGDATABASE', 'PGUSER', 'PGPASSWORD', 'PGCLIENTENCODING']
        for var in pg_env_vars:
            if var in os.environ:
                del os.environ[var]
        
        # Set clean environment variables
        os.environ['PGCLIENTENCODING'] = 'UTF8'
        
        import psycopg2
        import psycopg2.extensions
        
        # Monkey-patch psycopg2 to handle encoding errors gracefully
        # This is a workaround for Windows encoding issues
        original_connect = psycopg2.connect
        def patched_connect(*args, **kwargs):
            try:
                return original_connect(*args, **kwargs)
            except UnicodeDecodeError as e:
                # If we get a UnicodeDecodeError, it might be from error message encoding
                # Try to decode the error message in different encodings
                if hasattr(e, 'object') and isinstance(e.object, bytes):
                    # Try to decode error message in Windows-1251 (common Russian encoding)
                    try:
                        error_msg = e.object.decode('windows-1251', errors='replace')
                        print(f"WARNING: Decoded error message (Windows-1251): {error_msg}")
                    except:
                        pass
                    # Try cp866 (another Russian encoding)
                    try:
                        error_msg = e.object.decode('cp866', errors='replace')
                        print(f"WARNING: Decoded error message (CP866): {error_msg}")
                    except:
                        pass
                # Re-raise the original error
                raise
        psycopg2.connect = patched_connect
        
        def create_psycopg2_connection():
            """Create psycopg2 connection directly."""
            print("Creating psycopg2 connection directly...")
            print(f"Connection args types and values:")
            for key, value in connect_args.items():
                if key == 'password':
                    print(f"  {key}: {type(value)}, length={len(value)}, value=***")
                else:
                    print(f"  {key}: {type(value)}, value={repr(value)}")
                    # Check encoding
                    if isinstance(value, str):
                        try:
                            value.encode('utf-8')
                            print(f"    -> Valid UTF-8")
                        except UnicodeEncodeError as e:
                            print(f"    -> Encoding error: {e}")
            
            # Check for problematic bytes in password
            if isinstance(connect_args['password'], str):
                pass_bytes = connect_args['password'].encode('utf-8')
                print(f"Password as UTF-8 bytes: {pass_bytes.hex()}")
                # Check for 0xc2 byte
                if b'\xc2' in pass_bytes:
                    idx = pass_bytes.index(b'\xc2')
                    print(f"WARNING: Found 0xc2 byte at position {idx} in password bytes")
            
            try:
                # Try to create connection with explicit encoding handling
                # First, ensure all string parameters are bytes, then decode
                conn_params = {}
                for key, value in connect_args.items():
                    if isinstance(value, str):
                        # Convert to bytes and back to ensure clean UTF-8
                        try:
                            # Test if it can be encoded
                            test_bytes = value.encode('utf-8')
                            # Check for problematic bytes
                            if b'\xc2' in test_bytes:
                                pos = test_bytes.index(b'\xc2')
                                print(f"WARNING: Found 0xc2 in {key} bytes at position {pos}")
                            conn_params[key] = value
                        except UnicodeEncodeError:
                            # Fix encoding issues
                            conn_params[key] = value.encode('utf-8', errors='replace').decode('utf-8')
                    else:
                        conn_params[key] = value
                
                # Create connection
                conn = psycopg2.connect(**conn_params)
                print("psycopg2 connection created successfully")
                return conn
            except UnicodeDecodeError as e:
                print(f"UnicodeDecodeError in psycopg2.connect(): {e}")
                print(f"Error object type: {type(e.object) if hasattr(e, 'object') else 'N/A'}")
                if hasattr(e, 'object') and hasattr(e, 'start'):
                    print(f"Problematic bytes: {e.object[e.start:e.end].hex()}")
                    print(f"Context: {repr(e.object[max(0, e.start-10):e.end+10])}")
                import traceback
                traceback.print_exc()
                raise
            except Exception as e:
                print(f"Error creating psycopg2 connection: {e}")
                import traceback
                traceback.print_exc()
                raise
        
        # Create a minimal URL for SQLAlchemy
        # We'll use a custom connection creator
        minimal_url = f"{parsed.scheme}://localhost/postgres"
        
        print(f"Using connection creator function with minimal URL: {minimal_url}")
        
        # Create engine with custom connection creator
        connectable = create_engine(
            minimal_url,
            poolclass=pool.NullPool,
            echo=False,
            creator=create_psycopg2_connection
        )
        print("Engine created successfully")
    except Exception as e:
        print(f"ERROR creating engine: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        raise

    try:
        print("Attempting to connect to database...")
        # Try to get connection info before connecting
        print(f"Connection URL (masked): {database_url.split('@')[0]}@***")
        
        with connectable.connect() as connection:
            print("Connection established successfully!")
            context.configure(connection=connection, target_metadata=target_metadata)

            with context.begin_transaction():
                print("Running migrations...")
                context.run_migrations()
                print("Migrations completed successfully!")
    except UnicodeDecodeError as e:
        print(f"UnicodeDecodeError during connection: {e}")
        print(f"Error at position: {e.start if hasattr(e, 'start') else 'unknown'}")
        print(f"Problematic bytes: {e.object[e.start:e.end].hex() if hasattr(e, 'object') and hasattr(e, 'start') else 'unknown'}")
        import traceback
        traceback.print_exc()
        raise
    except Exception as e:
        print(f"ERROR during connection/migration: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        raise


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

