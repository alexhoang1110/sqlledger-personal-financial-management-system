<div align="center">

<img src="https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/MySQL-8.4-4479A1?style=for-the-badge&logo=mysql&logoColor=white"/>
<img src="https://img.shields.io/badge/Tkinter-GUI-FF6B35?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Aiven-Cloud_DB-FF0000?style=for-the-badge"/>

# SQLLedger
### Personal Finance Management System

> A comprehensive desktop application for tracking income, expenses, and financial health - powered by MySQL and Python.

**National Economics University - Database Management System Project**  
Student: Hoang Linh Phuong (11245925) | Instructor: Dr. Tran Hung

[Representing Video](https://youtu.be/HO4tPitm03I) · [Report](docs/11245925 - HoangLinhPhuong - FinalReport.pdf) · [Issues](https://github.com/alexhoang1110/sqlledger-personal-financial-management-system/issues)

</div>

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Database Architecture](#database-architecture)
- [Screenshots](#screenshots)

---

## Overview

SQLLedger is a two-tier desktop application that helps individuals automate the tracking of their income, expenses, and overall financial health. The system uses a cloud-hosted MySQL database (Aiven) for data integrity and a Python/Tkinter GUI for a dark-mode desktop interface.

Key highlights:
- **Automated balance updates** via database triggers - no manual sync needed
- **Role-based access control** with `finance_app_user` and `finance_viewer` MySQL users
- **Secure authentication** using bcrypt password hashing
- **Real-time budget alerts** (SURPLUS / BALANCED / DEFICIT) via User-Defined Functions
- **Visual analytics** with embedded Matplotlib charts

---

## Features

| Feature | Description |
|---|---|
| User Authentication | Secure login and registration with bcrypt-hashed passwords |
| Income Management | Add, view, and delete income records with automatic balance update |
| Expense Management | Categorized expense tracking with overdraft protection |
| Bank Account Tracking | Real-time balance cards and full audit log history |
| Financial Reports | Monthly income vs expense bar chart and category pie chart |
| Budget Status | Live SURPLUS / BALANCED / DEFICIT badge on dashboard |
| CSV Import | Seed the database from CSV files for quick setup |
| Audit Trail | Every balance change is automatically logged to `BalanceAuditLog` |

---

## Project Structure

```
sqlledger-personal-financial-management-system/
├── docs/                       # Documentation and diagrams
│   ├── ER_Diagram.png          # Entity-Relationship diagram
│   └── 11245925 - HoangLinhPh
│       uong - FinalReport.pdf  # Final project report
├── sql/                        # All database scripts
│   ├── 01_schema.sql           # Tables, PKs, FKs, constraints
│   ├── 02_indexes.sql          # Performance indexes
│   ├── 03_views.sql            # MonthlyFinancialSummary, CategoryWiseSpending
│   ├── 04_functions.sql        # GetTotalIncome, GetTotalExpenses, GetBudgetStatus
│   ├── 05_triggers.sql         # AfterIncomeInsert, AfterExpenseInsert, AfterBalanceUpdate
│   ├── 06_procedures.sql       # AddIncome, AddExpense, MonthlyClosure
│   ├── 07_security.sql         # Role-based user access control
│   └── run_all.sql             # Consolidated script to run all SQL files
│
├── python/                     # Python application
│   ├── main.py                 # Application entry point
│   ├── config.py               # Database connection configuration
│   ├── database.py             # Core DB access functions
│   ├── ca.pem                  # SSL certificate for Aiven cloud DB
│   ├── requirements.txt        # Python dependencies
│   ├── SQLLedger.spec          # PyInstaller build configuration
│   │
│   ├── models/                 # Data access layer (MVC - Model)
│   │   ├── user.py             # Users table operations
│   │   ├── income.py           # Income table operations
│   │   ├── expense.py          # Expenses table operations
│   │   └── account.py          # BankAccounts table operations
│   │
│   ├── gui/                    # GUI components (MVC - View + Controller)
│   │   ├── app.py              # Controller: session management & navigation
│   │   ├── theme.py            # Color palette and reusable widgets
│   │   ├── login_window.py     # Login and registration window
│   │   ├── base_page.py        # Base class for all pages
│   │   └── pages/
│   │       ├── dashboard.py    # Dashboard: stat cards, budget status, charts
│   │       ├── incomes.py      # Income entry form and history table
│   │       ├── expenses.py     # Expense entry form with category dropdown
│   │       ├── report.py       # Reports: bar chart and pie chart
│   │       ├── account.py      # Bank account cards and audit log
│   │       └── users.py        # User profile management
│   │
│   ├── reports/                # Standalone chart generation (MVC - View)
│   │   └── charts.py           # Bar chart and pie chart export functions
│   │
│   ├── utils/
│   │   └── csv_handler.py      # CSV import and export utilities
│   │
│   └── data/                   # Sample CSV data for initial seeding
│       ├── users.csv
│       ├── bank_accounts.csv
│       ├── income.csv
│       └── expenses.csv
│
└── docs/                       # Documentation and diagrams
    └── ER_Diagram.png          # Entity-Relationship diagram
```

---

## Tech Stack

| Component | Technology | Version |
|---|---|---|
| Database | MySQL (Aiven Cloud) | 8.4 |
| Programming Language | Python | 3.12 |
| DB Connector | mysql-connector-python | 9.3.0 |
| GUI Framework | Tkinter | Built-in |
| Data Visualization | Matplotlib | 3.10.8 |
| Password Security | bcrypt | 4.2.1 |
| Packaging | PyInstaller | 6.20.0 |

---

## Getting Started

### Option A - Download the App (Recommended for Users)

1. Go to the [**Releases**](https://github.com/alexhoang1110/sqlledger-personal-financial-management-system/releases) tab
2. Download `SQLLedger.exe`
3. Run the file - no Python or database setup required

> The app connects to a pre-configured cloud database (Aiven). Internet connection required.

---

### Option B - Run from Source (For Developers)

#### Prerequisites

- Python 3.12+
- Access to a MySQL 8.4 instance (local or cloud)

#### 1. Clone the repository

```bash
git clone https://github.com/alexhoang1110/sqlledger-personal-financial-management-system.git
cd sqlledger-personal-financial-management-system
```

#### 2. Install dependencies

```bash
cd python
pip install -r requirements.txt
```

#### 3. Set up the database

Run all SQL scripts in order against your MySQL instance:

```bash
mysql -u root -p < sql/run_all.sql
```

Or run individually:

```bash
mysql -u root -p < sql/01_schema.sql
mysql -u root -p < sql/02_indexes.sql
mysql -u root -p < sql/03_views.sql
mysql -u root -p < sql/04_functions.sql
mysql -u root -p < sql/05_triggers.sql
mysql -u root -p < sql/06_procedures.sql
mysql -u root -p < sql/07_security.sql
```

#### 4. Configure the database connection

Edit `python/config.py` with your database credentials:

```python
DB_CONFIG = {
    "host":     "your-host",
    "port":     3306,
    "user":     "finance_app_user",
    "password": "your-password",
    "database": "PersonalFinanceDB",
    "ssl_ca":   "ca.pem"       # Remove this line if not using SSL
}
```

#### 5. (Optional) Seed sample data

```bash
python python/utils/csv_handler.py
```

#### 6. Test the connection

```bash
python python/test_db.py
```

#### 7. Run the application

```bash
python python/main.py
```

---

### Option C - Build the `.exe` yourself

```bash
cd python
pyinstaller SQLLedger.spec
```

The compiled executable will be output to `python/dist/`.

---

## Database Architecture

### Tables

| Table | Description |
|---|---|
| `Users` | User profiles with bcrypt-hashed passwords |
| `BankAccounts` | Bank accounts with auto-updated balances |
| `Income` | Income transaction records |
| `ExpenseCategories` | Predefined spending categories |
| `Expenses` | Expense records linked to categories |
| `BalanceAuditLog` | Automatic audit trail of every balance change |

### Advanced Database Objects

| Object | Name | Purpose |
|---|---|---|
| Index | `idx_expense_date`, `idx_income_date` | Fast date-range queries for reports |
| View | `MonthlyFinancialSummary` | Monthly income, expense, net savings per user |
| View | `CategoryWiseSpending` | Spending breakdown by category per user/month |
| Function | `GetTotalIncome(UserID, Month, Year)` | Sum of income for a given month |
| Function | `GetTotalExpenses(UserID, Month, Year)` | Sum of expenses for a given month |
| Function | `GetBudgetStatus(UserID, Month, Year)` | Returns SURPLUS / BALANCED / DEFICIT |
| Trigger | `AfterIncomeInsert` | Auto-increments bank balance on income insert |
| Trigger | `AfterExpenseInsert` | Auto-decrements bank balance on expense insert |
| Trigger | `AfterBalanceUpdate` | Writes to `BalanceAuditLog` on every balance change |
| Procedure | `AddIncome` | Validates and inserts an income record |
| Procedure | `AddExpense` | Validates balance, rejects overdrafts, inserts expense |
| Procedure | `MonthlyClosure` | Generates end-of-month closing balance report |

### Database Security

Two dedicated MySQL users are used following the **principle of least privilege**:

| User | Permissions | Purpose |
|---|---|---|
| `finance_app_user` | SELECT, INSERT, UPDATE | Used by the application at runtime |
| `finance_viewer` | SELECT only | Read-only reporting access |

The `root` account is never referenced in any application file.

---

## References

- [MySQL 8.4 Reference Manual](https://dev.mysql.com/doc/refman/8.4/en/)
- [MySQL Connector/Python Developer Guide](https://dev.mysql.com/doc/connector-python/en/)
- [Python tkinter Documentation](https://docs.python.org/3/library/tkinter.html)
- [Matplotlib Documentation](https://matplotlib.org/stable/)
- [bcrypt on PyPI](https://pypi.org/project/bcrypt/)
- [Aiven for MySQL Documentation](https://aiven.io/docs/products/mysql)
