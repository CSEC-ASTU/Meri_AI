"""
Ingest Documents - Populate ASTU knowledge base with embeddings
Adds university information documents for RAG system
"""
import sys
import os
import asyncio
from pathlib import Path
from typing import List, Dict

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from database import Database
from config import settings
from app.core.logging_config import logger
from app.services.ai_service import GeminiAIService


# ASTU Knowledge Base Documents
# These should ideally come from web scraping, but manual curation for MVP
KNOWLEDGE_DOCUMENTS = [
    {
        "title": "About ASTU - University Overview",
        "content": """Adama Science and Technology University (ASTU) is one of Ethiopia's leading 
        science and technology universities, located in Adama city. Founded as Nazret Technical College, 
        it was later upgraded to university status. ASTU offers undergraduate and postgraduate programs 
        in Engineering, Natural and Computational Sciences, and Business. The university is known for 
        its focus on practical, hands-on education and research in science and technology fields.""",
        "source": "ASTU Website - About",
        "tags": ["about", "overview", "history", "introduction"]
    },
    {
        "title": "Academic Programs and Departments",
        "content": """ASTU offers programs across multiple departments including:
        - School of Engineering: Civil, Mechanical, Electrical, Chemical Engineering
        - School of Computing and Informatics: Computer Science, Software Engineering, Information Technology
        - School of Natural and Computational Sciences: Physics, Chemistry, Mathematics, Biology
        - School of Business and Economics: Accounting, Management, Economics
        All programs emphasize practical skills and industry collaboration.""",
        "source": "ASTU Academic Catalog",
        "tags": ["programs", "departments", "schools", "academic"]
    },
    {
        "title": "Campus Location and Access",
        "content": """ASTU main campus is located in Adama city (also known as Nazret), approximately 
        99 kilometers southeast of Addis Ababa along the Addis Ababa-Djibouti highway. The university 
        is easily accessible by public transportation with regular bus services from Addis Ababa. 
        The main gate is on the eastern side of the city, near the Adama-Asela road.""",
        "source": "ASTU General Information",
        "tags": ["location", "access", "address", "directions"]
    },
    {
        "title": "Admission Requirements for Undergraduate",
        "content": """Undergraduate admission to ASTU requires:
        - Completion of Ethiopian preparatory school (Grade 12)
        - Minimum EHEEE (Ethiopian Higher Education Entrance Examination) score as per yearly cutoff
        - Meeting specific department requirements for sciences and engineering
        - Application through the Ministry of Education placement system
        International students must provide equivalent qualifications and may need additional documentation.""",
        "source": "ASTU Admissions Office",
        "tags": ["admission", "requirements", "undergraduate", "application"]
    },
    {
        "title": "Library Services and Resources",
        "content": """The ASTU Main Library provides comprehensive resources including:
        - Physical books collection covering all academic disciplines
        - Digital library with online journals and e-books
        - Study halls and reading rooms for individual and group study
        - Computer lab with internet access
        - Research support and reference services
        Library hours: Monday-Friday 8:00 AM - 6:00 PM, Saturday 9:00 AM - 5:00 PM""",
        "source": "ASTU Library",
        "tags": ["library", "resources", "books", "study"]
    },
    {
        "title": "Student Housing and Dormitories",
        "content": """ASTU provides on-campus dormitory accommodation for students:
        - Separate dormitories for male and female students
        - Shared rooms with basic furniture (bed, desk, storage)
        - Common facilities including bathrooms and recreation areas
        - Cafeteria services available in dormitory areas
        Housing allocation is based on distance from home and academic performance. 
        First-year students are given priority for accommodation.""",
        "source": "ASTU Student Affairs",
        "tags": ["housing", "dormitory", "accommodation", "residence"]
    },
    {
        "title": "Campus Facilities and Services",
        "content": """ASTU campus offers various facilities:
        - Multiple cafeterias serving breakfast, lunch, and dinner
        - University clinic for basic medical services
        - Sports complex with football field, basketball courts, and gym
        - ICT center with computer labs and internet
        - ATM machines from major Ethiopian banks
        - Bookstore for academic materials and supplies
        - Prayer facilities including mosque and chapel""",
        "source": "ASTU Facilities Guide",
        "tags": ["facilities", "services", "amenities", "campus"]
    },
    {
        "title": "Student Organizations and Clubs",
        "content": """ASTU has various student organizations:
        - Student Union representing student interests
        - Academic clubs for different departments
        - Sports clubs for various athletics
        - Cultural and arts clubs
        - Volunteer and community service groups
        Students are encouraged to participate in extracurricular activities. 
        Club activities are coordinated through the Student Union Building.""",
        "source": "ASTU Student Union",
        "tags": ["clubs", "organizations", "activities", "extracurricular"]
    },
    {
        "title": "Academic Calendar and Schedule",
        "content": """ASTU follows a semester system:
        - Two main semesters per academic year
        - First semester: September to January
        - Second semester: February to June
        - Summer session may be available for some programs
        - Registration typically 1-2 weeks before semester start
        - Mid-term exams around week 7-8
        - Final exams at end of semester (week 15-16)""",
        "source": "ASTU Registrar",
        "tags": ["calendar", "schedule", "semester", "academic"]
    },
    {
        "title": "Tuition and Financial Information",
        "content": """ASTU is a public university with government-subsidized education:
        - Ethiopian students: Low tuition fees set by government
        - Fees cover registration, library, laboratory, and student services
        - Payment typically required at beginning of each semester
        - Various scholarship programs available for academically excellent students
        - Student loans available through Ethiopian government programs
        International students have separate fee structures.""",
        "source": "ASTU Finance Office",
        "tags": ["tuition", "fees", "financial", "payment"]
    },
    {
        "title": "Getting Around Campus - Navigation Tips",
        "content": """Tips for navigating ASTU campus:
        - Main academic blocks (Block 1-5) are in the central campus area
        - Administration and Registrar offices are near the main gate
        - Library is centrally located between academic blocks
        - Dormitories are on the eastern side of campus
        - Cafeteria and student facilities are in the central area
        - Sports complex is on the northern section
        - Main gate has campus map and security can provide directions
        Campus is walkable, takes about 15-20 minutes to cross""",
        "source": "ASTU Student Handbook",
        "tags": ["navigation", "directions", "campus", "map"]
    },
    {
        "title": "Registration and Academic Records",
        "content": """Student registration process at ASTU:
        - Online registration system for course enrollment
        - Registration period opens 1-2 weeks before semester
        - Students must meet with academic advisors before registration
        - Late registration incurs additional fees
        - Add/drop period in first two weeks of semester
        - Academic records available through Registrar office
        - Transcripts can be requested for official purposes""",
        "source": "ASTU Registrar Office",
        "tags": ["registration", "enrollment", "records", "transcript"]
    },
    {
        "title": "Laboratory and Practical Work",
        "content": """ASTU emphasizes practical laboratory work:
        - Engineering Lab Complex for engineering students
        - Science Lab Building for chemistry, physics, biology
        - Computer labs for IT and computing programs
        - Workshop facilities for hands-on training
        - Lab sessions are mandatory part of courses
        - Safety training required before lab access
        - Lab reports and practical exams contribute to final grades""",
        "source": "ASTU Academic Affairs",
        "tags": ["laboratory", "practical", "lab", "workshop"]
    },
    {
        "title": "Health Services and Campus Clinic",
        "content": """University clinic provides:
        - Basic medical consultation and treatment
        - First aid for emergencies
        - Referrals to hospitals for serious conditions
        - Health education and prevention programs
        - Operating hours: Monday-Friday 8:00 AM - 5:00 PM
        For emergencies outside clinic hours, security can assist with hospital transport.
        Nearest major hospital is Adama Hospital in the city center.""",
        "source": "ASTU Health Services",
        "tags": ["health", "clinic", "medical", "doctor"]
    },
    {
        "title": "Freshman Orientation and New Students",
        "content": """New student orientation at ASTU includes:
        - Campus tour showing all major facilities
        - Introduction to academic policies and expectations
        - Registration guidance and course selection help
        - Student ID card issuance
        - Library orientation and ICT account setup
        - Meeting department heads and academic advisors
        - Social activities to meet fellow students
        Orientation typically held in the week before semester starts. Attendance is highly recommended.""",
        "source": "ASTU New Student Guide",
        "tags": ["freshman", "orientation", "new students", "welcome"]
    },
    {
        "title": "Nearby City Services in Adama",
        "content": """Services available in Adama city near ASTU:
        - Multiple mosques within 1-2 km for prayer
        - Pharmacies and drugstores on main roads
        - Hair salons and barber shops in commercial areas
        - Restaurants and cafes serving various cuisines
        - Banks and ATMs throughout the city
        - Supermarkets and local markets for shopping
        - Internet cafes for those needing computer access
        - Transportation: bajaj, taxis, and buses readily available""",
        "source": "ASTU Area Guide",
        "tags": ["adama", "city", "services", "nearby"]
    },
    {
        "title": "Internet and ICT Services",
        "content": """ICT services at ASTU:
        - Campus-wide WiFi in academic buildings and library
        - Computer labs with internet access
        - Student email accounts provided
        - Learning Management System (LMS) for course materials
        - ICT Center provides technical support
        - Internet available in some dormitory areas
        Students receive login credentials during orientation.""",
        "source": "ASTU ICT Center",
        "tags": ["internet", "ict", "wifi", "computer"]
    },
    {
        "title": "Examination Rules and Academic Integrity",
        "content": """ASTU examination policies:
        - Student ID required for all exams
        - Arrive 15 minutes before exam start
        - No electronic devices allowed unless specified
        - Academic dishonesty (cheating, plagiarism) strictly prohibited
        - Penalties include failing grade, suspension, or expulsion
        - Mid-term exams typically 30-40% of final grade
        - Final exams 50-60% of final grade
        - Makeup exams only for documented emergencies""",
        "source": "ASTU Academic Policies",
        "tags": ["examination", "exams", "academic integrity", "rules"]
    },
    {
        "title": "Contact Information and Support",
        "content": """Important ASTU contacts:
        - Main Office: Available during business hours
        - Registrar Office: Academic records and registration
        - Student Affairs: Housing, clubs, student issues
        - ICT Center: Technical support
        - Library: Research and information services
        - Security: Emergency assistance and campus safety
        - Clinic: Health services
        Students should first contact their department office for academic matters.""",
        "source": "ASTU Directory",
        "tags": ["contact", "support", "help", "information"]
    },
    {
        "title": "Transportation to and from ASTU",
        "content": """Getting to ASTU from Addis Ababa and other cities:
        - Regular bus services from Addis Ababa to Adama (2-hour journey)
        - Buses depart from various terminals in Addis
        - Mini-buses and taxis available within Adama city
        - University shuttle may be available for special events
        - Private vehicles can access campus with parking available
        For daily commuting, students living off-campus use local transportation.""",
        "source": "ASTU Access Guide",
        "tags": ["transportation", "bus", "travel", "access"]
    }
]


