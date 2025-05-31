import json
from connector import connect_to_database, execute_query, load_config

def fetch_shipping_time_and_rating_data_by_category(connection):
    """
    Fetch shipping time and corresponding customer rating data from the database,
    separated by product category.
    """
    query = """
    SELECT s.shipping_time, ol.product_category_id, AVG(ol.customer_rating) as avg_rating
    FROM shipping s
    JOIN order_line ol ON s.shipping_id = ol.shipping_id
    GROUP BY s.shipping_time, ol.product_category_id
    ORDER BY ol.product_category_id, s.shipping_time
    """
    
    return execute_query(connection, query)

def fetch_category_names(connection):
    """
    Fetch product category names
    """
    query = "SELECT product_category_id, category_name FROM product_category"
    return execute_query(connection, query)

def fetch_shipping_time_by_supplier_and_weather(connection):
    """
    Fetch average shipping time data grouped by supplier and weather condition.
    """
    query = """
    SELECT s.supplier_id, w.weather_condition_id, w.weather_condition_name, 
           AVG(s.shipping_time) as avg_shipping_time
    FROM shipping s
    JOIN weather_condition w ON s.weather_condition_id = w.weather_condition_id
    GROUP BY s.supplier_id, w.weather_condition_id
    ORDER BY s.supplier_id, s.weather_condition_id
    """
    
    return execute_query(connection, query)

def fetch_supplier_names(connection):
    """
    Fetch supplier names
    """
    query = "SELECT supplier_id, supplier_name FROM supplier"
    return execute_query(connection, query)

def convert_to_serializable(data):
    """
    Convert data to JSON serializable format.
    This handles specific data types that are not JSON serializable by default.
    """
    if isinstance(data, list):
        return [convert_to_serializable(item) for item in data]
    elif isinstance(data, dict):
        return {key: convert_to_serializable(value) for key, value in data.items()}
    elif hasattr(data, 'isoformat'):  # For datetime objects
        return data.isoformat()
    elif hasattr(data, 'decode'):  # For bytes objects
        try:
            return data.decode('utf-8')
        except:
            return str(data)
    # Handle Decimal objects
    elif hasattr(data, 'as_tuple') and hasattr(data, 'quantize'):  # For Decimal objects
        return float(data)
    else:
        return data

def main():
    # Load database configuration from config.json
    db_config = load_config()
    
    if not db_config:
        print("Failed to load database configuration.")
        return
    
    # Connect to the database
    connection = connect_to_database(**db_config)
    
    if connection:
        # Initialize a dictionary to store all data
        all_data = {}
        
        # Fetch and store data for shipping time vs rating chart
        print("Fetching data for shipping time vs rating chart...")
        all_data['categories'] = convert_to_serializable(fetch_category_names(connection))
        all_data['shipping_time_rating_data'] = convert_to_serializable(
            fetch_shipping_time_and_rating_data_by_category(connection)
        )
        
        # Fetch and store data for shipping time heatmap
        print("Fetching data for shipping time heatmap...")
        all_data['suppliers'] = convert_to_serializable(fetch_supplier_names(connection))
        all_data['weather_conditions'] = convert_to_serializable(
            execute_query(connection, "SELECT weather_condition_id, weather_condition_name FROM weather_condition")
        )
        all_data['shipping_time_by_supplier_weather'] = convert_to_serializable(
            fetch_shipping_time_by_supplier_and_weather(connection)
        )
        
        # Close connection
        connection.close()
        
        # Save data to JSON file
        with open('visualization_data.json', 'w') as f:
            json.dump(all_data, f, indent=4)
        
        print("Data successfully exported to 'visualization_data.json'")
        print("The JSON file contains all data needed for both charts:")
        print("1. Shipping Time vs Rating Chart")
        print("   - Categories")
        print("   - Shipping time and rating data by category")
        print("2. Shipping Time Heatmap")
        print("   - Suppliers")
        print("   - Weather conditions")
        print("   - Shipping time data by supplier and weather")
    else:
        print("Failed to connect to the database.")

if __name__ == "__main__":
    main()
