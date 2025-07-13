# 🛍️ Luxury Bag Inventory Management System

A web-based inventory management system for luxury bags and accessories. Search through your inventory by SKU, keyword, or brand with a beautiful, responsive interface.

## 🌐 Live Demo

**[View Live Site](https://yourusername.github.io/inventory-system/)**

## ✨ Features

- **🔍 Smart Search**: Find items by exact SKU code or keyword search
- **🏷️ Brand Filtering**: Filter by specific luxury brands (Chanel, Gucci, Louis Vuitton, etc.)
- **📊 Status Tracking**: See if items are available or sold
- **💰 Financial Data**: View costs, prices, and profit margins
- **📱 Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **⚡ Fast Performance**: Static website loads instantly
- **📈 Dashboard Analytics**: Overview of inventory statistics

## Quick Start

### 1. Web Interface (Recommended for Teams)

```bash
cd /Users/yujunchen/Documents/goose/inventory_system
python3 web_app.py
```

Then open your browser to: http://127.0.0.1:5000

### 2. Command Line Interface

```bash
cd /Users/yujunchen/Documents/goose/inventory_system

# Interactive mode
python3 search_cli.py

# Direct searches
python3 search_cli.py --sku LV01
python3 search_cli.py --search "wallet"
python3 search_cli.py --brand "Chanel"
python3 search_cli.py --summary
```

### 3. Python Integration

```python
from inventory_manager import InventoryManager

# Load your data
inventory = InventoryManager("path/to/your/excel/file.xls")

# Search by SKU
item = inventory.search_by_sku("LV01")

# Search by keyword
items = inventory.search_by_keyword("wallet", max_results=10)

# Get summary
summary = inventory.get_inventory_summary()
```

## Data Structure

The system reads from your Excel file with these columns:
- **SKU**: Unique product identifier
- **Bag Name**: Product name/description
- **Bag Cost**: Product cost
- **Bag Price**: Selling price
- **Entrupy**: Authentication cost
- **Gross Profit**: Calculated profit
- **Sold Date**: Date of sale (if sold)
- **Brand**: Product brand (from sheet names)

## Search Examples

### Web Interface
- Search "LV01" → Find exact SKU
- Search "wallet chanel" → Find Chanel wallets
- Filter by "Gucci" brand → Show all Gucci items

### Command Line
```bash
# Find specific item
python3 search_cli.py --sku LV01

# Find all wallets
python3 search_cli.py --search wallet

# Find all Chanel items
python3 search_cli.py --brand Chanel

# Show inventory statistics
python3 search_cli.py --summary
```

## Team Usage Tips

1. **For Customer Service**: Use web interface for quick SKU lookups
2. **For Inventory Management**: Use command line for batch operations
3. **For Reporting**: Use Python integration for custom reports
4. **For Mobile**: Web interface works on phones/tablets

## Data Updates

To update with new inventory data:
1. Replace the Excel file with your updated version
2. Restart the web server or reload the CLI
3. The system automatically reads all sheets and combines the data

## System Requirements

- Python 3.7+
- pandas
- openpyxl
- xlrd
- flask (for web interface)

## File Locations

- Main system: `/Users/yujunchen/Documents/goose/inventory_system/`
- Excel data: `/Users/yujunchen/Documents/Copy of Copy of LBP Updated Inventory Management With Cost-4.xls`
- Web interface: `web_app.py`
- Command line: `search_cli.py`
- Core logic: `inventory_manager.py`
