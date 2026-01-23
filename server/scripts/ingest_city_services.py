"""
Ingest City Services - Populate Adama city services near ASTU
Adds nearby mosques, pharmacies, salons, cafes, etc.
"""
import sys
import os
import asyncio
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from database import Database
from config import settings
from app.core.logging_config import logger


# Adama City Services near ASTU
# Coordinates are approximate - ideally from OSM or Google Places API
CITY_SERVICES = [
    # Mosques
    {
        "name": "Grand Mosque Adama",
        "category": "mosque",
        "latitude": 8.5400,
        "longitude": 39.2700,
        "description": "Main grand mosque in Adama city center",
        "tags": ["mosque", "prayer", "islamic", "worship"]
    },
    {
        "name": "Al-Nur Mosque",
        "category": "mosque",
        "latitude": 8.5500,
        "longitude": 39.2800,
        "description": "Community mosque near ASTU",
        "tags": ["mosque", "prayer", "islamic"]
    },
    {
        "name": "Bilal Mosque",
        "category": "mosque",
        "latitude": 8.5450,
        "longitude": 39.2850,
        "description": "Small neighborhood mosque",
        "tags": ["mosque", "prayer", "islamic"]
    },
    
    # Pharmacies
    {
        "name": "Adama Pharmacy",
        "category": "pharmacy",
        "latitude": 8.5420,
        "longitude": 39.2720,
        "description": "Well-stocked pharmacy in city center",
        "tags": ["pharmacy", "medicine", "drugstore", "health"]
    },
    {
        "name": "Selam Pharmacy",
        "category": "pharmacy",
        "latitude": 8.5480,
        "longitude": 39.2780,
        "description": "24-hour pharmacy near hospital",
        "tags": ["pharmacy", "medicine", "24hour", "emergency"]
    },
    {
        "name": "Hayat Pharmacy",
        "category": "pharmacy",
        "latitude": 8.5550,
        "longitude": 39.2850,
        "description": "Pharmacy close to ASTU campus",
        "tags": ["pharmacy", "medicine", "drugstore"]
    },
    
    # Hair Salons
    {
        "name": "Star Beauty Salon",
        "category": "salon",
        "latitude": 8.5430,
        "longitude": 39.2740,
        "description": "Professional hair and beauty salon",
        "tags": ["salon", "hair", "beauty", "haircut"]
    },
    {
        "name": "Modern Barber Shop",
        "category": "salon",
        "latitude": 8.5460,
        "longitude": 39.2790,
        "description": "Men's barbershop",
        "tags": ["salon", "barber", "haircut", "male"]
    },
    {
        "name": "Elegance Hair Studio",
        "category": "salon",
        "latitude": 8.5520,
        "longitude": 39.2820,
        "description": "Unisex hair salon near campus",
        "tags": ["salon", "hair", "beauty", "unisex"]
    },
    
    # Cafes and Coffee Shops
    {
        "name": "Tomoca Coffee",
        "category": "cafe",
        "latitude": 8.5440,
        "longitude": 39.2760,
        "description": "Popular Ethiopian coffee house",
        "tags": ["cafe", "coffee", "ethiopian", "beverage"]
    },
    {
        "name": "Kaldi's Coffee",
        "category": "cafe",
        "latitude": 8.5490,
        "longitude": 39.2810,
        "description": "Modern cafe with WiFi",
        "tags": ["cafe", "coffee", "wifi", "study"]
    },
    {
        "name": "Student Cafe",
        "category": "cafe",
        "latitude": 8.5540,
        "longitude": 39.2880,
        "description": "Small cafe popular with ASTU students",
        "tags": ["cafe", "coffee", "student", "cheap"]
    },
    
    # Restaurants
    {
        "name": "Habesha Restaurant",
        "category": "restaurant",
        "latitude": 8.5410,
        "longitude": 39.2710,
        "description": "Traditional Ethiopian restaurant",
        "tags": ["restaurant", "ethiopian", "food", "traditional"]
    },
    {
        "name": "Pizza House Adama",
        "category": "restaurant",
        "latitude": 8.5470,
        "longitude": 39.2800,
        "description": "Pizza and fast food restaurant",
        "tags": ["restaurant", "pizza", "fastfood", "western"]
    },
    {
        "name": "Campus Eatery",
        "category": "restaurant",
        "latitude": 8.5560,
        "longitude": 39.2900,
        "description": "Budget-friendly restaurant near ASTU",
        "tags": ["restaurant", "budget", "student", "local"]
    },
    
    # Banks and ATMs
    {
        "name": "Commercial Bank of Ethiopia - Adama Branch",
        "category": "bank",
        "latitude": 8.5390,
        "longitude": 39.2690,
        "description": "Main CBE branch in Adama",
        "tags": ["bank", "cbe", "financial", "atm"]
    },
    {
        "name": "Dashen Bank",
        "category": "bank",
        "latitude": 8.5445,
        "longitude": 39.2770,
        "description": "Private bank branch",
        "tags": ["bank", "dashen", "financial"]
    },
    {
        "name": "ATM - Wegagen Bank",
        "category": "atm",
        "latitude": 8.5510,
        "longitude": 39.2830,
        "description": "24-hour ATM service",
        "tags": ["atm", "bank", "cash", "24hour"]
    },
    {
        "name": "ATM - Awash Bank",
        "category": "atm",
        "latitude": 8.5530,
        "longitude": 39.2860,
        "description": "ATM near campus",
        "tags": ["atm", "bank", "cash"]
    },
    
    # Medical Facilities
    {
        "name": "Adama Hospital",
        "category": "hospital",
        "latitude": 8.5380,
        "longitude": 39.2680,
        "description": "Main government hospital in Adama",
        "tags": ["hospital", "medical", "emergency", "health"]
    },
    {
        "name": "Family Health Clinic",
        "category": "clinic",
        "latitude": 8.5455,
        "longitude": 39.2785,
        "description": "Private medical clinic",
        "tags": ["clinic", "medical", "health", "doctor"]
    },
    {
        "name": "Adama Medical Center",
        "category": "clinic",
        "latitude": 8.5505,
        "longitude": 39.2825,
        "description": "Private clinic near ASTU",
        "tags": ["clinic", "medical", "health", "private"]
    },
    
    # Shopping
    {
        "name": "Adama Supermarket",
        "category": "supermarket",
        "latitude": 8.5425,
        "longitude": 39.2730,
        "description": "Large supermarket in city center",
        "tags": ["supermarket", "shopping", "groceries", "food"]
    },
    {
        "name": "Mini Mart",
        "category": "supermarket",
        "latitude": 8.5495,
        "longitude": 39.2815,
        "description": "Convenience store",
        "tags": ["supermarket", "convenience", "shopping"]
    },
    {
        "name": "Local Market (Suq)",
        "category": "market",
        "latitude": 8.5360,
        "longitude": 39.2650,
        "description": "Traditional open-air market",
        "tags": ["market", "traditional", "shopping", "local"]
    },
    
    # Bakeries
    {
        "name": "Fresh Bakery",
        "category": "bakery",
        "latitude": 8.5435,
        "longitude": 39.2750,
        "description": "Bakery with fresh bread and pastries",
        "tags": ["bakery", "bread", "pastry", "fresh"]
    },
    {
        "name": "Sunrise Bakery",
        "category": "bakery",
        "latitude": 8.5515,
        "longitude": 39.2835,
        "description": "Early morning bakery",
        "tags": ["bakery", "bread", "breakfast"]
    },
    
    # Hotels
    {
        "name": "Adama Hotel",
        "category": "hotel",
        "latitude": 8.5395,
        "longitude": 39.2695,
        "description": "Main hotel in city center",
        "tags": ["hotel", "accommodation", "lodging"]
    },
    {
        "name": "Rift Valley Hotel",
        "category": "hotel",
        "latitude": 8.5465,
        "longitude": 39.2795,
        "description": "Mid-range hotel",
        "tags": ["hotel", "accommodation", "midrange"]
    },
    
    # Transportation
    {
        "name": "Adama Bus Station",
        "category": "transport",
        "latitude": 8.5370,
        "longitude": 39.2670,
        "description": "Main bus terminal for intercity travel",
        "tags": ["bus", "transport", "station", "intercity"]
    },
    {
        "name": "Taxi Stand - Main Square",
        "category": "taxi",
        "latitude": 8.5415,
        "longitude": 39.2715,
        "description": "Taxi pickup point in city center",
        "tags": ["taxi", "transport", "ride"]
    },
    {
        "name": "Taxi Stand - Near ASTU",
        "category": "taxi",
        "latitude": 8.5545,
        "longitude": 39.2890,
        "description": "Taxi stand near university",
        "tags": ["taxi", "transport", "campus"]
    },
]


