#!/bin/bash

set -e

echo "🚀 Setting up Expense Tracker MCP..."

cd "$HOME/Desktop/MCP/expense_tracker_server"

echo "📦 Installing FastMCP..."
uv add fastmcp

echo "🔄 Syncing environment..."
uv sync

echo "🔍 Testing Python package..."
uv run python -c "import fastmcp; print('FastMCP:', fastmcp.__version__)"

echo ""
echo "✅ Setup complete!"


