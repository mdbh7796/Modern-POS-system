import sys
import os
sys.path.append(os.getcwd())
from services.currency_service import CurrencyService

def verify_phase_5():
    print("Starting Phase 5 verification...")
    
    svc = CurrencyService()
    
    # Test USD (Default)
    assert svc.convert(100) == 100.0
    assert svc.format(100) == "$100.00"
    print("Currency: USD OK")
    
    # Test MAD
    svc.set_currency('MAD')
    # Rate 10.0
    assert svc.convert(10) == 100.0 
    assert svc.format(10) == "100.00 DH"
    print("Currency: MAD OK")
    
    # Test EUR
    svc.set_currency('EUR')
    # Rate 0.95
    assert svc.convert(100) == 95.0
    assert svc.format(100) == "€95.00"
    print("Currency: EUR OK")
    
    print("PHASE 5 VERIFICATION COMPLETE")

if __name__ == "__main__":
    verify_phase_5()
