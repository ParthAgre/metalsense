from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.sample import CreateSample
from app.db.models.sample import Sample, Measurement
from geoalchemy2.elements import WKTElement
from app.services.tasks import calculate_risk_indices_task

router = APIRouter()

@router.post("/samples", status_code=202)
async def create_sample(
    payload: CreateSample, 
    background_tasks: BackgroundTasks, 
    db: Session = Depends(get_db)
):
    try:
        # 1. Create the Sample (The 'Where' and 'When')
        # We use WKTElement to store the location as a PostGIS point [cite: 141, 156]
        new_sample = Sample(
            location=WKTElement(f'POINT({payload.longitude} {payload.latitude})', srid=4326),
            timestamp=payload.timestamp,
            source_type=payload.source_type,
            standard_preference=payload.standard_preference
        )
        db.add(new_sample)
        db.flush()  # Push to DB to get the new_sample.id without committing yet

        # 2. Create the Measurements (The 'What')
        # Your Pydantic model already normalized these to mg/L
        db_measurements = [
            Measurement(
                sample_id=new_sample.id,
                metal=m.metal,
                concentration=m.concentration
            )
            for m in payload.measurements
        ]
        db.add_all(db_measurements)
        
        # 3. Commit the transaction
        db.commit()
        db.refresh(new_sample)

        # 4. Trigger the Brain (Background Task)
        background_tasks.add_task(calculate_risk_indices_task, new_sample.id)

        return {
            "status": "Accepted", 
            "sample_id": new_sample.id, 
            "message": "Calculation in progress"
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")