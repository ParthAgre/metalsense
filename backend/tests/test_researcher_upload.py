import time
from app.db.database import SessionLocal, init_db
from app.schemas.water_quality import CreateSample, MetalConcentration
from app.api.v1.researchers import create_sample
from fastapi import BackgroundTasks
from app.db.models.risk import RiskAssessment
import asyncio

async def test_full_pipeline():
    # 1. Initialize DB and Session
    init_db()
    db = SessionLocal()
    bg_tasks = BackgroundTasks()

    # 2. Mock Researcher Data (Aligarh Hotspot)
    test_data = CreateSample(
        latitude=27.8974,
        longitude=78.0880,
        source_type="Groundwater",
        standard_preference="BIS",
        measurements=[
            MetalConcentration(metal="Ni", concentration=1.87, unit="mg/L"),
            MetalConcentration(metal="Cu", concentration=980, unit="µg/L") # Testing unit conversion!
        ]
    )

    print("🚀 Sending Sample to API...")
    try:
        # 3. Call the route logic
        # Note: In a real test, you'd use TestClient, but this tests the logic directly
        response = await create_sample(payload=test_data, background_tasks=bg_tasks, db=db)
        
        # 4. Manually run the background tasks (since we aren't in a real FastAPI loop)
        for task in bg_tasks.tasks:
            task.func(*task.args, **task.kwargs)

        # 5. Verify the Results
        time.sleep(1) # Give it a second to commit
        assessment = db.query(RiskAssessment).order_by(RiskAssessment.id.desc()).first()
        
        if assessment:
            print(f"✅ Success! Sample ID: {assessment.sample_id}")
            print(f"📊 HPI Score: {assessment.hpi:.2f}")
            print(f"⚠️ Risk Category: {assessment.risk_category}")
            print(f"👶 Child Cancer Risk: {assessment.cancer_risk:.2e}")
        else:
            print("❌ Failure: No RiskAssessment record found.")

    except Exception as e:
        print(f"❌ Pipeline Test Failed: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    # Use asyncio to run the async function
    asyncio.run(test_full_pipeline())