import json
import os
import sys
from datetime import datetime

def main():
    print("🚀 Starting Google Scholar data fetch...")
    print("🔧 Environment check:")
    print(f"   - GOOGLE_SCHOLAR_ID: {os.environ.get('GOOGLE_SCHOLAR_ID', 'NOT SET')}")
    print(f"   - Python version: {sys.version}")
    print(f"   - Current directory: {os.getcwd()}")
    
    try:
        # Try to import scholarly
        print("📦 Importing scholarly library...")
        from scholarly import scholarly
        print("✅ Scholarly library imported successfully")
        
        scholar_id = os.environ.get('GOOGLE_SCHOLAR_ID')
        if not scholar_id:
            print("❌ ERROR: GOOGLE_SCHOLAR_ID not set")
            sys.exit(1)
            
        print(f"🔍 Fetching data for Google Scholar ID: {scholar_id}")
        
        # Set a proxy to avoid blocking and speed up requests
        print("🔧 Setting up free proxy to avoid rate limiting...")
        try:
            from scholarly import ProxyGenerator
            pg = ProxyGenerator()
            pg.FreeProxies()
            scholarly.use_proxy(pg)
            print("✅ Free proxy configured!")
        except Exception as proxy_error:
            print(f"⚠️  Proxy setup failed: {proxy_error}, continuing without proxy...")
        
        # Search for author
        try:
            print("🔎 Searching for author...")
            author = scholarly.search_author_id(scholar_id)
            print("✅ Author found, fetching detailed data...")
            
            scholarly.fill(author, sections=['basics', 'indices', 'counts', 'publications'])
            print("✅ Author data filled successfully")
            
            # Process data
            author['updated'] = datetime.now().isoformat() + "Z"
            author['publications'] = {v['author_pub_id']: v for v in author['publications']}
            
            print(f"✅ Successfully fetched data for {author.get('name', 'Unknown')}")
            print(f"📊 Total citations: {author.get('citedby', 0)}")
            print(f"📊 H-index: {author.get('hindex', 0)}")
            print(f"📊 I10-index: {author.get('i10index', 0)}")
            print(f"📚 Publications: {len(author.get('publications', {}))}")
            
        except Exception as e:
            print(f"❌ Error fetching from Google Scholar: {e}")
            print("⏭️  No statistics files were written; the published data remains unchanged.")
            sys.exit(1)
            
    except ImportError:
        print("❌ Scholarly library not available")
        print("⏭️  No statistics files were written; the published data remains unchanged.")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        print("⏭️  No statistics files were written; the published data remains unchanged.")
        sys.exit(1)
    
    # Save results
    print("💾 Saving data to files...")
    os.makedirs('results', exist_ok=True)
    print("📁 Created results directory")
    
    # Save full data
    print("📄 Writing gs_data.json...")
    with open('results/gs_data.json', 'w', encoding='utf-8') as f:
        json.dump(author, f, ensure_ascii=False, indent=2)
    print("✅ gs_data.json saved")
    
    # Save shields.io data
    print("📄 Writing gs_data_shieldsio.json...")
    shieldio_data = {
        "schemaVersion": 1,
        "label": "citations",
        "message": str(author.get('citedby', 0)),
    }
    with open('results/gs_data_shieldsio.json', 'w', encoding='utf-8') as f:
        json.dump(shieldio_data, f, ensure_ascii=False, indent=2)
    print("✅ gs_data_shieldsio.json saved")
    
    print("🎉 Data saved successfully!")
    print(f"📊 Final stats: {author.get('citedby', 0)} citations, {author.get('hindex', 0)} h-index")
    
if __name__ == "__main__":
    main()
