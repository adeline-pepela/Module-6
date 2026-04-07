#!/bin/bash

echo "🐳 Testing Docker Deployment..."
echo ""

# Check Docker files exist
echo "1️⃣ Checking Docker files..."
files=("Dockerfile" "docker-compose.yml" ".dockerignore" "docker-entrypoint.sh")
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "   ✓ $file"
    else
        echo "   ✗ $file missing"
        exit 1
    fi
done

echo ""
echo "2️⃣ Validating docker-compose.yml..."
docker-compose config > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "   ✓ docker-compose.yml is valid"
else
    echo "   ✗ docker-compose.yml has errors"
    exit 1
fi

echo ""
echo "3️⃣ Checking required files..."
if [ -f "../models/best_model.pkl" ]; then
    size=$(ls -lh ../models/best_model.pkl | awk '{print $5}')
    echo "   ✓ Model file exists ($size)"
else
    echo "   ✗ Model file missing"
    exit 1
fi

if [ -f "requirements.txt" ]; then
    count=$(wc -l < requirements.txt)
    echo "   ✓ requirements.txt exists ($count packages)"
else
    echo "   ✗ requirements.txt missing"
    exit 1
fi

echo ""
echo "✅ All checks passed! Ready to deploy."
echo ""
echo "To deploy, run:"
echo "  docker-compose up -d"
echo ""
echo "To view logs:"
echo "  docker-compose logs -f"
echo ""
echo "To stop:"
echo "  docker-compose down"
