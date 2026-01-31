from sqlalchemy.orm import Session
from app.db.models.sample import Sample, Measurement
from app.db.models.risk import RiskAssessment
from app.services.calculator import EnvironmentalCalculator
from app.db.database import SessionLocal



def calculate_risk_indices_task(sample_id: int):
    """
    Background task to fetch raw data, compute indices, and persist results.
    """
    db = SessionLocal()
    try:
        # 1. Fetch the sample and its measurements
        sample = db.query(Sample).filter(Sample.id == sample_id).first()
        if not sample:
            return

        name_mapping = {
            "As": "arsenic", "Pb": "lead", "Cd": "cadmium", 
            "Hg": "mercury", "Cr": "chromium", "Ni": "nickel",
            "Zn": "zinc", "Cu": "copper", "Fe": "iron", "Mn": "manganese"
        }

        # Update the transformation loop
        raw_data = {
            name_mapping.get(m.metal, m.metal.lower()): m.concentration 
            for m in sample.measurements
        }


        # 3. Perform the Scientific Calculations
        calc = EnvironmentalCalculator()
        hpi_score = calc.calculate_hpi(raw_data)
        hei_score = calc.calculate_hei(raw_data)
        
        # Calculate max I-geo among all metals provided
        i_geo_values = [calc.calculate_i_geo(m, c) for m, c in raw_data.items()]
        max_i_geo = max(i_geo_values) if i_geo_values else 0.0
        
        # Health Risk Assessment for children (the most vulnerable group)
        health_results = calc.calculate_health_risk(raw_data, group="child")

        # 4. Determine Risk Category for Citizens
        # [cite_start]Based on HPI threshold of 100 [cite: 126, 169]
        category = "Safe"
        if hpi_score > 100:
            category = "Hazardous"
        elif hpi_score > 50:
            category = "Moderately Polluted"

        # 5. Persist the results in the RiskAssessment table
        assessment = RiskAssessment(
            sample_id=sample.id,
            hpi=hpi_score,
            hei=hei_score,
            i_geo_max=max_i_geo,
            hazard_index=health_results["hazard_index"],
            cancer_risk=health_results["cancer_risk"],
            risk_category=category,
            is_safe=(hpi_score <= 100)
        )
        
        db.add(assessment)
        db.commit()
        print(f"✅ Risk Assessment completed for Sample ID: {sample_id}")

    except Exception as e:
        print(f"❌ Error in background task: {e}")
        db.rollback()
    finally:
        db.close()