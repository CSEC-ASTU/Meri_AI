"""
Diagnostic script to check connectivity and configuration
"""
import socket
import sys
from config import settings

print("\n=== ASTU Route AI - Diagnostics ===\n")

# Check DNS resolution
print("1. Testing DNS resolution...")
try:
    host = "db.pmazbsnglsbgaskxldpy.supabase.co"
    ip = socket.gethostbyname(host)
    print(f"   ✓ {host} -> {ip}")
except socket.gaierror as e:
    print(f"   ✗ DNS resolution failed: {e}")
    print("   → Check: Internet connection, firewall, Supabase project URL")

# Check database URL format
print("\n2. Checking DATABASE_URL format...")
db_url = settings.database_url
if db_url.startswith("postgresql://"):
    print(f"   ✓ Valid Postgres URL format")
    # Parse components
    parts = db_url.replace("postgresql://", "").split("@")
    if len(parts) == 2:
        creds, host_db = parts
        user, pwd = creds.split(":")
        print(f"   - User: {user}")
        print(f"   - Host: {host_db.split(':')[0]}")
else:
    print(f"   ✗ Invalid URL format")

# Check Supabase config
print("\n3. Checking Supabase configuration...")
if settings.supabase_url:
    print(f"   ✓ SUPABASE_URL: {settings.supabase_url}")
else:
    print(f"   ✗ SUPABASE_URL: Not set")

if settings.supabase_service_role_key and "YOUR" not in settings.supabase_service_role_key:
    print(f"   ✓ SUPABASE_SERVICE_ROLE_KEY: Configured (first 20 chars: {settings.supabase_service_role_key[:20]}...)")
else:
    print(f"   ✗ SUPABASE_SERVICE_ROLE_KEY: Not set or placeholder")

# Check AI config
print("\n4. Checking AI configuration...")
if settings.ai_api_key and "YOUR" not in settings.ai_api_key:
    print(f"   ✓ AI_API_KEY: Configured")
    print(f"   ✓ AI_MODEL: {settings.ai_model}")
    print(f"   ✓ EMBEDDING_MODEL: {settings.embedding_model}")
else:
    print(f"   ✗ AI_API_KEY: Not set or placeholder")

print("\n=== Summary ===")
print("Next steps:")
print("1. Ensure you're connected to internet (or VPN if required)")
print("2. Verify Supabase project URL in .env is correct")
print("3. Confirm DATABASE_URL credentials are valid")
print("4. Get SUPABASE_SERVICE_ROLE_KEY from Supabase dashboard (Settings > API)")
print("\nOnce DNS resolves, database.py will:")
print("  - Enable pgvector extension")
print("  - Create pois and documents tables")
print("  - Set up vector indexes")
print("")
