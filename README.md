# ConnVisual

A data visualization tool that connects to and analyzes the specific MySQL database provided in XJTLU IFB107TC coursework, focusing on shipping performance and customer satisfaction through interactive web dashboards.

## Features

- 🔗 MySQL database connection and query execution
- 📊 Static chart generation using matplotlib for line charts and heatmaps
- 🌐 Interactive web visualization with responsive and modern design
- 📤 Data export to JSON format for seamless web consumption

## Project Structure

```
ConnVisual/
├── connector.py              # Core database connection utilities and query execution functions
├── explore_db.py             # Displays table structures and sample data as context for AI
├── visualization.py          # Generates two static matplotlib charts in PNG file
├── export_vis_data.py        # Exports database query results to JSON format for webpage use
├── index.html                # Interactive web dashboard with modern design for enhanced readability
├── config.json               # Database configuration file containing connection credentials (excluded from repo)
├── visualization_data.json   # JSON data file storing relevant analytics data for webpage charts
└── *.png                     # Generated static chart images from visualization.py
```