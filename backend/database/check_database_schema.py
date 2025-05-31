"""
Script to check the actual structure of your database tables
"""
import sys, os

# Insert the project's root (backend/) into sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from database.database import engine
from sqlalchemy import text, inspect


def check_table_schema():
    """Check the actual columns in each table"""

    tables_to_check = ['departments', 'employees', 'products', 'batches', 'batch_tracking']

    try:
        inspector = inspect(engine)

        for table_name in tables_to_check:
            print(f"\n📋 Table: {table_name}")
            print("-" * 40)

            if inspector.has_table(table_name):
                columns = inspector.get_columns(table_name)
                for col in columns:
                    print(f"  ✓ {col['name']} ({col['type']})")
            else:
                print(f"  ❌ Table {table_name} does not exist")

        return True

    except Exception as e:
        print(f"❌ Error checking schema: {e}")
        return False


def check_with_sql():
    """Alternative method using SQL queries"""

    tables_to_check = ['departments', 'employees', 'products', 'batches', 'batch_tracking']

    try:
        with engine.connect() as connection:
            for table_name in tables_to_check:
                print(f"\n📋 Table: {table_name}")
                print("-" * 40)

                query = text(f"""
                    SELECT column_name, data_type, is_nullable
                    FROM information_schema.columns 
                    WHERE table_name = '{table_name}'
                    ORDER BY ordinal_position;
                """)

                result = connection.execute(query)
                columns = result.fetchall()

                if columns:
                    for col in columns:
                        nullable = "NULL" if col[2] == "YES" else "NOT NULL"
                        print(f"  ✓ {col[0]} ({col[1]}) {nullable}")
                else:
                    print(f"  ❌ No columns found for {table_name}")

        return True

    except Exception as e:
        print(f"❌ Error checking schema with SQL: {e}")
        return False


if __name__ == "__main__":
    print("🔍 Checking Database Schema...")
    print("\nMethod 1: Using SQLAlchemy Inspector")
    check_table_schema()

    print("\n" + "=" * 50)
    print("\nMethod 2: Using SQL Queries")
    check_with_sql()