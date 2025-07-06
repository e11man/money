#!/usr/bin/env python3
"""
Validation script to ensure the Personal Finance Manager works correctly
"""

import os
import sys
import json
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.getcwd())

def main():
    """Main validation function"""
    print("Personal Finance Manager - Validation")
    print("=" * 50)
    
    try:
        # Test 1: Import the app
        print("\n1. Testing app import...")
        from app import app, load_data, save_data, get_default_data
        print("✓ App imported successfully")
        
        # Test 2: Test data functions
        print("\n2. Testing data functions...")
        
        # Test get_default_data
        default_data = get_default_data()
        assert 'current_money' in default_data
        assert 'budget_rules' in default_data
        assert 'income_sources' in default_data
        assert 'expense_sources' in default_data
        print("✓ get_default_data() works correctly")
        
        # Test save_data and load_data
        test_data = {
            "current_money": 1000,
            "investments": 500,
            "budget_rules": {"needs": 50, "wants": 30, "savings": 20},
            "income_sources": [],
            "expense_sources": [],
            "yearly_data": {},
            "preferences": {
                "currency": "USD",
                "date_format": "MM/DD/YYYY"
            }
        }
        
        save_data(test_data)
        loaded_data = load_data()
        assert loaded_data['current_money'] == 1000
        assert loaded_data['investments'] == 500
        print("✓ save_data() and load_data() work correctly")
        
        # Test 3: Test Flask app configuration
        print("\n3. Testing Flask app configuration...")
        with app.app_context():
            assert app.config['DATA_FILE'] == 'data/finance_data.json'
            print("✓ Flask app configuration is correct")
        
        # Test 4: Test routes exist
        print("\n4. Testing routes...")
        with app.test_client() as client:
            # Test home page
            response = client.get('/')
            assert response.status_code == 200
            print("✓ Home page route works")
            
            # Test API endpoint
            response = client.get('/api/data')
            assert response.status_code == 200
            data = json.loads(response.data)
            assert 'current_money' in data
            print("✓ API endpoint works")
            
            # Test budget rules endpoint
            response = client.get('/api/budget-rules')
            assert response.status_code == 200
            print("✓ Budget rules endpoint works")
            
            # Test projections endpoint
            response = client.get('/api/projections')
            assert response.status_code == 200
            projections = json.loads(response.data)
            assert isinstance(projections, list)
            print("✓ Projections endpoint works")
        
        # Test 5: Verify JSON file exists and is valid
        print("\n5. Testing JSON file...")
        assert os.path.exists('data/finance_data.json')
        print("✓ JSON file exists")
        
        with open('data/finance_data.json', 'r') as f:
            json_data = json.load(f)
            assert 'current_money' in json_data
            print("✓ JSON file is valid")
        
        print("\n" + "=" * 50)
        print("🎉 ALL VALIDATIONS PASSED! 🎉")
        print("✓ Application is fully functional")
        print("✓ Data persistence works correctly")
        print("✓ All routes are accessible")
        print("✓ JSON file is properly formatted")
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"\n✗ Validation failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)