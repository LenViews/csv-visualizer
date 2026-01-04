#!/bin/bash

echo "========================================="
echo "CSV Visualizer - Setup Script"
echo "========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "✓ Python $python_version detected"

# Create directory structure
echo ""
echo "📁 Creating directory structure..."
mkdir -p app
mkdir -p tests
mkdir -p examples
mkdir -p data

# Create virtual environment
echo ""
echo "🐍 Creating virtual environment..."
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "❌ Failed to create virtual environment"
    echo "You might need to install python3-venv:"
    echo "  Ubuntu/Debian: sudo apt install python3-venv"
    echo "  macOS: brew install python3"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "❌ requirements.txt not found"
    exit 1
fi

# Make the script executable
echo ""
echo "🔧 Making scripts executable..."
chmod +x app/visualize_data.py 2>/dev/null || true
chmod +x tests/test_visualize_data.py 2>/dev/null || true
chmod +x examples/example_usage.py 2>/dev/null || true
chmod +x setup.sh 2>/dev/null || true

# Create test data if it doesn't exist
echo ""
echo "📊 Creating sample data files..."
if [ ! -f "data/sample.csv" ]; then
    cat > data/sample.csv << 'EOF'
id,age,salary,experience,department,performance
1,25,50000,2,Engineering,0.85
2,30,55000,5,Marketing,0.92
3,35,60000,8,Engineering,0.88
4,28,52000,3,HR,0.79
5,40,70000,12,Engineering,0.95
6,22,45000,1,Marketing,0.81
7,45,80000,15,Engineering,0.97
8,32,58000,6,HR,0.84
9,29,53000,4,Marketing,0.87
10,38,65000,10,Engineering,0.91
11,27,51000,2,Sales,0.83
12,33,62000,7,Engineering,0.89
13,31,59000,5,Marketing,0.90
14,26,49000,1,HR,0.78
15,42,75000,13,Engineering,0.96
16,24,47000,2,Marketing,0.80
17,37,68000,9,Engineering,0.93
18,34,63000,7,Sales,0.88
19,36,66000,8,Engineering,0.94
20,41,72000,11,Marketing,0.91
EOF
    echo "✓ Created data/sample.csv"
fi

if [ ! -f "data/sales_data.csv" ]; then
    cat > data/sales_data.csv << 'EOF'
month,revenue,profit,customers,avg_order,cost_of_goods,margin
Jan-2023,150000,30000,1200,125.00,120000,0.20
Feb-2023,165000,35000,1350,122.22,130000,0.21
Mar-2023,142000,28000,1150,123.48,114000,0.20
Apr-2023,178000,40000,1450,122.76,138000,0.22
May-2023,190000,45000,1550,122.58,145000,0.24
Jun-2023,205000,50000,1650,124.24,155000,0.24
Jul-2023,198000,48000,1600,123.75,150000,0.24
Aug-2023,185000,42000,1500,123.33,143000,0.23
Sep-2023,172000,38000,1400,122.86,134000,0.22
Oct-2023,210000,52000,1700,123.53,158000,0.25
Nov-2023,225000,58000,1800,125.00,167000,0.26
Dec-2023,240000,62000,1900,126.32,178000,0.26
Jan-2024,155000,31000,1250,124.00,124000,0.20
Feb-2024,170000,37000,1380,123.19,133000,0.22
Mar-2024,148000,29000,1180,125.42,119000,0.20
Apr-2024,182000,41000,1480,122.97,141000,0.23
May-2024,195000,46000,1580,123.42,149000,0.24
Jun-2024,210000,52000,1680,125.00,158000,0.25
Jul-2024,202000,49000,1620,124.69,153000,0.24
Aug-2024,188000,43000,1520,123.68,145000,0.23
Sep-2024,175000,39000,1420,123.24,136000,0.22
Oct-2024,215000,54000,1720,125.00,161000,0.25
Nov-2024,230000,60000,1820,126.37,170000,0.26
Dec-2024,245000,64000,1920,127.60,181000,0.26
EOF
    echo "✓ Created data/sales_data.csv"
fi

# Create .gitignore if it doesn't exist
if [ ! -f ".gitignore" ]; then
    cat > .gitignore << 'EOF'
# Virtual environment
venv/
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# IDE files
.vscode/
.idea/
*.swp
*.swo

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Test files
.pytest_cache/
.coverage
htmlcov/
.tox/

# OS files
.DS_Store
Thumbs.db

# Data files
*.csv
*.json
*.html
!data/sample.csv
!data/sales_data.csv

# Logs
logs/
*.log
EOF
    echo "✓ Created .gitignore"
fi

# Run a quick test
echo ""
echo "🧪 Running quick test..."
cd tests && python -m pytest test_visualize_data.py -xvs -k "test_load_simple_csv" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ Quick test passed!"
else
    echo "⚠️  Quick test failed or skipped"
fi

cd ..

echo ""
echo "========================================="
echo "✅ Setup complete!"
echo "========================================="
echo ""
echo "📋 Next steps:"
echo "1. Activate the virtual environment:"
echo "   $ source venv/bin/activate"
echo ""
echo "2. Run the visualizer:"
echo "   $ python app/visualize_data.py data/sample.csv"
echo ""
echo "3. Run examples:"
echo "   $ python examples/example_usage.py"
echo ""
echo "4. Run tests:"
echo "   $ python -m pytest tests/ -v"
echo ""
echo "5. For help:"
echo "   $ python app/visualize_data.py --help"
echo ""
echo "========================================="