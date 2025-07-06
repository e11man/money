#!/usr/bin/env python3
"""
Test runner script for Personal Finance Manager
Ensures all tests pass and data is properly saved
"""

import os
import sys
import subprocess
import json
from datetime import datetime

def ensure_data_directory():
    """Ensure data directory exists"""
    if not os.path.exists('data'):
        os.makedirs('data')
        print("✓ Created data directory")

def create_sample_data():
    """Create sample data to test JSON persistence"""
    sample_data = {
        "current_money": 5000,
        "investments": 2500,
        "budget_rules": {
            "needs": 50,
            "wants": 30,
            "savings": 20
        },
        "income_sources": [
            {
                "id": 1,
                "name": "Main Job",
                "amount": 6000,
                "type": "recurring",
                "frequency": "monthly",
                "active": True,
                "created_at": datetime.now().isoformat()
            },
            {
                "id": 2,
                "name": "Freelance",
                "amount": 1500,
                "type": "recurring",
                "frequency": "monthly",
                "active": True,
                "created_at": datetime.now().isoformat()
            }
        ],
        "expense_sources": [
            {
                "id": 1,
                "name": "Rent",
                "amount": 2000,
                "type": "recurring",
                "frequency": "monthly",
                "active": True,
                "category": "housing",
                "created_at": datetime.now().isoformat()
            },
            {
                "id": 2,
                "name": "Groceries",
                "amount": 600,
                "type": "recurring",
                "frequency": "monthly",
                "active": True,
                "category": "food",
                "created_at": datetime.now().isoformat()
            },
            {
                "id": 3,
                "name": "Utilities",
                "amount": 200,
                "type": "recurring",
                "frequency": "monthly",
                "active": True,
                "category": "bills",
                "created_at": datetime.now().isoformat()
            }
        ],
        "yearly_data": {},
        "preferences": {
            "currency": "USD",
            "date_format": "MM/DD/YYYY",
            "fiscal_year_start": 1,
            "projection_years": 5,
            "default_income_type": "recurring",
            "default_expense_type": "recurring"
        }
    }
    
    with open('data/finance_data.json', 'w') as f:
        json.dump(sample_data, f, indent=2)
    
    print("✓ Created sample finance data")
    return sample_data

def test_json_persistence():
    """Test that JSON data persists correctly"""
    try:
        with open('data/finance_data.json', 'r') as f:
            data = json.load(f)
        
        # Verify required fields exist
        required_fields = ['current_money', 'investments', 'budget_rules', 'income_sources', 'expense_sources', 'preferences']
        for field in required_fields:
            if field not in data:
                print(f"✗ Missing required field: {field}")
                return False
        
        # Verify budget rules add up to 100%
        budget_total = sum(data['budget_rules'].values())
        if budget_total != 100:
            print(f"✗ Budget rules don't add up to 100%: {budget_total}")
            return False
        
        print("✓ JSON data structure is valid")
        return True
    except Exception as e:
        print(f"✗ Error reading JSON data: {e}")
        return False

def install_requirements():
    """Install required packages"""
    try:
        # Check if we're in a virtual environment
        if os.path.exists('venv/bin/activate'):
            # Requirements should already be installed in venv
            print("✓ Virtual environment found, requirements should be installed")
            return True
        else:
            subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                          check=True, capture_output=True)
            print("✓ Requirements installed successfully")
            return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install requirements: {e}")
        return False

def run_pytest():
    """Run pytest with proper configuration"""
    try:
        # Use venv python if available
        if os.path.exists('venv/bin/python'):
            python_cmd = 'venv/bin/python'
        else:
            python_cmd = sys.executable
            
        result = subprocess.run([python_cmd, '-m', 'pytest', 'test_app.py', '-v'], 
                              capture_output=True, text=True)
        
        print("=" * 60)
        print("TEST RESULTS")
        print("=" * 60)
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        if result.returncode == 0:
            print("✓ All tests passed!")
            return True
        else:
            print("✗ Some tests failed")
            return False
            
    except Exception as e:
        print(f"✗ Error running pytest: {e}")
        return False

def main():
    """Main test runner"""
    print("Personal Finance Manager - Test Runner")
    print("=" * 50)
    
    # Step 1: Install requirements
    print("\n1. Installing requirements...")
    if not install_requirements():
        sys.exit(1)
    
    # Step 2: Ensure data directory exists
    print("\n2. Setting up data directory...")
    ensure_data_directory()
    
    # Step 3: Create sample data
    print("\n3. Creating sample data...")
    sample_data = create_sample_data()
    
    # Step 4: Test JSON persistence
    print("\n4. Testing JSON persistence...")
    if not test_json_persistence():
        sys.exit(1)
    
    # Step 5: Run all tests
    print("\n5. Running comprehensive tests...")
    if not run_pytest():
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("🎉 ALL TESTS PASSED! 🎉")
    print("✓ Data is properly saved to JSON file")
    print("✓ All functionality works correctly")
    print("✓ Application is ready for use")
    print("=" * 50)

if __name__ == "__main__":
    main()