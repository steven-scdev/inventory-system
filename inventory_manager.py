import pandas as pd
import re
from typing import Optional, List, Dict
from datetime import datetime

class InventoryManager:
    def __init__(self, excel_file_path: str):
        """Initialize the inventory manager with Excel data."""
        self.file_path = excel_file_path
        self.data = None
        self.all_sheets_data = {}
        self.load_data()
    
    def load_data(self):
        """Load data from all sheets in the Excel file."""
        try:
            # Read all sheets
            excel_file = pd.ExcelFile(self.file_path, engine='xlrd')
            
            # Combine all sheet data
            all_data = []
            for sheet_name in excel_file.sheet_names:
                try:
                    df_sheet = pd.read_excel(self.file_path, sheet_name=sheet_name, engine='xlrd')
                    # Add brand/sheet info if not main sheet
                    if sheet_name != 'Copy of Copy of LBP Updated Inv':
                        df_sheet['Brand'] = sheet_name
                    else:
                        df_sheet['Brand'] = 'Mixed'
                    
                    # Store individual sheet data
                    self.all_sheets_data[sheet_name] = df_sheet
                    
                    # Add to combined data if it has SKU column
                    if 'SKU' in df_sheet.columns:
                        all_data.append(df_sheet)
                except Exception as e:
                    print(f"Error reading sheet {sheet_name}: {e}")
            
            # Combine all data
            if all_data:
                self.data = pd.concat(all_data, ignore_index=True)
                self.clean_data()
            else:
                raise Exception("No valid data found")
                
        except Exception as e:
            print(f"Error loading data: {e}")
            raise
    
    def clean_data(self):
        """Clean and standardize the data."""
        if self.data is not None:
            # Remove rows with missing SKU
            self.data = self.data.dropna(subset=['SKU'])
            
            # Clean SKU column - remove extra spaces
            self.data['SKU'] = self.data['SKU'].astype(str).str.strip()
            
            # Standardize column names
            column_mapping = {
                'Bag Name': 'Product_Name',
                'Bag Cost': 'Cost',
                'Bag Price': 'Price',
                'Bag Price ': 'Price',  # Handle extra space
                'Sold Date': 'Sold_Date',
                'Gross Profit': 'Gross_Profit'
            }
            
            for old_col, new_col in column_mapping.items():
                if old_col in self.data.columns:
                    self.data[new_col] = self.data[old_col]
            
            # Convert numeric columns
            numeric_columns = ['Cost', 'Price', 'Entrupy', 'Gross_Profit']
            for col in numeric_columns:
                if col in self.data.columns:
                    self.data[col] = pd.to_numeric(self.data[col], errors='coerce')
            
            # Create search-friendly product name
            if 'Product_Name' in self.data.columns:
                self.data['Product_Name_Lower'] = self.data['Product_Name'].astype(str).str.lower()
            
            print(f"Data loaded successfully: {len(self.data)} records from {len(self.all_sheets_data)} sheets")
    
    def search_by_sku(self, sku: str) -> Optional[Dict]:
        """Search for a specific SKU."""
        sku = str(sku).strip().upper()
        
        # Search in main data
        matches = self.data[self.data['SKU'].str.upper() == sku]
        
        if matches.empty:
            return None
        
        # Return the first match as a dictionary
        result = matches.iloc[0].to_dict()
        
        # Clean up the result
        return self._format_result(result)
    
    def search_by_keyword(self, keyword: str, max_results: int = 10) -> List[Dict]:
        """Search for products by keyword in product name or SKU."""
        keyword = keyword.lower().strip()
        
        if not keyword:
            return []
        
        # Search in SKU and Product Name
        sku_matches = self.data[self.data['SKU'].str.lower().str.contains(keyword, na=False)]
        name_matches = self.data[self.data['Product_Name_Lower'].str.contains(keyword, na=False, regex=False)]
        
        # Combine and remove duplicates
        all_matches = pd.concat([sku_matches, name_matches]).drop_duplicates()
        
        # Limit results
        results = []
        for _, row in all_matches.head(max_results).iterrows():
            results.append(self._format_result(row.to_dict()))
        
        return results
    
    def search_by_brand(self, brand: str) -> List[Dict]:
        """Search for products by brand."""
        brand_matches = self.data[self.data['Brand'].str.lower().str.contains(brand.lower(), na=False)]
        
        results = []
        for _, row in brand_matches.iterrows():
            results.append(self._format_result(row.to_dict()))
        
        return results
    
    def get_all_brands(self) -> List[str]:
        """Get all available brands."""
        return sorted(self.data['Brand'].unique().tolist())
    
    def get_inventory_summary(self) -> Dict:
        """Get summary statistics of the inventory."""
        total_items = len(self.data)
        brands = self.data['Brand'].nunique()
        
        # Cost and price statistics
        avg_cost = self.data['Cost'].mean()
        avg_price = self.data['Price'].mean()
        
        # Sold items
        sold_items = len(self.data[self.data['Sold_Date'].notna()])
        available_items = total_items - sold_items
        
        return {
            'total_items': total_items,
            'brands': brands,
            'available_items': available_items,
            'sold_items': sold_items,
            'avg_cost': round(avg_cost, 2) if pd.notna(avg_cost) else 0,
            'avg_price': round(avg_price, 2) if pd.notna(avg_price) else 0,
            'brand_list': self.get_all_brands()
        }
    
    def _format_result(self, result: Dict) -> Dict:
        """Format a single result for display."""
        formatted = {}
        
        # Core fields
        formatted['sku'] = result.get('SKU', 'N/A')
        formatted['product_name'] = result.get('Product_Name', 'N/A')
        formatted['brand'] = result.get('Brand', 'N/A')
        
        # Financial info
        formatted['cost'] = self._format_currency(result.get('Cost'))
        formatted['price'] = self._format_currency(result.get('Price'))
        formatted['entrupy_cost'] = self._format_currency(result.get('Entrupy'))
        formatted['gross_profit'] = self._format_currency(result.get('Gross_Profit'))
        
        # Status
        sold_date = result.get('Sold_Date')
        if pd.notna(sold_date) and sold_date is not None:
            formatted['status'] = 'SOLD'
            formatted['sold_date'] = sold_date.strftime('%Y-%m-%d') if hasattr(sold_date, 'strftime') else str(sold_date)
        else:
            formatted['status'] = 'AVAILABLE'
            formatted['sold_date'] = None
        
        return formatted
    
    def _format_currency(self, value) -> str:
        """Format currency values."""
        if pd.isna(value) or value is None:
            return "N/A"
        try:
            return f"${float(value):,.2f}"
        except (ValueError, TypeError):
            return str(value)

# Example usage and testing
if __name__ == "__main__":
    # Test the inventory manager
    file_path = "/Users/yujunchen/Documents/Copy of Copy of LBP Updated Inventory Management With Cost-4.xls"
    
    try:
        inventory = InventoryManager(file_path)
        
        # Test search by SKU
        result = inventory.search_by_sku("LV01")
        print("Search by SKU 'LV01':")
        print(result)
        
        # Test keyword search
        results = inventory.search_by_keyword("wallet", 5)
        print(f"\nSearch by keyword 'wallet' (showing {len(results)} results):")
        for item in results:
            print(f"- {item['sku']}: {item['product_name']}")
        
        # Test summary
        summary = inventory.get_inventory_summary()
        print(f"\nInventory Summary:")
        print(f"Total items: {summary['total_items']}")
        print(f"Brands: {summary['brands']}")
        print(f"Available: {summary['available_items']}")
        print(f"Sold: {summary['sold_items']}")
        
    except Exception as e:
        print(f"Error: {e}")
