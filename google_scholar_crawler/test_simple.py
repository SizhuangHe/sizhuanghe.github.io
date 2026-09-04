#!/usr/bin/env python3
"""
Simple test script to debug GitHub Actions
"""

import os
import sys

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
    
    print("✅ Environment checks completed; no Scholar data files were created.")
    
    print("=" * 50)
    print("🎉 TEST SCRIPT COMPLETED")
    print("=" * 50)

if __name__ == "__main__":
    main()
