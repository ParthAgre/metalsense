import sys
import os

# Add parent dir to path to allow importing app
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.services.utils.indices import calculate_hpi
from app.services.utils.risk import get_comprehensive_risk_assessment

def test_hpi_example():
    print("--- Testing HPI Calculation ---")
    # User Example: Pb = 0.02, Limit = 0.01
    # Expected HPI = 200
    concentrations = {"lead": 0.02}
    
    hpi = calculate_hpi(concentrations)
    print(f"Input: Pb=0.02 mg/L")
    print(f"Calculated HPI: {hpi}")
    
    if abs(hpi - 200.0) < 0.1:
        print("✅ HPI Logic Verified (Matches User Example)")
    else:
        print(f"❌ HPI Mismatch. Expected 200, got {hpi}")

def test_risk_assessment():
    print("\n--- Testing Risk Assessment ---")
    # Using Arsenic: 0.02 mg/L (Limit 0.01)
    # Adult params: IR=2.2, EF=365, ED=30, BW=70, AT=30*365
    # RfD(As) = 3.0E-4
    # CSF(As) = 1.5
    
    # Hand calc:
    # CDI = (0.02 * 2.2 * 365 * 30) / (70 * 30 * 365) = (0.02 * 2.2) / 70 = 0.044 / 70 = 0.00062857
    # HQ = 0.00062857 / 3.0E-4 = 2.095
    # Cancer Risk (uses AT_C=70*365):
    # CDI_C = (0.02 * 2.2 * 365 * 30) / (70 * 70 * 365) = (0.02 * 2.2 * 30) / (70 * 70) = 1.32 / 4900 = 0.00026938
    # Risk = 0.00026938 * 1.5 = 0.000404
    
    concentrations = {"arsenic": 0.02}
    assessment = get_comprehensive_risk_assessment(concentrations)
    
    adult_risk = assessment["adult"]["metals"]["arsenic"]
    
    print(f"Input: As=0.02 mg/L")
    print(f"Adult HQ: {adult_risk['HQ']}")
    print(f"Adult Cancer Risk: {adult_risk['CancerRisk']}")
    
    if abs(adult_risk["HQ"] - 2.095) < 0.01:
        print("✅ HQ Calculation Verified")
    else:
        print(f"❌ HQ Mismatch. Expected ~2.095")
        
    if abs(adult_risk["CancerRisk"] - 0.000404) < 0.00001:
        print("✅ Cancer Risk Calculation Verified")
    else:
        print(f"❌ Cancer Risk Mismatch.")

if __name__ == "__main__":
    test_hpi_example()
    test_risk_assessment()
