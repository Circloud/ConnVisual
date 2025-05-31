import pymysql
import json
import os

def load_config(config_file="config.json"):
    """
    Load database configuration from JSON file.
    """
    try:
        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(script_dir, config_file)
        
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config['database']
    except Exception as e:
        print(f"Error loading configuration: {e}")
        return None

def connect_to_database(host, user, password, database, port=3306):
    try:
        # Establish connection to the MySQL database
        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port,
            cursorclass=pymysql.cursors.DictCursor  # Returns results as dictionaries
        )
        print("Database connection successful!")
        return connection
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def execute_query(connection, query):
    try:
        with connection.cursor() as cursor:
            # Execute the SQL query
            cursor.execute(query)
            # Fetch all results
            result = cursor.fetchall()
            return result
    except Exception as e:
        print(f"Error executing query: {e}")
        return None

if __name__ == "__main__":
    # Load database configuration from JSON file
    db_config = load_config()
    
    if db_config:
        # Example query
        sample_query = "SELECT * FROM order_line LIMIT 5"
        
        # Connect to the database
        connection = connect_to_database(**db_config)
        
        # If connection is successful, execute the query
        if connection:
            # Execute query and get results
            results = execute_query(connection, sample_query)
            
            # Display results
            if results:
                print("\nQuery Results:")
                for row in results:
                    print(row)
            else:
                print("No results found or query error.")
            
            # Always close the connection when finished
            connection.close()
            print("Database connection closed.")
        else:
            print("Failed to connect to the database.")
    else:
        print("Failed to load database configuration.")