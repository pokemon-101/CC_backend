#!/usr/bin/env python3
"""
PostgreSQL Setup Script for ChordCircle
Helps migrate from SQLite to PostgreSQL
"""

import os
import sys
import subprocess
import psycopg2
from pathlib import Path

def print_header(title):
    print("\n" + "="*60)
    print(f"  🐘 {title}")
    print("="*60)

def check_postgresql_installed():
    """Check if PostgreSQL is installed"""
    print_header("CHECKING POSTGRESQL INSTALLATION")
    
    try:
        # Try to run psql command
        result = subprocess.run(['psql', '--version'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ PostgreSQL found: {version}")
            return True
        else:
            print("❌ PostgreSQL not found")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ PostgreSQL not installed")
        return False

def install_postgresql_driver():
    """Install PostgreSQL Python driver"""
    print_header("INSTALLING POSTGRESQL DRIVER")
    
    try:
        # Check if already installed
        import psycopg2
        print("✅ psycopg2 already installed")
        return True
    except ImportError:
        print("📦 Installing psycopg2...")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'psycopg2-binary'], check=True)
            print("✅ psycopg2 installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install psycopg2")
            return False

def create_database():
    """Create ChordCircle database"""
    print_header("CREATING DATABASE")
    
    db_name = "chordcircle"
    
    try:
        # Connect to PostgreSQL (default database)
        conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password=input("Enter PostgreSQL password for user 'postgres': ")
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
        if cursor.fetchone():
            print(f"✅ Database '{db_name}' already exists")
        else:
            # Create database
            cursor.execute(f"CREATE DATABASE {db_name}")
            print(f"✅ Database '{db_name}' created successfully")
        
        cursor.close()
        conn.close()
        return True
        
    except psycopg2.Error as e:
        print(f"❌ Database creation failed: {e}")
        return False
    except KeyboardInterrupt:
        print("\n❌ Operation cancelled")
        return False

def update_env_file():
    """Update .env file with PostgreSQL URL"""
    print_header("UPDATING CONFIGURATION")
    
    env_file = Path(".env")
    
    if not env_file.exists():
        print("❌ .env file not found")
        return False
    
    # Read current .env
    with open(env_file, 'r') as f:
        lines = f.readlines()
    
    # Update DATABASE_URL
    new_lines = []
    updated = False
    
    for line in lines:
        if line.startswith('DATABASE_URL='):
            new_lines.append('DATABASE_URL=postgresql://postgres:password@localhost/chordcircle\n')
            updated = True
            print("✅ Updated DATABASE_URL in .env")
        else:
            new_lines.append(line)
    
    if not updated:
        new_lines.append('\n# PostgreSQL Database\n')
        new_lines.append('DATABASE_URL=postgresql://postgres:password@localhost/chordcircle\n')
        print("✅ Added DATABASE_URL to .env")
    
    # Write back to file
    with open(env_file, 'w') as f:
        f.writelines(new_lines)
    
    print("⚠️  Please update the password in DATABASE_URL to match your PostgreSQL password")
    return True

def migrate_data():
    """Migrate existing SQLite data to PostgreSQL"""
    print_header("MIGRATING DATA")
    
    sqlite_file = Path("chordcircle.db")
    
    if not sqlite_file.exists():
        print("ℹ️  No existing SQLite database found - starting fresh")
        return create_tables()
    
    print("📊 Found existing SQLite database")
    migrate = input("Do you want to migrate existing data? (y/N): ").strip().lower()
    
    if migrate == 'y':
        return migrate_sqlite_to_postgresql()
    else:
        return create_tables()

def create_tables():
    """Create tables in PostgreSQL"""
    print("🏗️  Creating database tables...")
    
    try:
        # Import your models to create tables
        sys.path.append(str(Path(__file__).parent))
        from app.core.database import Base, engine
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully")
        return True
        
    except Exception as e:
        print(f"❌ Table creation failed: {e}")
        return False

