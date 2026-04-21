#!/data/data/com.termux/files/usr/bin/bash

echo "📦 Installing hcat..."

# Update package
pkg update -y

# Install dependency
pkg install python -y

# Install python library
pip install rich

# Make executable
chmod +x hcat.py

# Copy ke PATH termux
cp hcat.py $PREFIX/bin/hcat

echo "✅ hcat installed!"
echo "👉 Usage 1: hcat file.py"
echo "👉 Usage 2: hcat py filename"
echo "hcat support lang: python, c++"
echo "<--- UPDATE LOG --->"
echo "Release | 1.0"