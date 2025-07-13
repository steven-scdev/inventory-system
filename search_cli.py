#!/usr/bin/env python3
"""
Command Line Interface for Inventory Management System
Usage: python search_cli.py [command] [arguments]
"""

import sys
import argparse
from inventory_manager import InventoryManager

def format_item_display(item):
    """Format an item for console display."""
    print(f"{'='*60}")
    print(f"SKU: {item['sku']}")
    print(f"Product: {item['product_name']}")
    print(f"Brand: {item['brand']}")
    print(f"Cost: {item['cost']}")
    print(f"Price: {item['price']}")
    print(f"Status: {item['status']}")
    if item['sold_date']:
        print(f"Sold Date: {item['sold_date']}")
    if item['entrupy_cost'] != "N/A":
        print(f"Entrupy Cost: {item['entrupy_cost']}")
    if item['gross_profit'] != "N/A":
        print(f"Gross Profit: {item['gross_profit']}")
    print(f"{'='*60}")

def search_by_sku(inventory, sku):
    """Search for a specific SKU."""
    result = inventory.search_by_sku(sku)
    if result:
        print(f"\nFound item for SKU: {sku}")
        format_item_display(result)
    else:
        print(f"\nNo item found for SKU: {sku}")

def search_by_keyword(inventory, keyword, max_results=10):
    """Search by keyword."""
    results = inventory.search_by_keyword(keyword, max_results)
    if results:
        print(f"\nFound {len(results)} items matching '{keyword}':")
        for i, item in enumerate(results, 1):
            print(f"\n{i}. {item['sku']}: {item['product_name']} ({item['brand']}) - {item['status']}")
        
        # Ask if user wants details
        if len(results) == 1:
            choice = input("\nShow full details? (y/n): ").strip().lower()
            if choice == 'y':
                format_item_display(results[0])
        else:
            choice = input(f"\nShow details for which item? (1-{len(results)}, 'all', or 'none'): ").strip().lower()
            if choice == 'all':
                for item in results:
                    format_item_display(item)
            elif choice.isdigit() and 1 <= int(choice) <= len(results):
                format_item_display(results[int(choice) - 1])
    else:
        print(f"\nNo items found matching '{keyword}'")

def search_by_brand(inventory, brand):
    """Search by brand."""
    results = inventory.search_by_brand(brand)
    if results:
        print(f"\nFound {len(results)} items for brand '{brand}':")
        for i, item in enumerate(results[:20], 1):  # Limit to 20 for display
            print(f"{i}. {item['sku']}: {item['product_name']} - {item['status']}")
        
        if len(results) > 20:
            print(f"... and {len(results) - 20} more items")
            
        choice = input(f"\nShow details for which item? (1-{min(20, len(results))}, or 'none'): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= min(20, len(results)):
            format_item_display(results[int(choice) - 1])
    else:
        print(f"\nNo items found for brand '{brand}'")

def show_summary(inventory):
    """Show inventory summary."""
    summary = inventory.get_inventory_summary()
    print(f"\n{'='*40}")
    print(f"INVENTORY SUMMARY")
    print(f"{'='*40}")
    print(f"Total Items: {summary['total_items']}")
    print(f"Available Items: {summary['available_items']}")
    print(f"Sold Items: {summary['sold_items']}")
    print(f"Number of Brands: {summary['brands']}")
    print(f"Average Cost: ${summary['avg_cost']}")
    print(f"Average Price: ${summary['avg_price']}")
    print(f"\nAvailable Brands:")
    for brand in summary['brand_list']:
        print(f"  - {brand}")

def interactive_mode(inventory):
    """Run interactive mode."""
    print("\n" + "="*50)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("="*50)
    print("Commands:")
    print("  sku [SKU_CODE] - Search by SKU")
    print("  search [KEYWORD] - Search by keyword")
    print("  brand [BRAND_NAME] - Search by brand")
    print("  summary - Show inventory summary")
    print("  brands - List all brands")
    print("  help - Show this help")
    print("  exit - Exit the program")
    print("="*50)
    
    while True:
        try:
            command = input("\nEnter command: ").strip().lower()
            
            if command == 'exit' or command == 'quit':
                print("Goodbye!")
                break
            elif command == 'help':
                print("\nAvailable commands:")
                print("  sku [SKU_CODE] - Search by SKU")
                print("  search [KEYWORD] - Search by keyword")
                print("  brand [BRAND_NAME] - Search by brand")
                print("  summary - Show inventory summary")
                print("  brands - List all brands")
                print("  help - Show this help")
                print("  exit - Exit the program")
            elif command == 'summary':
                show_summary(inventory)
            elif command == 'brands':
                brands = inventory.get_all_brands()
                print(f"\nAvailable brands ({len(brands)}):")
                for brand in brands:
                    print(f"  - {brand}")
            elif command.startswith('sku '):
                sku = command[4:].strip()
                if sku:
                    search_by_sku(inventory, sku)
                else:
                    print("Please provide an SKU code")
            elif command.startswith('search '):
                keyword = command[7:].strip()
                if keyword:
                    search_by_keyword(inventory, keyword)
                else:
                    print("Please provide a search keyword")
            elif command.startswith('brand '):
                brand = command[6:].strip()
                if brand:
                    search_by_brand(inventory, brand)
                else:
                    print("Please provide a brand name")
            else:
                print("Unknown command. Type 'help' for available commands.")
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Inventory Management System")
    parser.add_argument('--file', default="/Users/yujunchen/Documents/Copy of Copy of LBP Updated Inventory Management With Cost-4.xls", help='Excel file path')
    parser.add_argument('--sku', help='Search by SKU')
    parser.add_argument('--search', help='Search by keyword')
    parser.add_argument('--brand', help='Search by brand')
    parser.add_argument('--summary', action='store_true', help='Show inventory summary')
    parser.add_argument('--interactive', action='store_true', help='Run in interactive mode')
    
    args = parser.parse_args()
    
    try:
        print("Loading inventory data...")
        inventory = InventoryManager(args.file)
        print("Data loaded successfully!")
        
        if args.sku:
            search_by_sku(inventory, args.sku)
        elif args.search:
            search_by_keyword(inventory, args.search)
        elif args.brand:
            search_by_brand(inventory, args.brand)
        elif args.summary:
            show_summary(inventory)
        elif args.interactive or len(sys.argv) == 1:
            interactive_mode(inventory)
        else:
            parser.print_help()
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
