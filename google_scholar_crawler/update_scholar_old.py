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

def extract_scholar_stats(scholar_url):
    """Extract Google Scholar statistics using requests with fallback"""
    try:
        print(f"Fetching data from: {scholar_url}")
        
        # Set up headers to mimic a real browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Referer': 'https://scholar.google.com/',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache'
        }
        
        # Try multiple approaches
        session = requests.Session()
        session.headers.update(headers)
        
        # First try: Direct request
        try:
            response = session.get(scholar_url, timeout=30)
            response.raise_for_status()
            print(f"Response status: {response.status_code}")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 403:
                print("Google Scholar blocked the request (403 Forbidden)")
                print("Using fallback data...")
                return create_fallback_stats()
            else:
                raise e
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract citation stats
        stats = {}
        
        # Try to find citation count
        try:
            citation_elements = soup.find_all('td', class_='gsc_rsb_std')
            if citation_elements:
                stats['citations'] = int(citation_elements[0].text.replace(',', ''))
            else:
                stats['citations'] = 0
        except:
            stats['citations'] = 0
            
        # Try to find h-index
        try:
            if len(citation_elements) > 1:
                stats['h_index'] = int(citation_elements[1].text.replace(',', ''))
            else:
                stats['h_index'] = 0
        except:
            stats['h_index'] = 0
            
        # Try to find i10-index
        try:
            if len(citation_elements) > 2:
                stats['i10_index'] = int(citation_elements[2].text.replace(',', ''))
            else:
                stats['i10_index'] = 0
        except:
            stats['i10_index'] = 0
            
        # Add timestamp
        stats['last_updated'] = time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())
        
        print(f"Extracted stats: {stats}")
        return stats
        
    except Exception as e:
        print(f"Error extracting stats: {e}")
        print("Using fallback data...")
        return create_fallback_stats()

def create_fallback_stats():
    """Create fallback stats when scraping fails"""
    stats = {
        'citations': 0,
        'h_index': 0,
        'i10_index': 0,
        'last_updated': time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime()),
        'note': 'Data unavailable - Google Scholar blocking automated requests'
    }
    print(f"Using fallback stats: {stats}")
    return stats

def main():
    """Main function to fetch and save Google Scholar stats"""
    
    # Google Scholar URL from config
    scholar_url = "https://scholar.google.com/citations?hl=en&user=5biMMmIAAAAJ&view_op=list_works"
    
    try:
        print("Fetching Google Scholar data...")
        stats = extract_scholar_stats(scholar_url)
        
        if stats:
            # Create output directory
            os.makedirs("google-scholar-stats", exist_ok=True)
            
            # Save to JSON file
            output_file = "google-scholar-stats/gs_data.json"
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

if __name__ == "__main__":
    main()
