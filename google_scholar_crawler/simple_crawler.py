import json
import os
import sys
from datetime import datetime

# Simple fallback data generator
def generate_fallback_data():
    """Generate basic data structure when Google Scholar is unavailable"""
    data = {
        "name": "Sizhuang He",
        "affiliation": "Yale University",
        "email": "sizhuang.he@yale.edu",
        "citedby": 0,
        "citedby5y": 0,
        "hindex": 0,
        "hindex5y": 0,
        "i10index": 0,
        "i10index5y": 0,
        "updated": str(datetime.now()),
        "publications": {},
        "message": "Google Scholar data will be populated once publications are indexed"
    }
    return data

def main():
    print("Starting Google Scholar data fetch...")
    
    try:
        # Try to import scholarly
        from scholarly import scholarly
        
        scholar_id = os.environ.get('GOOGLE_SCHOLAR_ID')
        if not scholar_id:
            print("ERROR: GOOGLE_SCHOLAR_ID not set")
            sys.exit(1)
            
        print(f"Fetching data for Google Scholar ID: {scholar_id}")
        
        # Set a proxy to avoid blocking (optional)
        # scholarly.use_proxy(scholarly.ProxyGenerator())
        
        # Search for author
        try:
            author = scholarly.search_author_id(scholar_id)
            scholarly.fill(author, sections=['basics', 'indices', 'counts', 'publications'])
            
            # Process data
            author['updated'] = str(datetime.now())
            author['publications'] = {v['author_pub_id']: v for v in author['publications']}
            
            print(f"Successfully fetched data for {author.get('name', 'Unknown')}")
            print(f"Total citations: {author.get('citedby', 0)}")
            
        except Exception as e:
            print(f"Error fetching from Google Scholar: {e}")
            print("Using fallback data...")
            author = generate_fallback_data()
            
    except ImportError:
        print("Scholarly library not available, using fallback data")
        author = generate_fallback_data()
    except Exception as e:
        print(f"Unexpected error: {e}")
        author = generate_fallback_data()
    
    # Save results
    os.makedirs('results', exist_ok=True)
    
    # Save full data
    with open('results/gs_data.json', 'w', encoding='utf-8') as f:
        json.dump(author, f, ensure_ascii=False, indent=2)
    
    # Save shields.io data
    shieldio_data = {
        "schemaVersion": 1,
        "label": "citations",
        "message": str(author.get('citedby', 0)),
    }
    with open('results/gs_data_shieldsio.json', 'w', encoding='utf-8') as f:
        json.dump(shieldio_data, f, ensure_ascii=False, indent=2)
    
    print("Data saved successfully!")
    
if __name__ == "__main__":
    main()
