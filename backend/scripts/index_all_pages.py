#!/usr/bin/env python
"""
Comprehensive Page Indexing Script for ChromaDB Vector Store

This script indexes all pages from PostgreSQL into ChromaDB as vector embeddings.
Each page becomes one chunk with proper indexing between SQL DB and vector DB.

Usage:
    python scripts/index_all_pages.py

Requirements:
    - Django environment configured
    - ChromaDB and Google Generative AI packages installed
    - Database with Page model populated
"""

import os
import sys
import django
from pathlib import Path

# Add project root to Python path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'confluence_clone.settings')
django.setup()

from pages.models import Page
from pages.vector_store import vector_store
import time

def main():
    """Index all pages into ChromaDB vector store"""
    
    print("🚀 Starting comprehensive page indexing...")
    print("=" * 50)
    
    # Get all pages from database
    all_pages = Page.objects.all().order_by('id')
    total_pages = all_pages.count()
    
    if total_pages == 0:
        print("❌ No pages found in database. Create some pages first.")
        return
    
    print(f"📊 Found {total_pages} pages to index")
    
    # Get current vector store stats
    try:
        stats = vector_store.get_collection_stats()
        print(f"📦 Current vector store: {stats.get('total_vectors', 0)} vectors")
        print(f"🔧 Embedding model: {stats.get('embedding_model', 'Unknown')}")
    except Exception as e:
        print(f"⚠️  Could not get vector store stats: {e}")
    
    print("\n🔄 Starting indexing process...")
    
    # Track progress
    success_count = 0
    error_count = 0
    start_time = time.time()
    
    for i, page in enumerate(all_pages, 1):
        try:
            # Show progress
            print(f"[{i:3d}/{total_pages}] Indexing: {page.title[:50]}{'...' if len(page.title) > 50 else ''}")
            
            # Index the page
            if vector_store.add_page_vector(page):
                success_count += 1
            else:
                error_count += 1
                print(f"    ❌ Failed to index page {page.id}")
                
        except Exception as e:
            error_count += 1
            print(f"    ❌ Error indexing page {page.id}: {e}")
        
        # Show intermediate progress every 10 pages
        if i % 10 == 0:
            elapsed = time.time() - start_time
            rate = i / elapsed if elapsed > 0 else 0
            print(f"    📈 Progress: {i}/{total_pages} ({i/total_pages*100:.1f}%) | Rate: {rate:.1f} pages/sec")
    
    # Final statistics
    elapsed = time.time() - start_time
    print("\n" + "=" * 50)
    print("✅ Indexing complete!")
    print(f"📊 Results:")
    print(f"   • Total pages processed: {total_pages}")
    print(f"   • Successfully indexed: {success_count}")
    print(f"   • Failed to index: {error_count}")
    print(f"   • Time elapsed: {elapsed:.2f} seconds")
    print(f"   • Average rate: {total_pages/elapsed:.2f} pages/sec")
    
    # Verify final vector store stats
    try:
        final_stats = vector_store.get_collection_stats()
        print(f"   • Total vectors in store: {final_stats.get('total_vectors', 0)}")
    except Exception as e:
        print(f"   ⚠️  Could not verify final stats: {e}")
    
    print("\n🔍 Testing search functionality...")
    
    # Test search with a sample query
    if success_count > 0:
        test_query = "sample test query"
        try:
            results = vector_store.search_similar_pages(test_query, top_k=3)
            print(f"✅ Search test successful: found {len(results)} results for '{test_query}'")
            
            for i, result in enumerate(results, 1):
                print(f"   {i}. Page ID {result['page_id']}: {result['title']} (score: {result.get('similarity_score', 0):.3f})")
                
        except Exception as e:
            print(f"❌ Search test failed: {e}")
    
    print("\n🎉 Indexing process complete!")
    print("💡 You can now use the vector search API endpoints:")
    print("   • POST /api/vector-search/  - Search similar pages")
    print("   • GET  /api/vector-stats/   - Get collection statistics")
    print("   • POST /api/reindex-vectors/ - Re-run this indexing process")

if __name__ == '__main__':
    main()