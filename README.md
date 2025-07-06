# MoneyWise - Personal Finance Manager

A comprehensive personal finance management application with an elegant, Apple-inspired design. Built with Flask backend and modern web technologies.

![MoneyWise Logo](https://img.shields.io/badge/MoneyWise-Personal%20Finance-blue)
![Flask](https://img.shields.io/badge/Flask-2.3.2-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🌟 Features

### 📊 Budget Planning
- **Customizable Budget Rules**: Use the proven 50/30/20 method or create your own rules
- **Visual Budget Breakdown**: Beautiful charts showing your spending plan
- **Budget vs. Actual Comparison**: Track how well you're sticking to your budget
- **Quick Presets**: Conservative, Balanced, and Aggressive Savings presets

### 💰 Income Management
- **Flexible Income Sources**: Add multiple income streams with different schedules
- **Income Types Supported**:
  - **Recurring**: Weekly, biweekly, monthly, quarterly, yearly
  - **One-time**: Single payments (bonuses, gifts)
  - **Specific Months**: Seasonal work or irregular income
  - **Monthly Until**: Income that ends on a specific date
- **Income Tracking**: Monitor total monthly income and active/inactive sources

### 💳 Expense Management
- **Categorized Expenses**: Organize expenses into Needs, Wants, and Savings
- **Flexible Expense Types**: Same scheduling options as income
- **Visual Categories**: Color-coded expense tracking by category
- **Expense Guidelines**: Built-in tips for categorizing expenses correctly

### 📈 Investment Tracking
- **Portfolio Monitoring**: Track current investment value and expected ROI
- **Growth Projections**: See how your investments will grow over time
- **Compound Interest Calculator**: Factor in regular monthly contributions
- **Investment Guidelines**: Expected returns by asset class and best practices

### 🎯 Balance Projections
- **Automatic Calculations**: Future balance projections based on income and expenses
- **12-Month Forecasting**: See your financial trajectory for the next year
- **Visual Charts**: Interactive charts showing balance trends over time
- **Real-time Updates**: Projections update automatically when you change data

### ⚙️ Customization & Settings
- **Multi-Currency Support**: USD, EUR, GBP, CAD, AUD, JPY
- **Date Format Options**: US, UK, and ISO formats
- **Fiscal Year Settings**: Customize your financial year start
- **Data Management**: Export/import data, reset functionality

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/moneywise.git
   cd moneywise
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

## 📱 Screenshots

### Dashboard
The main dashboard provides a comprehensive overview of your financial status with interactive charts and key metrics.

### Budget Planning
Create and customize your budget using proven methods or your own rules with real-time validation.

### Income & Expense Management
Flexible forms for adding various types of income and expense sources with detailed scheduling options.

### Investment Tracking
Monitor your portfolio and see compound growth projections with interactive charts.

## 🛠️ Technical Details

### Backend
- **Framework**: Flask 2.3.2
- **Data Storage**: JSON files (easily migrable to database)
- **CORS Support**: Enabled for development
- **Error Handling**: Comprehensive error handling and validation

### Frontend
- **Design**: Apple-inspired UI with clean, modern aesthetics
- **Charts**: Chart.js for interactive data visualizations
- **Responsive**: Mobile-friendly design
- **Accessibility**: Proper form labels and semantic HTML

### Data Structure
```json
{
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
    "projection_years": 5
  }
}
```

## 🎨 Design Philosophy

MoneyWise follows Apple's design principles:

- **Simplicity**: Clean, uncluttered interface focusing on essential information
- **Consistency**: Consistent color scheme, typography, and interaction patterns
- **Visual Hierarchy**: Clear information hierarchy with proper use of typography and spacing
- **Feedback**: Immediate visual feedback for user actions
- **Accessibility**: High contrast ratios and semantic HTML structure

### Color Palette
- **Primary Blue**: #007AFF (iOS system blue)
- **Success Green**: #28a745
- **Warning Yellow**: #ffc107
- **Danger Red**: #dc3545
- **Secondary Gray**: #6c757d

## 📊 API Endpoints

### Data Management
- `GET /api/data` - Retrieve all financial data
- `POST /api/data` - Update all financial data

### Budget Rules
- `GET /api/budget-rules` - Get current budget rules
- `POST /api/budget-rules` - Update budget rules

### Income Sources
- `GET /api/income-sources` - Get all income sources
- `POST /api/income-sources` - Add new income source
- `PUT /api/income-sources/<id>` - Update income source
- `DELETE /api/income-sources/<id>` - Delete income source

### Expense Sources
- `GET /api/expense-sources` - Get all expense sources
- `POST /api/expense-sources` - Add new expense source
- `PUT /api/expense-sources/<id>` - Update expense source
- `DELETE /api/expense-sources/<id>` - Delete expense source

### Projections
- `GET /api/projections` - Get balance projections

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory:

```env
SECRET_KEY=your-secret-key-here
FLASK_DEBUG=True
FLASK_ENV=development
```

### Development Setup
```bash
# Install development dependencies
pip install -r requirements.txt

# Run in debug mode
export FLASK_DEBUG=1
python app.py
```

### Production Deployment
```bash
# Install production server
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 📈 Usage Guide

### Getting Started
1. **Set Your Budget**: Start by configuring your budget rules in the Budget Planning section
2. **Add Income Sources**: Set up all your income streams with appropriate scheduling
3. **Track Expenses**: Add your regular expenses and categorize them properly
4. **Monitor Investments**: Update your investment information for complete tracking
5. **Review Dashboard**: Use the dashboard to monitor your financial health

### Best Practices
- Update your current balance regularly for accurate projections
- Review and adjust your budget monthly based on actual spending
- Use specific categories for expenses to identify spending patterns
- Set up all recurring transactions for better automation
- Export your data regularly as a backup

### Pro Tips
- The 50/30/20 rule is a great starting point for budgeting
- Track your net worth monthly (assets minus liabilities)
- Build an emergency fund of 3-6 months of expenses
- Automate your savings and investments when possible
- Review your financial goals and progress quarterly

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Workflow
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add comments for complex logic
- Write docstrings for functions and classes

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Design Inspiration**: Apple's Human Interface Guidelines
- **Charts**: Chart.js for beautiful data visualizations
- **Icons**: System emoji for universal compatibility
- **Color Palette**: iOS system colors for consistency

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Documentation](docs/)
2. Search [Issues](https://github.com/yourusername/moneywise/issues)
3. Create a new issue if needed

## 🗺️ Roadmap

### Version 1.1 (Coming Soon)
- [ ] Multiple account support
- [ ] Recurring transaction templates
- [ ] Advanced reporting features
- [ ] Mobile app (React Native)

### Version 1.2 (Future)
- [ ] Bank integration (Plaid API)
- [ ] Goal tracking and milestone alerts
- [ ] Advanced investment analytics
- [ ] Multi-user support

### Version 2.0 (Long-term)
- [ ] Machine learning spending insights
- [ ] Cryptocurrency portfolio tracking
- [ ] Tax preparation integration
- [ ] Financial advisor recommendations

---

**Built with ❤️ for better financial management**

*MoneyWise - Your path to financial wisdom* 