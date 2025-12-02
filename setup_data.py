#!/usr/bin/env python3
"""
Script to setup data for the terrorism analysis app.
Downloads and extracts the data file if not present.
"""

import os
import zipfile
from pathlib import Path

def setup_data():
    """Extract data file from zip if it doesn't exist."""
    data_file = "globalterrorismdb_0522dist.xlsx"
    zip_file = "globalterrorismdb_0522dist.zip"
    
    # Check if data file already exists
    if os.path.exists(data_file):
        print(f"✅ Data file {data_file} already exists")
        return True
    
    # Check if zip file exists
    if not os.path.exists(zip_file):
        print(f"❌ Zip file {zip_file} not found")
        return False
    
    # Extract the zip file
    try:
        print(f"📦 Extracting {zip_file}...")
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall('.')
        print(f"✅ Successfully extracted {data_file}")
        return True
    except Exception as e:
        print(f"❌ Error extracting zip file: {e}")
        return False

if __name__ == "__main__":
    setup_data()