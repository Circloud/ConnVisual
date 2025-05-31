from connector import connect_to_database, execute_query, load_config

# Load database configuration from config.json
db_config = load_config()

if not db_config:
    print("Failed to load database configuration.")
    exit(1)

# Connect to the database
connection = connect_to_database(**db_config)

if connection:
    # Get all tables
    tables = execute_query(connection, "SHOW TABLES")
    print("Tables in database:")
    for table in tables:
        table_name = list(table.values())[0]
        print(f"- {table_name}")
        
        # Get table structure
        columns = execute_query(connection, f"DESCRIBE {table_name}")
        print(f"  Columns in {table_name}:")
        for column in columns:
            print(f"    - {column['Field']} ({column['Type']})")
            
        # Show a sample of data
        sample = execute_query(connection, f"SELECT * FROM {table_name} LIMIT 3")
        print(f"  Sample data from {table_name}:")
        for row in sample:
            print(f"    {row}")
        print()
    
    # Close the connection
    connection.close()
    print("Database connection closed.")
else:
    print("Failed to connect to the database.")
