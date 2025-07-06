"""
Test suite for Personal Finance Manager Flask Application
Tests all routes, data persistence, and functionality
"""

import os
import json
import pytest
import tempfile
from datetime import datetime, timedelta
from app import app, load_data, save_data, get_default_data, calculate_projections, calculate_monthly_income, calculate_monthly_expenses, calculate_source_amount


class TestFinanceApp:
    """Test class for the finance application"""

    @pytest.fixture
    def client(self):
        """Create test client"""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client

    @pytest.fixture
    def temp_data_dir(self):
        """Create temporary data directory for testing"""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_data_file = app.config.get('DATA_FILE', 'data/finance_data.json')
            app.config['DATA_FILE'] = os.path.join(tmpdir, 'test_finance_data.json')
            yield tmpdir
            app.config['DATA_FILE'] = original_data_file

    def test_home_page(self, client):
        """Test home page loads correctly"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'html' in response.data

    def test_dashboard_page(self, client):
        """Test dashboard page loads correctly"""
        response = client.get('/dashboard')
        assert response.status_code == 200
        assert b'html' in response.data

    def test_budget_page(self, client):
        """Test budget page loads correctly"""
        response = client.get('/budget')
        assert response.status_code == 200
        assert b'html' in response.data

    def test_income_page(self, client):
        """Test income page loads correctly"""
        response = client.get('/income')
        assert response.status_code == 200
        assert b'html' in response.data

    def test_expenses_page(self, client):
        """Test expenses page loads correctly"""
        response = client.get('/expenses')
        assert response.status_code == 200
        assert b'html' in response.data

    def test_investments_page(self, client):
        """Test investments page loads correctly"""
        response = client.get('/investments')
        assert response.status_code == 200
        assert b'html' in response.data

    def test_preferences_page(self, client):
        """Test preferences page loads correctly"""
        response = client.get('/preferences')
        assert response.status_code == 200
        assert b'html' in response.data

    def test_get_data_api(self, client):
        """Test GET /api/data endpoint"""
        response = client.get('/api/data')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'current_money' in data
        assert 'investments' in data
        assert 'budget_rules' in data
        assert 'income_sources' in data
        assert 'expense_sources' in data

    def test_update_data_api(self, client):
        """Test POST /api/data endpoint"""
        test_data = {
            "current_money": 1000,
            "investments": 500,
            "budget_rules": {"needs": 50, "wants": 30, "savings": 20},
            "income_sources": [],
            "expense_sources": []
        }
        response = client.post('/api/data', json=test_data)
        assert response.status_code == 200
        result = json.loads(response.data)
        assert result['status'] == 'success'

    def test_get_budget_rules(self, client):
        """Test GET /api/budget-rules endpoint"""
        response = client.get('/api/budget-rules')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'needs' in data
        assert 'wants' in data
        assert 'savings' in data

    def test_update_budget_rules(self, client):
        """Test POST /api/budget-rules endpoint"""
        rules = {"needs": 40, "wants": 35, "savings": 25}
        response = client.post('/api/budget-rules', json=rules)
        assert response.status_code == 200
        result = json.loads(response.data)
        assert result['status'] == 'success'

    def test_get_income_sources(self, client):
        """Test GET /api/income-sources endpoint"""
        response = client.get('/api/income-sources')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)

    def test_add_income_source(self, client):
        """Test POST /api/income-sources endpoint"""
        source = {
            "name": "Test Job",
            "amount": 5000,
            "type": "recurring",
            "frequency": "monthly",
            "active": True
        }
        response = client.post('/api/income-sources', json=source)
        assert response.status_code == 200
        result = json.loads(response.data)
        assert result['status'] == 'success'
        assert 'source' in result

    def test_update_income_source(self, client):
        """Test PUT /api/income-sources/<id> endpoint"""
        # First add a source
        source = {
            "name": "Test Job",
            "amount": 5000,
            "type": "recurring",
            "frequency": "monthly",
            "active": True
        }
        add_response = client.post('/api/income-sources', json=source)
        assert add_response.status_code == 200
        
        # Then update it
        update_data = {"amount": 6000}
        response = client.put('/api/income-sources/1', json=update_data)
        assert response.status_code == 200
        result = json.loads(response.data)
        assert result['status'] == 'success'

    def test_delete_income_source(self, client):
        """Test DELETE /api/income-sources/<id> endpoint"""
        # First add a source
        source = {
            "name": "Test Job",
            "amount": 5000,
            "type": "recurring",
            "frequency": "monthly",
            "active": True
        }
        add_response = client.post('/api/income-sources', json=source)
        assert add_response.status_code == 200
        
        # Then delete it
        response = client.delete('/api/income-sources/1')
        assert response.status_code == 200
        result = json.loads(response.data)
        assert result['status'] == 'success'

    def test_get_expense_sources(self, client):
        """Test GET /api/expense-sources endpoint"""
        response = client.get('/api/expense-sources')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)

    def test_add_expense_source(self, client):
        """Test POST /api/expense-sources endpoint"""
        source = {
            "name": "Test Expense",
            "amount": 500,
            "type": "recurring",
            "frequency": "monthly",
            "active": True,
            "category": "bills"
        }
        response = client.post('/api/expense-sources', json=source)
        assert response.status_code == 200
        result = json.loads(response.data)
        assert result['status'] == 'success'
        assert 'source' in result

    def test_update_expense_source(self, client):
        """Test PUT /api/expense-sources/<id> endpoint"""
        # First add a source
        source = {
            "name": "Test Expense",
            "amount": 500,
            "type": "recurring",
            "frequency": "monthly",
            "active": True,
            "category": "bills"
        }
        add_response = client.post('/api/expense-sources', json=source)
        assert add_response.status_code == 200
        
        # Then update it
        update_data = {"amount": 600}
        response = client.put('/api/expense-sources/1', json=update_data)
        assert response.status_code == 200
        result = json.loads(response.data)
        assert result['status'] == 'success'

    def test_delete_expense_source(self, client):
        """Test DELETE /api/expense-sources/<id> endpoint"""
        # First add a source
        source = {
            "name": "Test Expense",
            "amount": 500,
            "type": "recurring",
            "frequency": "monthly",
            "active": True,
            "category": "bills"
        }
        add_response = client.post('/api/expense-sources', json=source)
        assert add_response.status_code == 200
        
        # Then delete it
        response = client.delete('/api/expense-sources/1')
        assert response.status_code == 200
        result = json.loads(response.data)
        assert result['status'] == 'success'

    def test_get_projections(self, client):
        """Test GET /api/projections endpoint"""
        response = client.get('/api/projections')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) == 12  # 12 months of projections

    def test_data_persistence(self, temp_data_dir):
        """Test that data persists correctly to JSON file"""
        # Set up test data
        test_data = {
            "current_money": 1000,
            "investments": 500,
            "budget_rules": {"needs": 50, "wants": 30, "savings": 20},
            "income_sources": [
                {
                    "id": 1,
                    "name": "Test Job",
                    "amount": 5000,
                    "type": "recurring",
                    "frequency": "monthly",
                    "active": True,
                    "created_at": datetime.now().isoformat()
                }
            ],
            "expense_sources": [
                {
                    "id": 1,
                    "name": "Test Expense",
                    "amount": 500,
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
        
        # Save data
        save_data(test_data)
        
        # Load data back
        loaded_data = load_data()
        
        # Verify data matches
        assert loaded_data['current_money'] == test_data['current_money']
        assert loaded_data['investments'] == test_data['investments']
        assert loaded_data['budget_rules'] == test_data['budget_rules']
        assert len(loaded_data['income_sources']) == 1
        assert len(loaded_data['expense_sources']) == 1

    def test_default_data_structure(self):
        """Test that default data has correct structure"""
        default_data = get_default_data()
        assert 'current_money' in default_data
        assert 'investments' in default_data
        assert 'budget_rules' in default_data
        assert 'income_sources' in default_data
        assert 'expense_sources' in default_data
        assert 'yearly_data' in default_data
        assert 'preferences' in default_data
        
        # Test budget rules
        assert default_data['budget_rules']['needs'] == 50
        assert default_data['budget_rules']['wants'] == 30
        assert default_data['budget_rules']['savings'] == 20
        
        # Test preferences
        assert default_data['preferences']['currency'] == 'USD'
        assert default_data['preferences']['projection_years'] == 5

    def test_calculate_projections(self):
        """Test projection calculations"""
        test_data = {
            "current_money": 1000,
            "income_sources": [
                {
                    "name": "Job",
                    "amount": 5000,
                    "type": "recurring",
                    "frequency": "monthly",
                    "active": True
                }
            ],
            "expense_sources": [
                {
                    "name": "Rent",
                    "amount": 1500,
                    "type": "recurring",
                    "frequency": "monthly",
                    "active": True
                }
            ]
        }
        
        projections = calculate_projections(test_data)
        assert len(projections) == 12
        
        # First month should show income - expenses
        first_month = projections[0]
        assert first_month['income'] == 5000
        assert first_month['expenses'] == 1500
        assert first_month['balance'] == 1000 + 5000 - 1500  # 4500

    def test_calculate_monthly_income(self):
        """Test monthly income calculation"""
        sources = [
            {
                "name": "Job",
                "amount": 5000,
                "type": "recurring",
                "frequency": "monthly",
                "active": True
            },
            {
                "name": "Freelance",
                "amount": 1000,
                "type": "recurring",
                "frequency": "weekly",
                "active": True
            }
        ]
        
        month_date = datetime.now()
        total_income = calculate_monthly_income(sources, month_date)
        
        # Should be 5000 (monthly) + 1000 * 4.33 (weekly)
        expected = 5000 + (1000 * 4.33)
        assert abs(total_income - expected) < 0.01

    def test_calculate_monthly_expenses(self):
        """Test monthly expense calculation"""
        sources = [
            {
                "name": "Rent",
                "amount": 1500,
                "type": "recurring",
                "frequency": "monthly",
                "active": True
            },
            {
                "name": "Groceries",
                "amount": 200,
                "type": "recurring",
                "frequency": "weekly",
                "active": True
            }
        ]
        
        month_date = datetime.now()
        total_expenses = calculate_monthly_expenses(sources, month_date)
        
        # Should be 1500 (monthly) + 200 * 4.33 (weekly)
        expected = 1500 + (200 * 4.33)
        assert abs(total_expenses - expected) < 0.01

    def test_calculate_source_amount_frequencies(self):
        """Test different frequency calculations"""
        month_date = datetime.now()
        
        # Monthly
        monthly_source = {"amount": 1000, "type": "recurring", "frequency": "monthly"}
        assert calculate_source_amount(monthly_source, month_date) == 1000
        
        # Weekly
        weekly_source = {"amount": 200, "type": "recurring", "frequency": "weekly"}
        assert abs(calculate_source_amount(weekly_source, month_date) - (200 * 4.33)) < 0.01
        
        # Biweekly
        biweekly_source = {"amount": 400, "type": "recurring", "frequency": "biweekly"}
        assert abs(calculate_source_amount(biweekly_source, month_date) - (400 * 2.17)) < 0.01
        
        # Quarterly
        quarterly_source = {"amount": 3000, "type": "recurring", "frequency": "quarterly"}
        assert calculate_source_amount(quarterly_source, month_date) == 1000
        
        # Yearly
        yearly_source = {"amount": 12000, "type": "recurring", "frequency": "yearly"}
        assert calculate_source_amount(yearly_source, month_date) == 1000

    def test_calculate_source_amount_one_time(self):
        """Test one-time source calculation"""
        # Current month
        current_month = datetime.now()
        current_month_source = {
            "amount": 1000,
            "type": "one-time",
            "date": current_month.isoformat()
        }
        assert calculate_source_amount(current_month_source, current_month) == 1000
        
        # Different month
        different_month = current_month + timedelta(days=60)
        assert calculate_source_amount(current_month_source, different_month) == 0

    def test_inactive_sources(self):
        """Test that inactive sources are not included in calculations"""
        sources = [
            {
                "name": "Active Job",
                "amount": 5000,
                "type": "recurring",
                "frequency": "monthly",
                "active": True
            },
            {
                "name": "Inactive Job",
                "amount": 2000,
                "type": "recurring",
                "frequency": "monthly",
                "active": False
            }
        ]
        
        month_date = datetime.now()
        total_income = calculate_monthly_income(sources, month_date)
        
        # Should only include active source
        assert total_income == 5000