async def ingest_city_services():
    """Ingest Adama city services into database"""
    logger.info("Starting Adama City Services ingestion...")
    
    db = Database()
    
    try:
        # Test connection
        if not db.test_connection():
            logger.error("Database connection failed")
            return False
        
        logger.info("✓ Database connected")
        
        # Create tables if they don't exist
        db.create_tables()
        logger.info("✓ Tables ready")
        
        # Insert city services
        success_count = 0
        error_count = 0
        
        for service in CITY_SERVICES:
            try:
                service_id = await db.add_poi(
                    name=service["name"],
                    category=service["category"],
                    latitude=service["latitude"],
                    longitude=service["longitude"],
                    description=service.get("description"),
                    tags=service.get("tags", [])
                )
                
                if service_id:
                    logger.info(f"✓ Added: {service['name']} ({service['category']})")
                    success_count += 1
                else:
                    logger.warning(f"⚠ Failed to add: {service['name']}")
                    error_count += 1
                    
            except Exception as e:
                logger.error(f"✗ Error adding {service['name']}: {e}")
                error_count += 1
        
        # Summary
        logger.info("\n=== Ingestion Complete ===")
        logger.info(f"Total Services: {len(CITY_SERVICES)}")
        logger.info(f"Successful: {success_count}")
        logger.info(f"Failed: {error_count}")
        logger.info(f"Success rate: {(success_count/len(CITY_SERVICES)*100):.1f}%")
        
        # Category breakdown
        categories = {}
        for service in CITY_SERVICES:
            cat = service["category"]
            categories[cat] = categories.get(cat, 0) + 1
        
        logger.info("\n=== Category Breakdown ===")
        for cat, count in sorted(categories.items()):
            logger.info(f"{cat}: {count}")
        
        return success_count > 0
        
    except Exception as e:
        logger.error(f"Ingestion failed: {e}")
        return False


if __name__ == "__main__":
    print("\n🏙️  ASTU Route AI - Adama City Services Ingestion")
    print("=" * 50)
    print(f"Database: {settings.database_url[:30]}...")
    print(f"Services to ingest: {len(CITY_SERVICES)}")
    print("=" * 50)
    
    # Run ingestion
    result = asyncio.run(ingest_city_services())
    
    if result:
        print("\n✅ Ingestion completed successfully!")
        print("City services data is ready for nearby search.")
        sys.exit(0)
    else:
        print("\n❌ Ingestion failed!")
        sys.exit(1)
