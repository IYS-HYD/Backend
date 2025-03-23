import psycopg2

# Database connection parameters
db_params = {
    "dbname": "newdb",
    "user": "nitish",
    "password": "nitishnaik2022@",
    "host": "localhost",
    "port": "5432"
}

try:
    # Connect to PostgreSQL
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()
    cur.execute("SELECT current_schema();")
    print("Connected Schema:", cur.fetchone()[0])
    # Query to count tables in the 'newschema' schema
    cur.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'newschema';
    """)
    tables = cur.fetchall()  # Fetch all table names

    # Print number of tables
    print(f"Number of tables in 'newschema': {len(tables)}")

    # if tables:
    #     print("Tables in 'newschema':")
    #     for table in tables:
    #         table_name = table[0]
    #         print(f"Table Name: {table_name}")
    #         print(table_name)

    #         # Fetch all rows from the table
    #         cur.execute(f"SELECT * FROM newschema.{table_name} LIMIT 5;")  # Limit to 5 for preview
    #         rows = cur.fetchall()

    #         if rows:
    #             for row in rows:
    #                 print(row)
    #         else:
    #             print("No data in this table.")

    # else:
    #     print("No tables found in 'newschema'.")

    def delete(table_name: str):
        cur.execute(f"DELETE FROM  newschema.{table_name}")
        print("Data deleted successfully")
    # Close the connection
    # delete('auth_user') 

    def view(table_name : str):
        cur.execute(f"select count(*) from newschema.{table_name}")
        print("view data")
    view("authenticate_sadhanaentry")
    cur.close()
    conn.close()

except Exception as e:
    print(f"Error: {e}")


