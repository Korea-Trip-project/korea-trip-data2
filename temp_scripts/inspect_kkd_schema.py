import sqlite3

conn = sqlite3.connect("★korea-trip-data/data/kkday_products.db")
cursor = conn.cursor()

# Get list of tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables in kkday_products.db:")
for t in tables:
    t_name = t[0]
    print("\nTable:", t_name)
    # Get column info
    cursor.execute(f"PRAGMA table_info({t_name});")
    columns = cursor.fetchall()
    for col in columns:
        print(f"  Column: {col[1]} ({col[2]})")
        
conn.close()
