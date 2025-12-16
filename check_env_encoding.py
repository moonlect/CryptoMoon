"""Script to check and fix .env file encoding issues."""
import os
import sys

def check_and_fix_env():
    """Check .env file encoding and suggest fixes."""
    env_file = ".env"
    
    if not os.path.exists(env_file):
        print(f"ERROR: {env_file} file not found!")
        return False
    
    print("=" * 80)
    print("Checking .env file encoding")
    print("=" * 80)
    
    # Read file as bytes
    with open(env_file, "rb") as f:
        content_bytes = f.read()
    
    print(f"File size: {len(content_bytes)} bytes")
    
    # Try different encodings
    encodings_to_try = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252', 'cp866', 'windows-1251']
    decoded_content = None
    used_encoding = None
    
    for encoding in encodings_to_try:
        try:
            decoded = content_bytes.decode(encoding)
            print(f"[OK] Successfully decoded as {encoding}")
            decoded_content = decoded
            used_encoding = encoding
            break
        except UnicodeDecodeError as e:
            print(f"[FAIL] Failed to decode as {encoding}: {e}")
    
    if not decoded_content:
        print("\nERROR: Could not decode .env file with any encoding!")
        return False
    
    print(f"\nUsing encoding: {used_encoding}")
    
    # Check for DATABASE_URL_SYNC
    lines = decoded_content.split('\n')
    db_url_line = None
    db_url_line_num = None
    
    for i, line in enumerate(lines, 1):
        if 'DATABASE_URL_SYNC' in line.upper():
            db_url_line = line
            db_url_line_num = i
            break
    
    if not db_url_line:
        print("\nWARNING: DATABASE_URL_SYNC not found in .env file")
        return False
    
    print(f"\nFound DATABASE_URL_SYNC at line {db_url_line_num}:")
    print(f"  {db_url_line[:100]}...")
    
    # Extract URL
    if '=' in db_url_line:
        url = db_url_line.split('=', 1)[1].strip()
        # Remove quotes if present
        url = url.strip('"').strip("'")
        
        print(f"\nDatabase URL (first 80 chars): {url[:80]}...")
        
        # Check for problematic characters
        problematic = []
        for i, char in enumerate(url):
            try:
                char.encode('utf-8')
            except UnicodeEncodeError:
                problematic.append((i, char, ord(char)))
        
        if problematic:
            print(f"\n[WARNING] Found {len(problematic)} problematic characters:")
            for pos, char, code in problematic[:10]:
                print(f"  Position {pos}: {repr(char)} (U+{code:04X})")
            
            # Try to parse URL
            import urllib.parse
            try:
                parsed = urllib.parse.urlparse(url)
                if parsed.password:
                    print(f"\nPassword found (length: {len(parsed.password)})")
                    # Check password
                    pass_problematic = []
                    for i, char in enumerate(parsed.password):
                        try:
                            char.encode('utf-8')
                        except UnicodeEncodeError:
                            pass_problematic.append((i, char, ord(char)))
                    
                    if pass_problematic:
                        print(f"  Password has {len(pass_problematic)} problematic characters")
                        print("\nSOLUTION: URL-encode special characters in password")
                        print("  Example: if password is 'p@ss#word', use 'p%40ss%23word'")
                        print("  Or use urllib.parse.quote() to encode it")
            except:
                pass
        else:
            print("\n[OK] No problematic characters found in URL")
        
        # Check if file needs to be re-saved as UTF-8
        if used_encoding != 'utf-8':
            print(f"\n[WARNING] File is encoded as {used_encoding}, not UTF-8")
            print("SOLUTION: Re-save the file as UTF-8")
            print("  In Notepad++: Encoding → Convert to UTF-8")
            print("  In VS Code: Click encoding in status bar → Save with Encoding → UTF-8")
            
            # Offer to create a fixed version
            response = input("\nCreate a UTF-8 version? (y/n): ").strip().lower()
            if response == 'y':
                backup_file = f"{env_file}.backup"
                print(f"Creating backup: {backup_file}")
                with open(backup_file, "wb") as f:
                    f.write(content_bytes)
                
                print(f"Creating UTF-8 version: {env_file}")
                with open(env_file, "w", encoding="utf-8") as f:
                    f.write(decoded_content)
                
                print("[OK] File converted to UTF-8")
                return True
    
    return True

if __name__ == "__main__":
    try:
        check_and_fix_env()
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

