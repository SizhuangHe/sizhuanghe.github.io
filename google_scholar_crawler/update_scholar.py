#!/usr/bin/env python3
"""
Google Scholar Data Updater
Fetches real-time publication and citation data from Google Scholar
"""

import json
import os
import sys
from datetime import datetime
import time
import random
from scholarly import scholarly
import requests
from bs4 import BeautifulSoup

def fetch_google_scholar_data(scholar_id="5biMMmIAAAAJ"):
    """Fetch data from Google Scholar using scholarly library"""
    try:
        # Search for the author
        author = scholarly.search_author_id(scholar_id)
        author = scholarly.fill(author, sections=['basics', 'indices', 'counts', 'publications'])
        
        # Extract basic information
        data = {
            "name": author.get('name', 'Sizhuang He'),
            "affiliation": author.get('affiliation', 'Yale University'),
            "email": author.get('email', 'sizhuang.he@yale.edu'),
            "citedby": author.get('citedby', 0),
            "citedby5y": author.get('citedby5y', 0),
            "hindex": author.get('hindex', 0),
            "hindex5y": author.get('hindex5y', 0),
            "i10index": author.get('i10index', 0),
            "i10index5y": author.get('i10index5y', 0),
            "updated": str(datetime.now()),
            "publications": {}
        }
        
        # Extract publications
        for i, pub in enumerate(author.get('publications', [])):
            pub_filled = scholarly.fill(pub)
            pub_id = f"pub_{i}"
            
            # Extract publication details
            bib = pub_filled.get('bib', {})
            data["publications"][pub_id] = {
                "bib": {
                    "title": bib.get('title', ''),
                    "author": ', '.join(bib.get('author', [])) if isinstance(bib.get('author', []), list) else bib.get('author', ''),
                    "venue": bib.get('venue', bib.get('journal', '')),
                    "pub_year": bib.get('pub_year', ''),
                    "volume": bib.get('volume', ''),
                    "number": bib.get('number', ''),
                    "pages": bib.get('pages', '')
                },
                "num_citations": pub_filled.get('num_citations', 0),
                "pub_url": pub_filled.get('pub_url', '#'),
                "author_pub_id": pub_id
            }
        
        return data
        
    except Exception as e:
        print(f"Error fetching Google Scholar data: {e}")
        return None

def fetch_with_requests(scholar_id="pez-fEUAAAAJ"):
    """Fallback method using requests library"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        url = f"https://scholar.google.com/citations?user={scholar_id}&hl=en"
        
        # Add random delay to avoid rate limiting
        time.sleep(random.uniform(1, 3))
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract citation count
            citation_text = soup.find('td', text='Citations')
            citations = 0
            if citation_text:
                citations_td = citation_text.find_next_sibling('td')
                if citations_td:
                    citations = int(citations_td.text.replace(',', ''))
            
            # Extract h-index
            hindex_text = soup.find('td', text='h-index')
            hindex = 0
            if hindex_text:
                hindex_td = hindex_text.find_next_sibling('td')
                if hindex_td:
                    hindex = int(hindex_td.text.replace(',', ''))
            
            # Extract i10-index
            i10_text = soup.find('td', text='i10-index')
            i10index = 0
            if i10_text:
                i10_td = i10_text.find_next_sibling('td')
                if i10_td:
                    i10index = int(i10_td.text.replace(',', ''))
            
            # Extract publications
            publications = {}
            pub_rows = soup.find_all('tr', class_='gsc_a_tr')
            
            for i, row in enumerate(pub_rows):
                title_elem = row.find('a', class_='gsc_a_at')
                authors_elem = row.find('div', class_='gs_gray')
                venue_elem = row.find_all('div', class_='gs_gray')[1] if len(row.find_all('div', class_='gs_gray')) > 1 else None
                year_elem = row.find('span', class_='gsc_a_h')
                citations_elem = row.find('a', class_='gsc_a_ac')
                
                pub_id = f"pub_{i}"
                publications[pub_id] = {
                    "bib": {
                        "title": title_elem.text if title_elem else "",
                        "author": authors_elem.text if authors_elem else "",
                        "venue": venue_elem.text if venue_elem else "",
                        "pub_year": year_elem.text if year_elem else ""
                    },
                    "num_citations": int(citations_elem.text) if citations_elem and citations_elem.text else 0,
                    "pub_url": f"https://scholar.google.com{title_elem['href']}" if title_elem and 'href' in title_elem.attrs else "#",
                    "author_pub_id": pub_id
                }
            
            return {
                "name": "Shiyang Zhang",
                "affiliation": "Yale University",
                "email": "harryzhang957@gmail.com",
                "citedby": citations,
                "hindex": hindex,
                "i10index": i10index,
                "citedby5y": citations,  # Simplified
                "hindex5y": hindex,  # Simplified
                "i10index5y": i10index,  # Simplified
                "updated": str(datetime.now()),
                "publications": publications
            }
    except Exception as e:
        print(f"Error with requests method: {e}")
        return None

def main():
    print("Fetching Google Scholar data...")
    
    # Try scholarly library first
    data = fetch_google_scholar_data()
    
    # If scholarly fails, try requests method
    if not data:
        print("Trying fallback method...")
        data = fetch_with_requests()
    
    if not data:
        print("Failed to fetch data from Google Scholar")
        sys.exit(1)
    
    # Create google-scholar-stats directory if it doesn't exist
    os.makedirs('google-scholar-stats', exist_ok=True)
    
    # Save main data
    with open('google-scholar-stats/gs_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    # Save shields.io data for citation badge
    shieldio_data = {
        "schemaVersion": 1,
        "label": "citations",
        "message": str(data['citedby']),
    }
    with open('google-scholar-stats/gs_data_shieldsio.json', 'w', encoding='utf-8') as f:
        json.dump(shieldio_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Data fetched successfully!")
    print(f"   Total publications: {len(data['publications'])}")
    print(f"   Total citations: {data['citedby']}")
    print(f"   H-index: {data['hindex']}")
    print(f"   i10-index: {data['i10index']}")

if __name__ == "__main__":
    main()