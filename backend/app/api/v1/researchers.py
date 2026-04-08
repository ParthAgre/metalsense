from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.api import deps
from app.schemas.water_quality import CreateSample
from app.db.models.sample import Sample, Measurement
from app.db.models.dataset import Dataset
from fastapi import UploadFile, File
import pandas as pd
import io
from app.services.tasks import calculate_risk_indices_task

router = APIRouter()

@router.post("/samples", status_code=202)
async def create_sample(
    payload: CreateSample, 
    background_tasks: BackgroundTasks, 
    db: Session = Depends(get_db),
    current_user = Depends(deps.get_current_researcher)
):
    try:
        # 1. Create the Sample (The 'Where' and 'When')
        # We use simple lat, lng because we switched to SQLite
        new_sample = Sample(
            lat=payload.latitude,
            lng=payload.longitude,
            timestamp=payload.timestamp,
            source_type=payload.source_type,
            standard_preference=payload.standard_preference
        )
        db.add(new_sample)
        db.flush()  # Push to DB to get the new_sample.id without committing yet

        # 2. Create the Measurements (The 'What')
        # Your Pydantic model already normalized these to mg/L
        print(f"DEBUG: Full Pydantic Payload: {payload.model_dump()}")
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

@router.post("/upload-csv", status_code=202)
async def upload_csv(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(deps.get_current_researcher)
):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")

    contents = await file.read()
    try:
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid CSV format: {str(e)}")

    dataset = Dataset(uploader_id=current_user.id, filename=file.filename, upload_status="processing")
    db.add(dataset)
    db.flush()

    try:
        sample_ids = []
        # Support flexible column names
        cols = {c.lower(): c for c in df.columns}
        lat_col = cols.get('lat') or cols.get('latitude')
        lng_col = cols.get('lng') or cols.get('longitude') or cols.get('long')
        time_col = cols.get('timestamp') or cols.get('date') or cols.get('sampling_date')
        source_col = cols.get('source_type') or cols.get('source')
        metal_col = cols.get('metal') or cols.get('element')
        conc_col = cols.get('concentration') or cols.get('value') or cols.get('conc')

        for index, row in df.iterrows():
            try:
                # Extract coordinates
                lat_val = float(row.get(lat_col, 0.0)) if lat_col else 0.0
                lng_val = float(row.get(lng_col, 0.0)) if lng_col else 0.0
                
                # Create Sample
                sample = Sample(
                    dataset_id=dataset.id,
                    lat=lat_val,
                    lng=lng_val,
                    timestamp=pd.to_datetime(row.get(time_col, pd.Timestamp.now())) if time_col else pd.Timestamp.now(),
                    source_type=row.get(source_col, 'Groundwater'),
                )
                db.add(sample)
                db.flush()
                
                # Create Measurement
                metal_val = str(row.get(metal_col, 'Unknown')) if metal_col else 'Unknown'
                conc_val = float(row.get(conc_col, 0.0)) if conc_col else 0.0
                
                measurement = Measurement(
                    sample_id=sample.id,
                    metal=metal_val,
                    concentration=conc_val
                )
                db.add(measurement)
                sample_ids.append(sample.id)
            except Exception as row_err:
                print(f"Skipping row {index} due to error: {row_err}")
                continue
            
        if not sample_ids:
            raise Exception("No valid rows found in CSV")

        dataset.upload_status = "completed"
        db.commit()
        
        for sid in sample_ids:
            background_tasks.add_task(calculate_risk_indices_task, sid)

        return {"status": "Success", "dataset_id": dataset.id, "message": f"CSV processed. {len(sample_ids)} samples imported."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Processing Error: {str(e)}")

@router.get("/samples")
def get_samples(db: Session = Depends(get_db)):
    samples = db.query(Sample).all()
    # Eager load related measurements and assessments manually or just return simple dict
    result = []
    for s in samples:
        measurements = [{"metal": m.metal, "concentration": m.concentration} for m in s.measurements]
        risk = s.assessment
        result.append({
            "id": s.id,
            "lat": s.lat,
            "lng": s.lng,
            "timestamp": s.timestamp,
            "source_type": s.source_type,
            "measurements": measurements,
            "risk": {
                "hpi": risk.hpi if risk else None,
                "risk_category": risk.risk_category if risk else "Safe"
            }
        })
    return result