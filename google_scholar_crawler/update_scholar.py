#!/usr/bin/env python3
"""
Google Scholar Stats Crawler
Fetches citation statistics from Google Scholar profile
"""

import json
import os
import re
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

def setup_driver():
    """Setup Chrome driver with appropriate options"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def extract_scholar_stats(driver, scholar_url):
    """Extract Google Scholar statistics"""
    try:
        print(f"Fetching data from: {scholar_url}")
        driver.get(scholar_url)
        
        # Wait for the page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "gsc_rsb_std"))
        )
        
        # Extract citation stats
        stats = {}
        
        # Try to find citation count
        try:
            citation_element = driver.find_element(By.CSS_SELECTOR, "td.gsc_rsb_std")
            stats['citations'] = int(citation_element.text.replace(',', ''))
        except:
            stats['citations'] = 0
            
        # Try to find h-index
        try:
            h_index_elements = driver.find_elements(By.CSS_SELECTOR, "td.gsc_rsb_std")
            if len(h_index_elements) > 1:
                stats['h_index'] = int(h_index_elements[1].text.replace(',', ''))
            else:
                stats['h_index'] = 0
        except:
            stats['h_index'] = 0
            
        # Try to find i10-index
        try:
            i10_elements = driver.find_elements(By.CSS_SELECTOR, "td.gsc_rsb_std")
            if len(i10_elements) > 2:
                stats['i10_index'] = int(i10_elements[2].text.replace(',', ''))
            else:
                stats['i10_index'] = 0
        except:
            stats['i10_index'] = 0
            
        # Try to find recent citations (last 5 years)
        try:
            recent_citations_element = driver.find_element(By.CSS_SELECTOR, "td.gsc_rsb_std")
            # This might be the recent citations, but Google Scholar layout varies
            stats['recent_citations'] = stats.get('citations', 0)  # Fallback to total citations
        except:
            stats['recent_citations'] = 0
            
        # Add timestamp
        stats['last_updated'] = time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())
        
        print(f"Extracted stats: {stats}")
        return stats
        
    except Exception as e:
        print(f"Error extracting stats: {e}")
        return None

def main():
    """Main function to fetch and save Google Scholar stats"""
    
    # Google Scholar URL from config
    scholar_url = "https://scholar.google.com/citations?hl=en&user=5biMMmIAAAAJ&view_op=list_works&gmla=AH8HC4w9PHnAcAf7bKCdnfwUTP-gOdHizFkhbBTcbl9KMusS_qOEFoZWRrT_ulxjNPXzT3HFQhDPvmDvo4lYUnwC"
    
    driver = None
    try:
        print("Setting up Chrome driver...")
        driver = setup_driver()
        
        print("Fetching Google Scholar data...")
        stats = extract_scholar_stats(driver, scholar_url)
        
        if stats:
            # Create output directory
            os.makedirs("../google-scholar-stats", exist_ok=True)
            
            # Save to JSON file
            output_file = "../google-scholar-stats/gs_data.json"
            with open(output_file, 'w') as f:
                json.dump(stats, f, indent=2)
            
            print(f"Stats saved to {output_file}")
            print(f"Citation count: {stats.get('citations', 'N/A')}")
            print(f"H-index: {stats.get('h_index', 'N/A')}")
            print(f"I10-index: {stats.get('i10_index', 'N/A')}")
        else:
            print("Failed to extract stats")
            
    except Exception as e:
        print(f"Error in main: {e}")
    finally:
        if driver:
            driver.quit()
            print("Driver closed")

if __name__ == "__main__":
    main()