def migrate_sqlite_to_postgresql():
    """Migrate data from SQLite to PostgreSQL"""
    print("🔄 Migrating data from SQLite to PostgreSQL...")
    
    try:
        import sqlite3
        
        # Connect to SQLite
        sqlite_conn = sqlite3.connect("chordcircle.db")
        sqlite_conn.row_factory = sqlite3.Row
        
        # Connect to PostgreSQL
        pg_conn = psycopg2.connect(
            host="localhost",
            database="chordcircle",
            user="postgres",
            password=input("Enter PostgreSQL password: ")
        )
        
        # Create tables first
        if not create_tables():
            return False
        
        # Migrate users table
        sqlite_cursor = sqlite_conn.cursor()
        pg_cursor = pg_conn.cursor()
        
        # Get users from SQLite
        sqlite_cursor.execute("SELECT * FROM users")
        users = sqlite_cursor.fetchall()
        
        if users:
            print(f"📤 Migrating {len(users)} users...")
            for user in users:
                pg_cursor.execute("""
                    INSERT INTO users (id, email, username, full_name, hashed_password, 
                                     is_active, is_verified, avatar_url, bio, created_at, 
                                     updated_at, last_login)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO NOTHING
                """, tuple(user))
            
            pg_conn.commit()
            print("✅ Users migrated successfully")
        
        # Close connections
        sqlite_conn.close()
        pg_conn.close()
        
        print("✅ Data migration completed")
        return True
        
    except Exception as e:
        print(f"❌ Data migration failed: {e}")
        return False

def test_connection():
    """Test PostgreSQL connection"""
    print_header("TESTING CONNECTION")
    
    try:
        sys.path.append(str(Path(__file__).parent))
        from app.core.database import engine, SessionLocal
        from app.models.user import User
        
        # Test connection
        with engine.connect() as connection:
            print("✅ PostgreSQL connection successful")
        
        # Test session and query
        db = SessionLocal()
        try:
            user_count = db.query(User).count()
            print(f"✅ Database query successful - {user_count} users in database")
        finally:
            db.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False

def show_next_steps():
    """Show what to do next"""
    print_header("SETUP COMPLETE!")
    
    print("🎉 PostgreSQL setup completed successfully!")
    print("\n📋 What was configured:")
    print("   ✅ PostgreSQL driver installed")
    print("   ✅ ChordCircle database created")
    print("   ✅ Database tables created")
    print("   ✅ .env file updated")
    print("   ✅ Connection tested")
    
    print("\n🚀 Next steps:")
    print("   1. Update the password in your .env file:")
    print("      DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost/chordcircle")
    print("   2. Start your backend server:")
    print("      python start.py")
    print("   3. Test the API:")
    print("      http://localhost:8000/docs")
    
    print("\n🌐 Production deployment options:")
    print("   - Heroku Postgres (free tier available)")
    print("   - Railway ($5/month)")
    print("   - Supabase (PostgreSQL + real-time)")
    print("   - AWS RDS (managed PostgreSQL)")
    
    print("\n📚 Benefits you now have:")
    print("   ✅ Better performance for complex queries")
    print("   ✅ JSON support for music API data")
    print("   ✅ Full-text search capabilities")
    print("   ✅ Better scalability")
    print("   ✅ Production-ready database")

def main():
    """Main setup function"""
    print_header("CHORDCIRCLE POSTGRESQL SETUP")
    print("This script will help you migrate from SQLite to PostgreSQL")
    
    # Check if PostgreSQL is installed
    if not check_postgresql_installed():
        print("\n❌ PostgreSQL is not installed!")
        print("\n📥 Please install PostgreSQL first:")
        print("   - Windows: Download from https://www.postgresql.org/download/windows/")
        print("   - macOS: brew install postgresql")
        print("   - Linux: sudo apt-get install postgresql postgresql-contrib")
        return False
    
    # Install Python driver
    if not install_postgresql_driver():
        return False
    
    # Create database
    if not create_database():
        return False
    
    # Update configuration
    if not update_env_file():
        return False
    
    # Migrate data
    if not migrate_data():
        return False
    
    # Test connection
    if not test_connection():
        return False
    
    # Show completion message
    show_next_steps()
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)