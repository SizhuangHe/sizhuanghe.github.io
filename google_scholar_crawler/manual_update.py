#!/usr/bin/env python3
"""
Manual Google Scholar data updater
Run this locally to update your publication data
"""
import json
import os
from datetime import datetime

# Your publication data - UPDATE THIS WITH YOUR ACTUAL PUBLICATIONS
PUBLICATIONS = [
    # Example format:
    # {
    #     "title": "Your Paper Title",
    #     "authors": "Shiyang Zhang, Co-author Name",
    #     "venue": "Conference/Journal Name",
    #     "year": 2024,
    #     "citations": 0,
    #     "url": "https://link-to-paper.com"
    # }
]

def generate_scholar_data():
    """Generate Google Scholar-like data structure"""
    
    # Calculate total citations
    total_citations = sum(pub.get('citations', 0) for pub in PUBLICATIONS)
    
    # Create publication dictionary
    publications = {}
    for i, pub in enumerate(PUBLICATIONS):
        pub_id = f"pub_{i}"
        publications[pub_id] = {
            "bib": {
                "title": pub.get("title", ""),
                "author": pub.get("authors", ""),
                "venue": pub.get("venue", ""),
                "pub_year": pub.get("year", 2024),
            },
            "num_citations": pub.get("citations", 0),
            "pub_url": pub.get("url", "#"),
            "author_pub_id": pub_id
        }
    
    # Create the main data structure
    data = {
        "name": "Shiyang Zhang",
        "affiliation": "Yale University",
        "email": "harryzhang957@gmail.com",
        "citedby": total_citations,
        "citedby5y": total_citations,  # Simplified for now
        "hindex": 0,  # Calculate if needed
        "hindex5y": 0,
        "i10index": len([p for p in PUBLICATIONS if p.get('citations', 0) >= 10]),
        "i10index5y": len([p for p in PUBLICATIONS if p.get('citations', 0) >= 10]),
        "updated": str(datetime.now()),
        "publications": publications
    }
    
    return data

def main():
    print("Generating Google Scholar data...")
    
    # Generate data
    data = generate_scholar_data()
    
    # Create results directory
    os.makedirs('results', exist_ok=True)
    
    # Save main data
    with open('results/gs_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    # Save shields.io data
    shieldio_data = {
        "schemaVersion": 1,
        "label": "citations",
        "message": str(data['citedby']),
    }
    with open('results/gs_data_shieldsio.json', 'w', encoding='utf-8') as f:
        json.dump(shieldio_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Data generated successfully!")
    print(f"   Total publications: {len(PUBLICATIONS)}")
    print(f"   Total citations: {data['citedby']}")
    print("\nTo update on GitHub:")
    print("1. Copy the files from 'results/' directory")
    print("2. Commit them to the 'google-scholar-stats' branch")

if __name__ == "__main__":
    main()
