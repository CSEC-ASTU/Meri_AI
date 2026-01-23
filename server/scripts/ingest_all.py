"""
Run All Ingestion Scripts
Master script to populate all ASTU Route AI data
"""
import sys
import os
import asyncio
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.ingest_campus_pois import ingest_campus_pois
from scripts.ingest_documents import ingest_documents
from scripts.ingest_city_services import ingest_city_services
from app.core.logging_config import logger


async def run_all_ingestion():
    """Run all ingestion scripts in sequence"""
    print("\n" + "=" * 60)
    print("🚀 ASTU Route AI - Complete Data Ingestion")
    print("=" * 60)
    print("\nThis will populate:")
    print("  1. Campus POIs (buildings, facilities)")
    print("  2. Knowledge Base (ASTU information documents)")
    print("  3. City Services (nearby mosques, pharmacies, etc.)")
    print("\n" + "=" * 60)
    
    results = {}
    
    # Step 1: Campus POIs
    print("\n📍 Step 1/3: Ingesting Campus POIs...")
    print("-" * 60)
    try:
        results['campus_pois'] = await ingest_campus_pois()
        if results['campus_pois']:
            print("✅ Campus POIs ingestion successful")
        else:
            print("❌ Campus POIs ingestion failed")
    except Exception as e:
        logger.error(f"Campus POIs ingestion error: {e}")
        results['campus_pois'] = False
    
    # Step 2: Knowledge Documents
    print("\n📚 Step 2/3: Ingesting Knowledge Base Documents...")
    print("-" * 60)
    print("⏳ This will take ~30 seconds (generating embeddings)...")
    try:
        results['documents'] = await ingest_documents()
        if results['documents']:
            print("✅ Documents ingestion successful")
        else:
            print("❌ Documents ingestion failed")
    except Exception as e:
        logger.error(f"Documents ingestion error: {e}")
        results['documents'] = False
    
    # Step 3: City Services
    print("\n🏙️  Step 3/3: Ingesting City Services...")
    print("-" * 60)
    try:
        results['city_services'] = await ingest_city_services()
        if results['city_services']:
            print("✅ City services ingestion successful")
        else:
            print("❌ City services ingestion failed")
    except Exception as e:
        logger.error(f"City services ingestion error: {e}")
        results['city_services'] = False
    
    # Final Summary
    print("\n" + "=" * 60)
    print("📊 INGESTION SUMMARY")
    print("=" * 60)
    
    success_count = sum(1 for v in results.values() if v)
    total_count = len(results)
    
    for task, success in results.items():
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"{task.replace('_', ' ').title()}: {status}")
    
    print("-" * 60)
    print(f"Overall: {success_count}/{total_count} tasks completed")
    
    if success_count == total_count:
        print("\n🎉 All data ingestion completed successfully!")
        print("\n✅ Your ASTU Route AI backend is ready to use!")
        print("\nNext steps:")
        print("  1. Start the server: python main.py")
        print("  2. Test API endpoints at http://localhost:4000/api/docs")
        print("  3. Try queries, routes, and nearby services")
        return True
    else:
        print(f"\n⚠️  {total_count - success_count} task(s) failed")
        print("Review the logs above for error details.")
        return False


if __name__ == "__main__":
    result = asyncio.run(run_all_ingestion())
    sys.exit(0 if result else 1)
