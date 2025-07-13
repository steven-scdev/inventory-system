#!/usr/bin/env python3
"""
Web-based Inventory Management System
"""

from flask import Flask, render_template_string, request, jsonify
from inventory_manager import InventoryManager
import json

app = Flask(__name__)

# Global inventory manager
inventory = None

# HTML Template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Inventory Management System</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .header {
            text-align: center;
            color: #333;
            margin-bottom: 30px;
        }
        .search-section {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
        }
        .search-form {
            display: grid;
            grid-template-columns: 1fr 1fr 200px;
            gap: 15px;
            align-items: end;
        }
        .form-group {
            display: flex;
            flex-direction: column;
        }
        label {
            margin-bottom: 5px;
            font-weight: 500;
            color: #555;
        }
        input, select {
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
        }
        button {
            background-color: #007bff;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
            transition: background-color 0.2s;
        }
        button:hover {
            background-color: #0056b3;
        }
        .results {
            margin-top: 20px;
        }
        .item-card {
            background-color: #fff;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 15px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        .item-header {
            display: flex;
            justify-content: between;
            align-items: center;
            margin-bottom: 10px;
        }
        .sku {
            font-weight: bold;
            color: #007bff;
            font-size: 18px;
        }
        .status {
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: bold;
        }
        .status.available {
            background-color: #d4edda;
            color: #155724;
        }
        .status.sold {
            background-color: #f8d7da;
            color: #721c24;
        }
        .item-details {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
        }
        .detail-item {
            display: flex;
            justify-content: space-between;
            padding: 5px 0;
            border-bottom: 1px solid #eee;
        }
        .detail-label {
            font-weight: 500;
            color: #555;
        }
        .summary-stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }
        .stat-number {
            font-size: 2em;
            font-weight: bold;
            color: #007bff;
        }
        .stat-label {
            color: #666;
            margin-top: 5px;
        }
        .loading {
            text-align: center;
            padding: 40px;
            color: #666;
        }
        .error {
            background-color: #f8d7da;
            color: #721c24;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
        }
        @media (max-width: 768px) {
            .search-form {
                grid-template-columns: 1fr;
            }
            .item-details {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛍️ Inventory Management System</h1>
            <p>Search for products by SKU, keyword, or brand</p>
        </div>

        <div id="summary-section" class="summary-stats">
            <!-- Summary stats will be loaded here -->
        </div>

        <div class="search-section">
            <div class="search-form">
                <div class="form-group">
                    <label for="search-input">Search by SKU or Keyword:</label>
                    <input type="text" id="search-input" placeholder="Enter SKU or product name...">
                </div>
                <div class="form-group">
                    <label for="brand-select">Filter by Brand:</label>
                    <select id="brand-select">
                        <option value="">All Brands</option>
                    </select>
                </div>
                <div class="form-group">
                    <button onclick="performSearch()">Search</button>
                </div>
            </div>
        </div>

        <div id="results" class="results">
            <!-- Results will be displayed here -->
        </div>
    </div>

    <script>
        let allBrands = [];

        // Load initial data
        window.onload = function() {
            loadSummary();
            loadBrands();
        };

        async function loadSummary() {
            try {
                const response = await fetch('/api/summary');
                const data = await response.json();
                
                const summaryHTML = `
                    <div class="stat-card">
                        <div class="stat-number">${data.total_items}</div>
                        <div class="stat-label">Total Items</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">${data.available_items}</div>
                        <div class="stat-label">Available</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">${data.sold_items}</div>
                        <div class="stat-label">Sold</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">${data.brands}</div>
                        <div class="stat-label">Brands</div>
                    </div>
                `;
                
                document.getElementById('summary-section').innerHTML = summaryHTML;
            } catch (error) {
                console.error('Error loading summary:', error);
            }
        }

        async function loadBrands() {
            try {
                const response = await fetch('/api/brands');
                const brands = await response.json();
                allBrands = brands;
                
                const select = document.getElementById('brand-select');
                select.innerHTML = '<option value="">All Brands</option>';
                
                brands.forEach(brand => {
                    const option = document.createElement('option');
                    option.value = brand;
                    option.textContent = brand;
                    select.appendChild(option);
                });
            } catch (error) {
                console.error('Error loading brands:', error);
            }
        }

        async function performSearch() {
            const searchInput = document.getElementById('search-input').value.trim();
            const brandFilter = document.getElementById('brand-select').value;
            const resultsDiv = document.getElementById('results');
            
            if (!searchInput && !brandFilter) {
                resultsDiv.innerHTML = '<p class="error">Please enter a search term or select a brand.</p>';
                return;
            }

            resultsDiv.innerHTML = '<div class="loading">Searching...</div>';

            try {
                let url = '/api/search?';
                const params = new URLSearchParams();
                
                if (searchInput) {
                    params.append('query', searchInput);
                }
                if (brandFilter) {
                    params.append('brand', brandFilter);
                }
                
                const response = await fetch(url + params.toString());
                const results = await response.json();
                
                if (results.length === 0) {
                    resultsDiv.innerHTML = '<p>No items found matching your search criteria.</p>';
                    return;
                }

                let html = `<h3>Found ${results.length} item(s):</h3>`;
                
                results.forEach(item => {
                    html += `
                        <div class="item-card">
                            <div class="item-header">
                                <span class="sku">${item.sku}</span>
                                <span class="status ${item.status.toLowerCase()}">${item.status}</span>
                            </div>
                            <h4>${item.product_name}</h4>
                            <div class="item-details">
                                <div class="detail-item">
                                    <span class="detail-label">Brand:</span>
                                    <span>${item.brand}</span>
                                </div>
                                <div class="detail-item">
                                    <span class="detail-label">Cost:</span>
                                    <span>${item.cost}</span>
                                </div>
                                <div class="detail-item">
                                    <span class="detail-label">Price:</span>
                                    <span>${item.price}</span>
                                </div>
                                <div class="detail-item">
                                    <span class="detail-label">Gross Profit:</span>
                                    <span>${item.gross_profit}</span>
                                </div>
                                ${item.sold_date ? `
                                <div class="detail-item">
                                    <span class="detail-label">Sold Date:</span>
                                    <span>${item.sold_date}</span>
                                </div>
                                ` : ''}
                                ${item.entrupy_cost !== 'N/A' ? `
                                <div class="detail-item">
                                    <span class="detail-label">Entrupy Cost:</span>
                                    <span>${item.entrupy_cost}</span>
                                </div>
                                ` : ''}
                            </div>
                        </div>
                    `;
                });
                
                resultsDiv.innerHTML = html;
                
            } catch (error) {
                resultsDiv.innerHTML = '<p class="error">Error searching inventory. Please try again.</p>';
                console.error('Search error:', error);
            }
        }

        // Allow search on Enter key
        document.getElementById('search-input').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                performSearch();
            }
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    """Main page."""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/summary')
def api_summary():
    """Get inventory summary."""
    try:
        summary = inventory.get_inventory_summary()
        return jsonify(summary)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/brands')
def api_brands():
    """Get all brands."""
    try:
        brands = inventory.get_all_brands()
        return jsonify(brands)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search')
def api_search():
    """Search inventory."""
    try:
        query = request.args.get('query', '').strip()
        brand = request.args.get('brand', '').strip()
        
        results = []
        
        if query and brand:
            # Search by keyword and filter by brand
            keyword_results = inventory.search_by_keyword(query, 50)
            results = [item for item in keyword_results if item['brand'].lower() == brand.lower()]
        elif query:
            # Check if it's an exact SKU first
            sku_result = inventory.search_by_sku(query)
            if sku_result:
                results = [sku_result]
            else:
                # Search by keyword
                results = inventory.search_by_keyword(query, 20)
        elif brand:
            # Search by brand only
            results = inventory.search_by_brand(brand)[:20]  # Limit to 20 results
        
        return jsonify(results)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def main():
    """Main function to run the web app."""
    global inventory
    
    file_path = "/Users/yujunchen/Documents/Copy of Copy of LBP Updated Inventory Management With Cost-4.xls"
    
    print("Loading inventory data...")
    try:
        inventory = InventoryManager(file_path)
        print("✅ Data loaded successfully!")
        print(f"📊 Loaded {inventory.get_inventory_summary()['total_items']} items")
        print("\n🌐 Starting web server...")
        print("📱 Open your browser and go to: http://127.0.0.1:5000")
        print("💡 Press Ctrl+C to stop the server")
        
        app.run(debug=True, host='127.0.0.1', port=5000)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

if __name__ == "__main__":
    main()
