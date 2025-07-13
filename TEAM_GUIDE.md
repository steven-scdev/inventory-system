# Team Guide: Inventory Management System

## 🎯 Quick Reference for Team Members

### For Customer Service & Sales Team

#### **Web Interface (Easiest)**
1. Double-click `start_web_server.sh` or run it from terminal
2. Open browser to: http://127.0.0.1:5000
3. Use the search box to find items by:
   - **SKU**: Type exact code like "LV01"
   - **Product Name**: Type keywords like "wallet" or "bag"
   - **Brand Filter**: Select brand from dropdown

#### **Common Search Scenarios**
- Customer asks about SKU "CH123" → Type "CH123" in search box
- Customer wants "Chanel wallet" → Type "wallet" and select "Chanel" brand
- Check if item is available → Look for green "AVAILABLE" or red "SOLD" status

### For Inventory Managers

#### **Command Line (More Powerful)**
```bash
# Open terminal and navigate to system folder
cd /Users/yujunchen/Documents/goose/inventory_system

# Start interactive mode
python3 search_cli.py

# In interactive mode, use these commands:
sku LV01              # Find specific SKU
search wallet         # Find all wallets
brand Chanel          # Show all Chanel items
summary              # Show inventory stats
brands               # List all brands
help                 # Show all commands
exit                 # Quit
```

## 📋 What Information You'll See

For each item, the system shows:
- **SKU**: Unique product code
- **Product Name**: Full item description
- **Brand**: Manufacturer/designer
- **Cost**: What we paid for it
- **Price**: What we sell it for
- **Status**: AVAILABLE or SOLD
- **Sold Date**: When it was sold (if applicable)
- **Gross Profit**: Profit margin
- **Entrupy Cost**: Authentication fee

## 🔍 Search Tips

### Best Practices
1. **For exact matches**: Use the complete SKU
2. **For browsing**: Use keywords like "wallet", "bag", "clutch"
3. **For brand search**: Use the brand filter or type brand name
4. **Case doesn't matter**: "lv01" works the same as "LV01"

### Search Examples
| What Customer Wants | How to Search |
|-------------------|---------------|
| "Do you have SKU LV01?" | Type: `LV01` |
| "Any Chanel wallets?" | Type: `wallet` + Brand: `Chanel` |
| "What Gucci bags do you have?" | Brand: `Gucci` |
| "Any black bags?" | Type: `black` |
| "Items under $500?" | Search then filter results manually |

## 🚨 Troubleshooting

### If Web Interface Won't Start
1. Check if Python is installed: `python3 --version`
2. Install missing packages: `pip install flask pandas openpyxl xlrd`
3. Make sure Excel file path is correct in `web_app.py`

### If Data Seems Wrong
1. Check the Excel file date - make sure it's the latest
2. Restart the web server to reload data
3. Contact IT if data is still incorrect

### If Search Returns No Results
1. Try simpler keywords
2. Check spelling
3. Try searching without brand filter first
4. Use the summary command to see what data is available

## 🔧 For System Updates

### When You Get New Inventory Data
1. Stop the web server (Ctrl+C)
2. Replace the Excel file with the new one
3. Update the file path in `web_app.py` if filename changed
4. Restart the web server

### Adding New Team Members
1. Share the folder: `/Users/yujunchen/Documents/goose/inventory_system/`
2. Make sure they have Python installed
3. Show them this guide
4. Test with a few sample searches

## 📞 Support

### Quick Help
- Type `help` in the command line interface
- Check the README.md file for technical details
- All code is documented and customizable

### For Technical Issues
- Check the console for error messages
- Verify Excel file exists and isn't corrupted
- Ensure all Python packages are installed
- Contact the person who set up the system

## 📈 System Stats

The system currently handles:
- **1,598 total items** across 19 brands
- **459 available items** and 1,139 sold items
- **Real-time search** through all data
- **Multiple sheets** automatically combined
- **Cross-platform** compatibility (Mac, Windows, Linux)

---

*Last updated: July 2025*
*System location: `/Users/yujunchen/Documents/goose/inventory_system/`*
