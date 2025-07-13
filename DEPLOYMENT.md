# 🚀 Deployment Guide

## Updating Inventory Data

When you have new inventory data, follow these steps to update the live website:

### 1. Update Local Data

```bash
# Navigate to the project
cd /Users/yujunchen/Documents/goose/inventory_system

# Update the Excel file path in extract_data.py if needed
# Then extract new data to JSON
python3 extract_data.py
```

### 2. Commit and Push Changes

```bash
# Add the updated JSON file
git add inventory_data.json

# Commit with a descriptive message
git commit -m "Update inventory data - $(date '+%Y-%m-%d')"

# Push to GitHub
git push origin main
```

### 3. Automatic Deployment

- GitHub Pages will automatically rebuild and deploy your site
- Changes typically take 1-10 minutes to appear live
- Check the live site: https://steven-scdev.github.io/inventory-system/

## Development Workflow

### Testing Locally

```bash
# Option 1: Use Python's built-in server
python3 -m http.server 8000

# Option 2: Use the Flask app for testing
python3 web_app.py

# Then open: http://localhost:8000 or http://localhost:5000
```

### File Structure

```
inventory_system/
├── index.html              # Main website (GitHub Pages)
├── inventory_data.json     # Static data file
├── web_app.py             # Flask version (for local dev)
├── inventory_manager.py   # Data processing logic
├── extract_data.py        # Data extraction script
├── search_cli.py          # Command line interface
└── README.md              # Documentation
```

## Production URL

Your inventory system is live at:
**https://steven-scdev.github.io/inventory-system/**

## Troubleshooting

### Site Not Loading
- Wait 5-10 minutes after pushing changes
- Check GitHub Actions tab for deployment status
- Ensure index.html is in the root directory

### Data Not Updating
- Verify inventory_data.json was committed and pushed
- Clear browser cache (Ctrl+F5 or Cmd+Shift+R)
- Check browser developer tools for errors

### Performance Issues
- The site loads 1,500+ items instantly
- If slow, check internet connection
- Consider pagination for larger datasets

## Security Notes

- Only commit the JSON data file, not the original Excel files
- The current setup is public - anyone can view inventory data
- For private data, consider:
  - Making the repository private
  - Using authentication
  - Deploying to a private hosting service
