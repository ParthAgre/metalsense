from app.db.database import SessionLocal, init_db
from app.db.models.sample import Sample
from datetime import datetime
from geoalchemy2.elements import WKTElement

def test_gis_insertion():
    init_db() # Run your table creation
    db = SessionLocal()
    try:
        # Create a dummy sample in Delhi (approx coordinates)
        dummy_sample = Sample(
            location=WKTElement('POINT(77.2090 28.6139)', srid=4326),
            timestamp=datetime.now(),
            source_type="Groundwater",
            standard_preference="BIS"
        )
        db.add(dummy_sample)
        db.commit()
        print("🚀 PostGIS Insertion Successful!")
    except Exception as e:
        print(f"❌ GIS Test Failed: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_gis_insertion()