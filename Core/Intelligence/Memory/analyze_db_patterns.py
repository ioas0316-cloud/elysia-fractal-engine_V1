import sqlite3
import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def analyze_patterns():
    db_path = "data/Memory/memory.db"
    if not os.path.exists(db_path):
        print(f"❌ Error: {db_path} not found!")
        return

    print(f"🔍 Analyzing {db_path}...")
    
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            # Get all tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            print(f"\n📊 Found {len(tables)} tables:")
            
            total_rows = 0
            for table_name in tables:
                table = table_name[0]
                try:
                    cursor.execute(f"SELECT count(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    print(f"   - {table}: {count} rows")
                    total_rows += count
                except sqlite3.OperationalError as e:
                    print(f"   - {table}: Error ({e})")
            
            print(f"\nTotal Rows across all tables: {total_rows}")
            
            # Check file size
            size_mb = os.path.getsize(db_path) / (1024 * 1024)
            print(f"\n💾 Physical File Size: {size_mb:.2f} MB")
            
    except Exception as e:
        print(f"❌ Database Error: {e}")

if __name__ == "__main__":
    analyze_patterns()
