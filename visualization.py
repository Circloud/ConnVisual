# filepath: d:\Onedrive\XJTLU-Academic\Year 2\IFB107TC\Assessment\Materials\04_Visualization\ConnectionAndVisualization\visualization.py
# Set matplotlib backend to non-interactive to avoid Tkinter issues
import matplotlib
matplotlib.use('Agg')  # Use Agg backend which doesn't require a GUI
import matplotlib.pyplot as plt
import numpy as np
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

def create_shipping_time_vs_rating_chart(data, categories):
    """
    Create a line chart showing the relationship between shipping time and customer rating
    for each product category.
    """
    if not data:
        print("No data available for visualization.")
        return
    
    # Create a dictionary of category names
    category_dict = {cat['product_category_id']: cat['category_name'] for cat in categories}
    
    # Group data by product category
    category_data = {}
    for row in data:
        cat_id = row['product_category_id']
        if cat_id not in category_data:
            category_data[cat_id] = []
        category_data[cat_id].append(row)
    
    # Create the figure and axis
    plt.figure(figsize=(12, 7))
    
    # Colors for different categories
    colors = ['blue', 'green', 'red', 'purple', 'orange']
    
    # Plot a line for each product category
    for i, (cat_id, cat_rows) in enumerate(category_data.items()):
        if cat_id is None:
            continue
            
        # Sort by shipping time
        cat_rows = sorted(cat_rows, key=lambda x: x['shipping_time'])
        
        # Extract shipping times and ratings for this category
        times = [float(row['shipping_time']) for row in cat_rows]
        ratings = [float(row['avg_rating']) for row in cat_rows]
        
        if not times:
            continue
            
        # Plot the line for this category
        color = colors[i % len(colors)]
        category_name = category_dict.get(cat_id, f"Category {cat_id}")
        plt.plot(times, ratings, marker='o', linestyle='-', color=color, 
                 linewidth=2, markersize=6, label=f"{category_name}")
        
        # Add annotations for each data point
        for x, y in zip(times, ratings):
            plt.annotate(f"{y:.2f}", (x, y), textcoords="offset points", 
                        xytext=(0, 7), ha='center', fontsize=8)
    
    # Add labels and title
    plt.xlabel('Shipping Time (days)', fontsize=12)
    plt.ylabel('Average Customer Rating (1-5)', fontsize=12)
    plt.title('Relationship Between Shipping Time and Customer Rating by Product Category', fontsize=14)
    
    # Add grid lines
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Set x-axis ticks
    min_time = min([min(float(row['shipping_time']) for row in data if row['shipping_time'] is not None)])
    max_time = max([max(float(row['shipping_time']) for row in data if row['shipping_time'] is not None)])
    plt.xticks(np.arange(min_time, max_time + 1, 1))
    
    # Add legend
    plt.legend()
    
    # Adjust layout
    plt.tight_layout()
    
    # Save the chart
    plt.savefig('shipping_time_vs_rating.png')
    
    print("Chart saved as 'shipping_time_vs_rating.png'")

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

def create_shipping_time_heatmap(shipping_data, suppliers, weather_conditions):
    """
    Create a heatmap showing average shipping time by supplier and weather condition.
    """
    if not shipping_data:
        print("No data available for heatmap visualization.")
        return
    
    # Create dictionaries for supplier and weather condition names
    supplier_dict = {sup['supplier_id']: sup['supplier_name'] for sup in suppliers}
    weather_dict = {w['weather_condition_id']: w['weather_condition_name'] for w in weather_conditions}
    
    # Create a DataFrame for the heatmap
    # First organize data into a nested dictionary
    data_dict = {}
    for row in shipping_data:
        supplier_id = row['supplier_id']
        weather_id = row['weather_condition_id']
        avg_time = float(row['avg_shipping_time'])
        
        if supplier_id not in data_dict:
            data_dict[supplier_id] = {}
        data_dict[supplier_id][weather_id] = avg_time
    
    # Create arrays for heatmap
    supplier_ids = sorted(list(set([row['supplier_id'] for row in shipping_data if row['supplier_id'] is not None])))
    weather_ids = sorted(list(set([row['weather_condition_id'] for row in shipping_data if row['weather_condition_id'] is not None])))
    
    # Create the data matrix
    matrix = []
    for s_id in supplier_ids:
        row_data = []
        for w_id in weather_ids:
            if s_id in data_dict and w_id in data_dict[s_id]:
                row_data.append(data_dict[s_id][w_id])
            else:
                row_data.append(np.nan)  # Use NaN for missing data
        matrix.append(row_data)
    
    # Convert to numpy array
    matrix = np.array(matrix)
    
    # Create labels
    supplier_labels = [supplier_dict.get(s_id, f"Supplier {s_id}") for s_id in supplier_ids]
    weather_labels = [weather_dict.get(w_id, f"Weather {w_id}") for w_id in weather_ids]
    
    # Create figure and axis
    plt.figure(figsize=(10, 8))
    
    # Create heatmap
    im = plt.imshow(matrix, cmap='YlOrRd')
    
    # Add colorbar
    cbar = plt.colorbar(im)
    cbar.set_label('Average Shipping Time (days)', rotation=270, labelpad=20)
    
    # Add labels and title
    plt.title('Average Shipping Time by Supplier and Weather Condition', fontsize=14)
    plt.xlabel('Weather Condition', fontsize=12)
    plt.ylabel('Supplier', fontsize=12)
    
    # Set ticks and labels
    plt.xticks(np.arange(len(weather_labels)), weather_labels, rotation=45, ha="right")
    plt.yticks(np.arange(len(supplier_labels)), supplier_labels)
      # Add text annotations
    for i in range(len(supplier_ids)):
        for j in range(len(weather_ids)):
            if not np.isnan(matrix[i, j]):
                text = plt.text(j, i, f"{matrix[i, j]:.1f}",
                               ha="center", va="center", color="black")
    
    # Adjust layout
    plt.tight_layout()
    
    # Save the chart
    plt.savefig('shipping_time_heatmap.png')
    
    print("Heatmap saved as 'shipping_time_heatmap.png'")

def main():
    # Load database configuration from config.json
    db_config = load_config()
    
    if not db_config:
        print("Failed to load database configuration.")
        return
    
    # Connect to the database
    connection = connect_to_database(**db_config)
    
    if connection:
        # Fetch category data
        categories = fetch_category_names(connection)
        
        # Fetch shipping and rating data
        data = fetch_shipping_time_and_rating_data_by_category(connection)
        
        # Create visualization
        create_shipping_time_vs_rating_chart(data, categories)
        
        # Fetch supplier and weather data for heatmap
        shipping_data = fetch_shipping_time_by_supplier_and_weather(connection)
        suppliers = fetch_supplier_names(connection)
        weather_conditions = execute_query(connection, "SELECT weather_condition_id, weather_condition_name FROM weather_condition")
        
        # Create heatmap visualization
        create_shipping_time_heatmap(shipping_data, suppliers, weather_conditions)
        
        # Close connection
        connection.close()
        print("Visualization complete!")
    else:
        print("Failed to connect to the database.")

if __name__ == "__main__":
    main()