async def ingest_documents():
    """Ingest knowledge documents with embeddings"""
    logger.info("Starting ASTU Knowledge Base document ingestion...")
    
    db = Database()
    ai_service = GeminiAIService()
    
    try:
        # Test connection
        if not db.test_connection():
            logger.error("Database connection failed")
            return False
        
        logger.info("✓ Database connected")
        logger.info(f"✓ AI service ready: {ai_service.model}")
        
        # Create tables
        db.create_tables()
        logger.info("✓ Tables ready")
        
        # Insert documents with embeddings
        success_count = 0
        error_count = 0
        
        for idx, doc in enumerate(KNOWLEDGE_DOCUMENTS, 1):
            try:
                logger.info(f"[{idx}/{len(KNOWLEDGE_DOCUMENTS)}] Processing: {doc['title']}")
                
                # Generate embedding for document content
                embedding = await ai_service.generate_embedding(doc['content'])
                
                if not embedding:
                    logger.error(f"Failed to generate embedding for: {doc['title']}")
                    error_count += 1
                    continue
                
                # Verify embedding dimension
                if len(embedding) != 768:
                    logger.error(f"Embedding dimension mismatch: {len(embedding)} (expected 768)")
                    error_count += 1
                    continue
                
                # Add document to database
                doc_id = await db.add_document(
                    title=doc['title'],
                    content=doc['content'],
                    source=doc['source'],
                    tags=doc.get('tags', []),
                    embedding=embedding
                )
                
                if doc_id:
                    logger.info(f"  ✓ Added document ID: {doc_id}")
                    success_count += 1
                else:
                    logger.warning(f"  ⚠ Failed to add document")
                    error_count += 1
                
                # Small delay to avoid rate limiting
                await asyncio.sleep(0.5)
                    
            except Exception as e:
                logger.error(f"  ✗ Error processing {doc['title']}: {e}")
                error_count += 1
        
        # Summary
        logger.info("\n=== Ingestion Complete ===")
        logger.info(f"Total Documents: {len(KNOWLEDGE_DOCUMENTS)}")
        logger.info(f"Successful: {success_count}")
        logger.info(f"Failed: {error_count}")
        logger.info(f"Success rate: {(success_count/len(KNOWLEDGE_DOCUMENTS)*100):.1f}%")
        
        return success_count > 0
        
    except Exception as e:
        logger.error(f"Ingestion failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("\n📚 ASTU Route AI - Knowledge Base Document Ingestion")
    print("=" * 50)
    print(f"Database: {settings.database_url[:30]}...")
    print(f"AI Model: text-embedding-004")
    print(f"Documents to ingest: {len(KNOWLEDGE_DOCUMENTS)}")
    print("=" * 50)
    print("\nThis will generate embeddings using Gemini AI...")
    print("Estimated time: ~30 seconds\n")
    
    # Run ingestion
    result = asyncio.run(ingest_documents())
    
    if result:
        print("\n✅ Ingestion completed successfully!")
        print("Knowledge base is ready for RAG queries.")
        sys.exit(0)
    else:
        print("\n❌ Ingestion failed!")
        sys.exit(1)
