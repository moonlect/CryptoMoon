"""Application configuration."""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
import os
import sys

# DEBUG: Check .env file encoding
if os.path.exists(".env"):
    print("=" * 80)
    print("DEBUG: Checking .env file")
    print("=" * 80)
    try:
        with open(".env", "rb") as f:
            env_bytes = f.read()
        print(f".env file size: {len(env_bytes)} bytes")
        print(f"First 200 bytes (hex): {env_bytes[:200].hex()}")
        
        # Try to find DATABASE_URL_SYNC line
        for encoding in ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252', 'cp866']:
            try:
                content = env_bytes.decode(encoding)
                if 'DATABASE_URL_SYNC' in content:
                    print(f"Successfully decoded .env as {encoding}")
                    for line in content.split('\n'):
                        if 'DATABASE_URL_SYNC' in line:
                            print(f"Found DATABASE_URL_SYNC line: {line[:80]}...")
                            break
                    break
            except UnicodeDecodeError:
                continue
    except Exception as e:
        print(f"Error reading .env: {e}")
    print("=" * 80)

# DEBUG: Check environment variables
print("\nDEBUG: Environment variables")
print("=" * 80)
db_url_sync_env = os.environ.get("DATABASE_URL_SYNC")
if db_url_sync_env:
    print(f"DATABASE_URL_SYNC from env: type={type(db_url_sync_env)}, length={len(db_url_sync_env)}")
    print(f"First 80 chars: {db_url_sync_env[:80]}...")
    # Check for problematic bytes
    try:
        db_url_sync_env.encode('utf-8')
        print("Environment variable is valid UTF-8")
    except UnicodeEncodeError as e:
        print(f"Environment variable encoding issue: {e}")
else:
    print("DATABASE_URL_SYNC not found in environment variables")
print("=" * 80 + "\n")


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    database_url: str
    database_url_sync: str

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # Security
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 14400  # 24 hours
    refresh_token_expire_days: int = 70

    # CoinMarketCap API
    coinmarketcap_api_key: str = ""

    # Telegram Bot
    telegram_bot_token: str = ""
    telegram_chat_id: str = ""

    # Email (SMTP)
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    smtp_from_email: str = "noreply@cryptotracker.com"

    # Environment
    environment: str = "development"
    debug: bool = True

    # CORS
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    # Rate Limiting
    rate_limit_anonymous: int = 60
    rate_limit_free: int = 300
    rate_limit_vip: int = 1000

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from comma-separated string."""
        if isinstance(self.cors_origins, str):
            return [origin.strip() for origin in self.cors_origins.split(",")]
        return self.cors_origins


settings = Settings()

# DEBUG: Print settings after loading
print("\n" + "=" * 80)
print("DEBUG: Settings loaded")
print("=" * 80)
print(f"database_url_sync type: {type(settings.database_url_sync)}")
print(f"database_url_sync length: {len(settings.database_url_sync)}")
print(f"database_url_sync repr (first 100): {repr(settings.database_url_sync[:100])}")

# Check each character for encoding issues
problematic_chars = []
for i, char in enumerate(settings.database_url_sync):
    try:
        char.encode('utf-8')
    except UnicodeEncodeError:
        problematic_chars.append((i, char, ord(char)))
if problematic_chars:
    print(f"Found {len(problematic_chars)} problematic characters:")
    for pos, char, code in problematic_chars[:10]:  # Show first 10
        print(f"  Position {pos}: {repr(char)} (U+{code:04X})")
else:
    print("No problematic characters found in database_url_sync")

# Try to parse URL components
import urllib.parse
try:
    parsed = urllib.parse.urlparse(settings.database_url_sync)
    print(f"URL parsed successfully:")
    print(f"  scheme: {parsed.scheme}")
    print(f"  username: {parsed.username}")
    print(f"  password: {'***' if parsed.password else 'None'}")
    print(f"  hostname: {parsed.hostname}")
    print(f"  port: {parsed.port}")
    print(f"  path: {parsed.path}")
    
    # Check password encoding
    if parsed.password:
        print(f"  Password type: {type(parsed.password)}")
        print(f"  Password length: {len(parsed.password)}")
        try:
            parsed.password.encode('utf-8')
            print("  Password is valid UTF-8")
        except UnicodeEncodeError as e:
            print(f"  Password encoding issue: {e}")
            # Try to find the problematic byte
            for i, char in enumerate(parsed.password):
                try:
                    char.encode('utf-8')
                except UnicodeEncodeError:
                    print(f"    Problematic char at position {i}: {repr(char)} (U+{ord(char):04X})")
except Exception as e:
    print(f"Error parsing URL: {e}")
    import traceback
    traceback.print_exc()

print("=" * 80 + "\n")



