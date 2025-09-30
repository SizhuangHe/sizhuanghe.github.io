#!/usr/bin/env python3
"""
Simple test script to debug GitHub Actions
"""

import os
import sys
import json
from datetime import datetime

def main():
    print("=" * 50)
    print("🎯 TEST SCRIPT STARTING")
    print("=" * 50)
    
    print("🔧 Environment check:")
    print(f"   - GOOGLE_SCHOLAR_ID: {os.environ.get('GOOGLE_SCHOLAR_ID', 'NOT SET')}")
    print(f"   - Python version: {sys.version}")
    print(f"   - Current directory: {os.getcwd()}")
    print(f"   - Python executable: {sys.executable}")
    
    print("📦 Testing imports...")
    try:
        import requests
        print("✅ requests imported")
    except ImportError as e:
        print(f"❌ requests import failed: {e}")
    
    try:
        from bs4 import BeautifulSoup
        print("✅ BeautifulSoup imported")
    except ImportError as e:
        print(f"❌ BeautifulSoup import failed: {e}")
    
    try:
        from scholarly import scholarly
        print("✅ scholarly imported")
    except ImportError as e:
        print(f"❌ scholarly import failed: {e}")
    
    print("🧪 Testing basic functionality...")
    
    # Create test data
    test_data = {
        "name": "Test Author",
        "affiliation": "Test University",
        "email": "test@test.edu",
        "citedby": 100,
        "hindex": 5,
        "i10index": 3,
        "updated": str(datetime.now())
    }
    
    print("💾 Creating results directory...")
    os.makedirs('results', exist_ok=True)
    
    print("📄 Writing test data...")
    with open('results/gs_data.json', 'w', encoding='utf-8') as f:
        json.dump(test_data, f, ensure_ascii=False, indent=2)
    
    print("✅ Test data written successfully")
    
    print("=" * 50)
    print("🎉 TEST SCRIPT COMPLETED")
    print("=" * 50)

if __name__ == "__main__":
    main()
