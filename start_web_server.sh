#!/bin/bash
echo "🛍️ Starting E-commerce Inventory Management System..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

cd "$(dirname "$0")"

echo "📁 Working directory: $(pwd)"
echo "📊 Loading inventory data..."

python3 web_app.py

echo ""
echo "✅ Server stopped. Goodbye!"
