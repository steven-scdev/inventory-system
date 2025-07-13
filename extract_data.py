#!/usr/bin/env python3
"""
Extract inventory data to JSON for static website
"""

from inventory_manager import InventoryManager
import json

def main():
    # Load the inventory data
    file_path = "/Users/yujunchen/Documents/Copy of Copy of LBP Updated Inventory Management With Cost-4.xls"
    
    try:
        print("Loading inventory data...")
        inventory = InventoryManager(file_path)
        
        # Get all data
        all_items = []
        brands = inventory.get_all_brands()
        
        for brand in brands:
            brand_items = inventory.search_by_brand(brand)
            all_items.extend(brand_items)
        
        # Get summary
        summary = inventory.get_inventory_summary()
        
        # Create the data structure for the static site
        data = {
            'items': all_items,
            'brands': brands,
            'summary': summary,
            'last_updated': '2024-07-13'
        }
        
        # Save to JSON file
        with open('inventory_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Exported {len(all_items)} items to inventory_data.json")
        print(f"📊 Brands: {len(brands)}")
        print(f"📈 Summary: {summary}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

if __name__ == "__main__":
    main()
