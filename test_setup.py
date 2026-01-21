#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'safeboda.settings')

# Setup Django
django.setup()

def test_basic_setup():
    print("Testing basic Django setup...")
    
    # Test database connection
    from django.db import connection
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("[OK] Database connection: OK")
    except Exception as e:
        print(f"[ERROR] Database connection failed: {e}")
        return False
    
    # Test cache configuration (without Redis)
    try:
        from django.core.cache import cache
        print("[OK] Cache configuration loaded: OK")
    except Exception as e:
        print(f"[ERROR] Cache configuration failed: {e}")
        return False
    
    # Test models
    try:
        from users.models import User
        print("[OK] User model imported: OK")
    except Exception as e:
        print(f"[ERROR] User model import failed: {e}")
        return False
    
    # Test views
    try:
        from users.views import UserViewSet
        print("[OK] UserViewSet imported: OK")
    except Exception as e:
        print(f"[ERROR] UserViewSet import failed: {e}")
        return False
    
    print("\n[SUCCESS] Basic setup test completed successfully!")
    print("\nNext steps:")
    print("1. Install Redis server")
    print("2. Run: python manage.py migrate")
    print("3. Run: python manage.py runserver")
    print("4. Test caching with: python test_cache_performance.py")
    
    return True

if __name__ == "__main__":
    test_basic_setup()