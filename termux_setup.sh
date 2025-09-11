#!/data/data/com.termux/files/usr/bin/bash

# Update package repositories
pkg update -y

# Install required packages
pkg install -y python git

# Install pip if not already installed
pkg install -y python-pip

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Make Python scripts executable
chmod +x bot.py
chmod +x modules/*.py

echo "Setup complete! You can now run ./bot.py"
