#!/bin/bash
# SGNS Classroom Package - Setup and Verification Script
# Run this to verify everything is installed and working

echo "════════════════════════════════════════════════════════════"
echo "Skip-gram with Negative Sampling - Classroom Package Setup"
echo "════════════════════════════════════════════════════════════"
echo ""

# Check Python version
echo "✓ Checking Python version..."
python --version
echo ""

# Check required packages
echo "✓ Checking required packages..."
packages=("numpy" "matplotlib" "sklearn" "seaborn")
missing=0

for package in "${packages[@]}"; do
    if python -c "import ${package}" 2>/dev/null; then
        echo "  ✓ ${package} is installed"
    else
        echo "  ✗ ${package} is NOT installed"
        missing=1
    fi
done

if [ $missing -eq 1 ]; then
    echo ""
    echo "⚠️  Some packages are missing. Installing..."
    pip install numpy matplotlib scikit-learn seaborn
    echo ""
fi

# Verify files exist
echo "✓ Checking package files..."
files=(
    "sgns.py"
    "sgns_visualization.py"
    "classroom_examples.py"
    "README.md"
    "TEACHING_CHEATSHEET.md"
    "VISUALIZATION_GUIDE.md"
    "ONE_PAGE_SUMMARY.md"
    "INDEX.md"
)

missing_files=0
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✓ $file"
    else
        echo "  ✗ $file (MISSING)"
        missing_files=1
    fi
done

# Test run sgns.py
echo ""
echo "✓ Running test..."
echo "  (This should complete in ~5 seconds)"
python sgns.py > /tmp/sgns_test.log 2>&1
if [ $? -eq 0 ]; then
    echo "  ✓ sgns.py runs successfully!"
else
    echo "  ✗ sgns.py failed to run"
    cat /tmp/sgns_test.log
fi

echo ""
echo "════════════════════════════════════════════════════════════"
if [ $missing_files -eq 0 ] && [ $missing -eq 0 ]; then
    echo "✅ ALL CHECKS PASSED - Ready for classroom!"
else
    echo "⚠️  Some issues detected - see above"
fi
echo "════════════════════════════════════════════════════════════"
echo ""
echo "NEXT STEPS:"
echo "  1. Read INDEX.md for quick start"
echo "  2. Choose teaching approach from README.md"
echo "  3. Run: python sgns_visualization.py (to regenerate images)"
echo "  4. Run: python classroom_examples.py (for interactive demo)"
echo ""
echo "Happy teaching! 🎓"
