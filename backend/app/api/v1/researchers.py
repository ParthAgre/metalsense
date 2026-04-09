from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.database import get_db
from app.api import deps
from app.schemas.water_quality import CreateSample
from app.db.models.sample import Sample, Measurement
from app.db.models.dataset import Dataset
from app.db.models.risk import RiskAssessment
from fastapi import UploadFile, File
import pandas as pd
import io
import re
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
        # Check for duplicates
        existing = db.query(Sample).filter(
            Sample.lat == payload.latitude,
            Sample.lng == payload.longitude,
            Sample.timestamp == payload.timestamp
        ).first()
        
        if existing:
             raise HTTPException(status_code=400, detail="A sample at this location and time already exists.")

        new_sample = Sample(
            lat=payload.latitude,
            lng=payload.longitude,
            timestamp=payload.timestamp,
            source_type=payload.source_type,
            standard_preference=payload.standard_preference
        )
        db.add(new_sample)
        db.flush()

        db_measurements = [
            Measurement(
                sample_id=new_sample.id,
                metal=m.metal,
                concentration=m.concentration
            )
            for m in payload.measurements
        ]

        db.add_all(db_measurements)
        db.commit()
        db.refresh(new_sample)

        background_tasks.add_task(calculate_risk_indices_task, new_sample.id)

        return {
            "status": "Accepted", 
            "sample_id": new_sample.id, 
            "message": "Calculation in progress"
        }

    except HTTPException:
        raise
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
        
        # Identify coordinate and metadata columns
        lat_col = next((c for c in df.columns if 'lat' in c.lower()), None)
        lng_col = next((c for c in df.columns if 'long' in c.lower() or 'lng' in c.lower()), None)
        time_col = next((c for c in df.columns if 'year' in c.lower() or 'date' in c.lower() or 'time' in c.lower()), None)
        loc_col = next((c for c in df.columns if 'location' in c.lower() or 'site' in c.lower()), None)
        state_col = next((c for c in df.columns if 'state' in c.lower()), None)
        dist_col = next((c for c in df.columns if 'district' in c.lower()), None)
        
        # Identify metal columns (e.g. As (ppb), Fe (ppm))
        metal_cols = [c for c in df.columns if '(ppb)' in c.lower() or '(ppm)' in c.lower()]

        for index, row in df.iterrows():
            try:
                lat_val = float(row.get(lat_col, 0.0)) if lat_col else 0.0
                lng_val = float(row.get(lng_col, 0.0)) if lng_col else 0.0
                loc_val = str(row.get(loc_col, 'Unknown')) if loc_col else 'Unknown'
                state_val = str(row.get(state_col, 'Unknown')) if state_col else 'Unknown'
                dist_val = str(row.get(dist_col, 'Unknown')) if dist_col else 'Unknown'
                
                # Deduce timestamp (if only Year is provided, use Jan 1st)
                raw_time = row.get(time_col)
                if time_col and 'year' in time_col.lower() and str(raw_time).isdigit():
                    timestamp = pd.Timestamp(year=int(raw_time), month=1, day=1)
                elif time_col:
                    timestamp = pd.to_datetime(raw_time, errors='coerce') or pd.Timestamp.now()
                else:
                    timestamp = pd.Timestamp.now()

                # Duplicate Check
                existing = db.query(Sample).filter(
                    Sample.lat == lat_val,
                    Sample.lng == lng_val,
                    Sample.timestamp == timestamp,
                    Sample.location_name == loc_val
                ).first()
                if existing:
                    print(f"Skipping duplicate at row {index}: {loc_val}")
                    continue

                sample = Sample(
                    dataset_id=dataset.id,
                    lat=lat_val,
                    lng=lng_val,
                    location_name=loc_val,
                    state=state_val,
                    district=dist_val,
                    timestamp=timestamp,
                    source_type="Groundwater" # Default
                )
                db.add(sample)
                db.flush()
                
                # Process each metal column
                for col in metal_cols:
                    val = row.get(col)
                    if pd.isna(val) or val == '-':
                        continue
                    
                    try:
                        conc = float(val)
                        if '(ppb)' in col.lower():
                            conc = conc / 1000.0 # ppb to mg/L
                        
                        metal_name = re.split(r'\(', col)[0].strip()
                        
                        measurement = Measurement(
                            sample_id=sample.id,
                            metal=metal_name,
                            concentration=conc
                        )
                        db.add(measurement)
                    except ValueError:
                        continue

                sample_ids.append(sample.id)
            except Exception as row_err:
                print(f"Skipping row {index} due to error: {row_err}")
                continue
            
        if not sample_ids:
            db.delete(dataset)
            db.commit()
            return {"status": "Complete", "message": "No new data found or all entries were duplicates."}

        dataset.upload_status = "completed"
        db.commit()
        
        for sid in sample_ids:
            background_tasks.add_task(calculate_risk_indices_task, sid)

        return {"status": "Success", "dataset_id": dataset.id, "message": f"CSV processed. {len(sample_ids)} new samples imported."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Processing Error: {str(e)}")

@router.get("/uploads")
def get_my_uploads(db: Session = Depends(get_db), current_user = Depends(deps.get_current_researcher)):
    return db.query(Dataset).filter(Dataset.uploader_id == current_user.id).all()

@router.delete("/uploads/{dataset_id}")
def delete_upload(dataset_id: int, db: Session = Depends(get_db), current_user = Depends(deps.get_current_researcher)):
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id, Dataset.uploader_id == current_user.id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found or unauthorized")
    
    db.delete(dataset)
    db.commit()
    return {"message": "Dataset and associated samples deleted successfully"}

@router.get("/samples")
def get_samples(db: Session = Depends(get_db), uploader_id: int = None):
    query = db.query(Sample)
    if uploader_id:
        query = query.join(Dataset).filter(Dataset.uploader_id == uploader_id)
    
    samples = query.all()
    result = []
    for s in samples:
        measurements = [{"metal": m.metal, "concentration": m.concentration} for m in s.measurements]
        risk = s.assessment
        result.append({
            "id": s.id,
            "lat": s.lat,
            "lng": s.lng,
            "location_name": s.location_name,
            "state": s.state,
            "district": s.district,
            "timestamp": s.timestamp,
            "source_type": s.source_type,
            "measurements": measurements,
            "risk": {
                "hpi": risk.hpi if risk else None,
                "mi": risk.mi if risk else None,
                "risk_category": risk.risk_category if risk else "Safe"
            }
        })
    return result

@router.get("/dashboard-stats")
def get_dashboard_stats(db: Session = Depends(get_db), current_user = Depends(deps.get_current_researcher)):
    # Get all samples uploaded by this researcher
    samples = db.query(Sample).join(Dataset).filter(Dataset.uploader_id == current_user.id).all()
    sample_ids = [s.id for s in samples]
    
    if not sample_ids:
        return {
            "total_samples": 0,
            "avg_hpi": 0,
            "risk_distribution": {"Safe": 0, "Low Risk": 0, "High Risk": 0},
            "recent_uploads": [],
            "metal_averages": []
        }

    # Fetch risk assessments
    assessments = db.query(RiskAssessment).filter(RiskAssessment.sample_id.in_(sample_ids)).all()
    
    avg_hpi = sum(a.hpi for a in assessments if a.hpi) / len(assessments) if assessments else 0
    avg_mi = sum(a.mi for a in assessments if a.mi) / len(assessments) if assessments else 0
    
    risk_dist = {"Safe": 0, "Moderately Polluted": 0, "Hazardous": 0}
    for a in assessments:
        cat = a.risk_category or "Safe"
        risk_dist[cat] = risk_dist.get(cat, 0) + 1

    # Metal averages
    measurements = db.query(Measurement.metal, func.avg(Measurement.concentration)).filter(Measurement.sample_id.in_(sample_ids)).group_by(Measurement.metal).all()
    metal_avgs = [{"name": m[0], "value": m[1]} for m in measurements]

    return {
        "total_samples": len(samples),
        "avg_hpi": round(avg_hpi, 2),
        "avg_mi": round(avg_mi, 2),
        "risk_distribution": risk_dist,
        "metal_averages": metal_avgs,
        "latest_site": samples[0].location_name if samples else "N/A"
    }