#!/bin/bash

# 1. Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python3 is not installed. Please install it first."
    exit
fi

# 2. Create a virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# 3. Activate the virtual environment (Windows path)
echo "Activating virtual environment..."
source venv/Scripts/activate

# 4. Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# 5. Install required Python packages
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
else
    echo "No requirements.txt file found. Skipping package installation."
fi

# 6. Deactivate virtual environment
echo "You can deactivate the virtual environment manually when done."
