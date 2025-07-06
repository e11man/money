"""
Personal Finance Manager - Flask Application
A comprehensive personal finance management application with Apple-inspired design
"""

import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import json
from datetime import datetime, timedelta
import calendar

# Initialize Flask application
app = Flask(__name__)
CORS(app)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'

# Data storage (in production, use a proper database)
app.config['DATA_FILE'] = 'data/finance_data.json'

def ensure_data_directory():
    """Ensure data directory exists"""
    data_file = app.config.get('DATA_FILE', 'data/finance_data.json')
    data_dir = os.path.dirname(data_file)
    if data_dir and not os.path.exists(data_dir):
        os.makedirs(data_dir)

def load_data():
    """Load finance data from file"""
    ensure_data_directory()
    data_file = app.config.get('DATA_FILE', 'data/finance_data.json')
    try:
        with open(data_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return get_default_data()

def save_data(data):
    """Save finance data to file"""
    ensure_data_directory()
    data_file = app.config.get('DATA_FILE', 'data/finance_data.json')
    with open(data_file, 'w') as f:
        json.dump(data, f, indent=2)

def get_default_data():
    """Get default finance data structure"""
    return {
        "current_money": 0,
        "investments": 0,
        "budget_rules": {
            "needs": 50,
            "wants": 30,
            "savings": 20
        },
        "income_sources": [],
        "expense_sources": [],
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

# Routes
@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """Dashboard page"""
    return render_template('dashboard.html')

@app.route('/budget')
def budget():
    """Budget planning page"""
    return render_template('budget.html')

@app.route('/income')
def income():
    """Income management page"""
    return render_template('income.html')

@app.route('/expenses')
def expenses():
    """Expense management page"""
    return render_template('expenses.html')

@app.route('/investments')
def investments():
    """Investment tracking page"""
    return render_template('investments.html')

@app.route('/preferences')
def preferences():
    """User preferences page"""
    return render_template('preferences.html')

# API Routes
@app.route('/api/data', methods=['GET'])
def get_data():
    """Get all finance data"""
    return jsonify(load_data())

@app.route('/api/data', methods=['POST'])
def update_data():
    """Update finance data"""
    data = request.get_json()
    save_data(data)
    return jsonify({"status": "success"})

@app.route('/api/budget-rules', methods=['GET'])
def get_budget_rules():
    """Get budget rules"""
    data = load_data()
    return jsonify(data['budget_rules'])

@app.route('/api/budget-rules', methods=['POST'])
def update_budget_rules():
    """Update budget rules"""
    rules = request.get_json()
    data = load_data()
    data['budget_rules'] = rules
    save_data(data)
    return jsonify({"status": "success"})

@app.route('/api/income-sources', methods=['GET'])
def get_income_sources():
    """Get all income sources"""
    data = load_data()
    return jsonify(data['income_sources'])

@app.route('/api/income-sources', methods=['POST'])
def add_income_source():
    """Add new income source"""
    source = request.get_json()
    data = load_data()
    source['id'] = len(data['income_sources']) + 1
    source['created_at'] = datetime.now().isoformat()
    data['income_sources'].append(source)
    save_data(data)
    return jsonify({"status": "success", "source": source})

@app.route('/api/income-sources/<int:source_id>', methods=['PUT'])
def update_income_source(source_id):
    """Update income source"""
    updated_source = request.get_json()
    data = load_data()
    for i, source in enumerate(data['income_sources']):
        if source['id'] == source_id:
            data['income_sources'][i] = {**source, **updated_source}
            break
    save_data(data)
    return jsonify({"status": "success"})

@app.route('/api/income-sources/<int:source_id>', methods=['DELETE'])
def delete_income_source(source_id):
    """Delete income source"""
    data = load_data()
    data['income_sources'] = [s for s in data['income_sources'] if s['id'] != source_id]
    save_data(data)
    return jsonify({"status": "success"})

@app.route('/api/expense-sources', methods=['GET'])
def get_expense_sources():
    """Get all expense sources"""
    data = load_data()
    return jsonify(data['expense_sources'])

@app.route('/api/expense-sources', methods=['POST'])
def add_expense_source():
    """Add new expense source"""
    source = request.get_json()
    data = load_data()
    source['id'] = len(data['expense_sources']) + 1
    source['created_at'] = datetime.now().isoformat()
    data['expense_sources'].append(source)
    save_data(data)
    return jsonify({"status": "success", "source": source})

@app.route('/api/expense-sources/<int:source_id>', methods=['PUT'])
def update_expense_source(source_id):
    """Update expense source"""
    updated_source = request.get_json()
    data = load_data()
    for i, source in enumerate(data['expense_sources']):
        if source['id'] == source_id:
            data['expense_sources'][i] = {**source, **updated_source}
            break
    save_data(data)
    return jsonify({"status": "success"})

@app.route('/api/expense-sources/<int:source_id>', methods=['DELETE'])
def delete_expense_source(source_id):
    """Delete expense source"""
    data = load_data()
    data['expense_sources'] = [s for s in data['expense_sources'] if s['id'] != source_id]
    save_data(data)
    return jsonify({"status": "success"})

@app.route('/api/projections', methods=['GET'])
def get_projections():
    """Get balance projections"""
    data = load_data()
    projections = calculate_projections(data)
    return jsonify(projections)

def calculate_projections(data):
    """Calculate balance projections for future months"""
    projections = []
    current_balance = data['current_money']
    
    for month_offset in range(12):  # Project 12 months ahead
        month_date = datetime.now() + timedelta(days=30 * month_offset)
        month_key = month_date.strftime("%Y-%m")
        
        monthly_income = calculate_monthly_income(data['income_sources'], month_date)
        monthly_expenses = calculate_monthly_expenses(data['expense_sources'], month_date)
        
        current_balance += monthly_income - monthly_expenses
        
        projections.append({
            "month": month_key,
            "balance": current_balance,
            "income": monthly_income,
            "expenses": monthly_expenses
        })
    
    return projections

def calculate_monthly_income(sources, month_date):
    """Calculate total monthly income for a given month"""
    total = 0
    for source in sources:
        if source.get('active', True):
            total += calculate_source_amount(source, month_date)
    return total

def calculate_monthly_expenses(sources, month_date):
    """Calculate total monthly expenses for a given month"""
    total = 0
    for source in sources:
        if source.get('active', True):
            total += calculate_source_amount(source, month_date)
    return total

def calculate_source_amount(source, month_date):
    """Calculate the amount for a source in a given month"""
    source_type = source.get('type', 'recurring')
    amount = source.get('amount', 0)
    
    if source_type == 'one-time':
        # Check if this is the specific month
        target_date = datetime.fromisoformat(source.get('date', ''))
        if target_date.year == month_date.year and target_date.month == month_date.month:
            return amount
    elif source_type == 'recurring':
        frequency = source.get('frequency', 'monthly')
        if frequency == 'weekly':
            return amount * 4.33  # Average weeks per month
        elif frequency == 'biweekly':
            return amount * 2.17  # Average biweekly periods per month
        elif frequency == 'monthly':
            return amount
        elif frequency == 'quarterly':
            return amount / 3
        elif frequency == 'yearly':
            return amount / 12
    
    return 0

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001) 