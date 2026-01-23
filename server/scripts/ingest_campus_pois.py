"""
Ingest Campus POIs - Populate ASTU building and landmark data
Adds Points of Interest for Adama Science and Technology University
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


# ASTU Campus POIs - Manually curated data
# Coordinates are approximate - should be verified with actual GPS data
CAMPUS_POIS = [
    # Main Buildings
    {
        "name": "ASTU Main Gate",
        "category": "gate",
        "latitude": 8.5569,
        "longitude": 39.2911,
        "description": "Main entrance to Adama Science and Technology University",
        "tags": ["entrance", "gate", "main"]
    },
    {
        "name": "Block 1",
        "category": "building",
        "latitude": 8.5575,
        "longitude": 39.2920,
        "description": "Academic Block 1 - Main lecture halls",
        "tags": ["classroom", "lecture", "academic"]
    },
    {
        "name": "Block 2",
        "category": "building",
        "latitude": 8.5580,
        "longitude": 39.2925,
        "description": "Academic Block 2 - Engineering departments",
        "tags": ["engineering", "classroom", "academic"]
    },
    {
        "name": "Block 3",
        "category": "building",
        "latitude": 8.5585,
        "longitude": 39.2930,
        "description": "Academic Block 3 - Science departments",
        "tags": ["science", "classroom", "academic"]
    },
    {
        "name": "Block 4",
        "category": "building",
        "latitude": 8.5570,
        "longitude": 39.2935,
        "description": "Academic Block 4 - Computing and IT",
        "tags": ["computing", "it", "classroom", "academic"]
    },
    {
        "name": "Block 5",
        "category": "building",
        "latitude": 8.5565,
        "longitude": 39.2940,
        "description": "Academic Block 5 - Business and Economics",
        "tags": ["business", "economics", "classroom", "academic"]
    },
    
    # Administrative Buildings
    {
        "name": "Administration Building",
        "category": "administrative",
        "latitude": 8.5578,
        "longitude": 39.2915,
        "description": "Main administration and offices",
        "tags": ["admin", "office", "registry"]
    },
    {
        "name": "Registrar Office",
        "category": "administrative",
        "latitude": 8.5576,
        "longitude": 39.2913,
        "description": "Student registration and academic records",
        "tags": ["registrar", "registration", "office"]
    },
    
    # Library and Resources
    {
        "name": "Main Library",
        "category": "library",
        "latitude": 8.5582,
        "longitude": 39.2922,
        "description": "Central library and study halls",
        "tags": ["library", "books", "study", "reading"]
    },
    {
        "name": "ICT Center",
        "category": "facility",
        "latitude": 8.5573,
        "longitude": 39.2918,
        "description": "Information and Communication Technology Center",
        "tags": ["ict", "computer", "lab", "technology"]
    },
    
    # Laboratories
    {
        "name": "Engineering Lab Complex",
        "category": "laboratory",
        "latitude": 8.5590,
        "longitude": 39.2928,
        "description": "Engineering laboratories and workshops",
        "tags": ["lab", "engineering", "workshop", "practical"]
    },
    {
        "name": "Science Lab Building",
        "category": "laboratory",
        "latitude": 8.5588,
        "longitude": 39.2932,
        "description": "Chemistry, Physics, and Biology labs",
        "tags": ["lab", "science", "chemistry", "physics", "biology"]
    },
    {
        "name": "Computer Lab 1",
        "category": "laboratory",
        "latitude": 8.5572,
        "longitude": 39.2938,
        "description": "Main computer laboratory",
        "tags": ["lab", "computer", "programming", "software"]
    },
    
    # Student Facilities
    {
        "name": "Student Cafeteria",
        "category": "cafeteria",
        "latitude": 8.5577,
        "longitude": 39.2927,
        "description": "Main student dining hall and cafeteria",
        "tags": ["cafeteria", "food", "dining", "restaurant"]
    },
    {
        "name": "Student Union Building",
        "category": "facility",
        "latitude": 8.5574,
        "longitude": 39.2924,
        "description": "Student activities and clubs",
        "tags": ["student", "union", "activities", "clubs"]
    },
    
    # Dormitories
    {
        "name": "Male Dormitory Block A",
        "category": "dormitory",
        "latitude": 8.5560,
        "longitude": 39.2945,
        "description": "Male student housing Block A",
        "tags": ["dormitory", "housing", "male", "residence"]
    },
    {
        "name": "Male Dormitory Block B",
        "category": "dormitory",
        "latitude": 8.5562,
        "longitude": 39.2948,
        "description": "Male student housing Block B",
        "tags": ["dormitory", "housing", "male", "residence"]
    },
    {
        "name": "Female Dormitory Block A",
        "category": "dormitory",
        "latitude": 8.5558,
        "longitude": 39.2950,
        "description": "Female student housing Block A",
        "tags": ["dormitory", "housing", "female", "residence"]
    },
    {
        "name": "Female Dormitory Block B",
        "category": "dormitory",
        "latitude": 8.5555,
        "longitude": 39.2953,
        "description": "Female student housing Block B",
        "tags": ["dormitory", "housing", "female", "residence"]
    },
    
    # Sports and Recreation
    {
        "name": "Sports Complex",
        "category": "sports",
        "latitude": 8.5595,
        "longitude": 39.2942,
        "description": "Main sports facilities and gymnasium",
        "tags": ["sports", "gym", "athletics", "fitness"]
    },
    {
        "name": "Football Field",
        "category": "sports",
        "latitude": 8.5598,
        "longitude": 39.2945,
        "description": "Main football/soccer field",
        "tags": ["sports", "football", "soccer", "field"]
    },
    {
        "name": "Basketball Court",
        "category": "sports",
        "latitude": 8.5593,
        "longitude": 39.2938,
        "description": "Outdoor basketball courts",
        "tags": ["sports", "basketball", "court"]
    },
    
    # Medical and Health
    {
        "name": "University Clinic",
        "category": "medical",
        "latitude": 8.5571,
        "longitude": 39.2921,
        "description": "Campus health clinic and medical services",
        "tags": ["clinic", "medical", "health", "doctor"]
    },
    
    # Other Facilities
    {
        "name": "Auditorium",
        "category": "facility",
        "latitude": 8.5583,
        "longitude": 39.2917,
        "description": "Main auditorium for events and ceremonies",
        "tags": ["auditorium", "hall", "ceremony", "event"]
    },
    {
        "name": "Mosque",
        "category": "religious",
        "latitude": 8.5567,
        "longitude": 39.2933,
        "description": "Campus mosque for prayer",
        "tags": ["mosque", "prayer", "islamic", "worship"]
    },
    {
        "name": "Chapel",
        "category": "religious",
        "latitude": 8.5566,
        "longitude": 39.2936,
        "description": "Campus chapel for worship",
        "tags": ["chapel", "church", "christian", "worship"]
    },
    {
        "name": "Parking Lot 1",
        "category": "parking",
        "latitude": 8.5568,
        "longitude": 39.2910,
        "description": "Main parking area near entrance",
        "tags": ["parking", "car", "vehicle"]
    },
    {
        "name": "Parking Lot 2",
        "category": "parking",
        "latitude": 8.5585,
        "longitude": 39.2943,
        "description": "Secondary parking near dormitories",
        "tags": ["parking", "car", "vehicle"]
    },
    {
        "name": "Bus Stop - Main Gate",
        "category": "transport",
        "latitude": 8.5570,
        "longitude": 39.2908,
        "description": "University shuttle and public bus stop",
        "tags": ["bus", "transport", "shuttle", "public"]
    },
    {
        "name": "ATM - Commercial Bank",
        "category": "atm",
        "latitude": 8.5575,
        "longitude": 39.2916,
        "description": "Commercial Bank of Ethiopia ATM",
        "tags": ["atm", "bank", "money", "cash"]
    },
    {
        "name": "Campus Bookstore",
        "category": "shop",
        "latitude": 8.5576,
        "longitude": 39.2919,
        "description": "University bookstore and supplies",
        "tags": ["bookstore", "shop", "supplies", "books"]
    },
]


async def ingest_campus_pois():
    """Ingest campus POIs into database"""
    logger.info("Starting ASTU Campus POI ingestion...")
    
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
        
        # Insert POIs
        success_count = 0
        error_count = 0
        
        for poi in CAMPUS_POIS:
            try:
                poi_id = await db.add_poi(
                    name=poi["name"],
                    category=poi["category"],
                    latitude=poi["latitude"],
                    longitude=poi["longitude"],
                    description=poi.get("description"),
                    tags=poi.get("tags", [])
                )
                
                if poi_id:
                    logger.info(f"✓ Added: {poi['name']} (ID: {poi_id})")
                    success_count += 1
                else:
                    logger.warning(f"⚠ Failed to add: {poi['name']}")
                    error_count += 1
                    
            except Exception as e:
                logger.error(f"✗ Error adding {poi['name']}: {e}")
                error_count += 1
        
        # Summary
        logger.info("\n=== Ingestion Complete ===")
        logger.info(f"Total POIs: {len(CAMPUS_POIS)}")
        logger.info(f"Successful: {success_count}")
        logger.info(f"Failed: {error_count}")
        logger.info(f"Success rate: {(success_count/len(CAMPUS_POIS)*100):.1f}%")
        
        return success_count > 0
        
    except Exception as e:
        logger.error(f"Ingestion failed: {e}")
        return False


if __name__ == "__main__":
    print("\n🏫 ASTU Route AI - Campus POI Ingestion")
    print("=" * 50)
    print(f"Database: {settings.database_url[:30]}...")
    print(f"POIs to ingest: {len(CAMPUS_POIS)}")
    print("=" * 50)
    
    # Run ingestion
    result = asyncio.run(ingest_campus_pois())
    
    if result:
        print("\n✅ Ingestion completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Ingestion failed!")
        sys.exit(1)
