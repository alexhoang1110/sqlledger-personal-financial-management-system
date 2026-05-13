from database import fetch_all, fetch_one

def get_accounts_by_user(user_id):
    """Get a list of the user's bank accounts."""
    return fetch_all(
        "SELECT * FROM BankAccounts WHERE UserID = %s",
        (user_id,)
    )

def get_total_balance(user_id):
    """Total balance of all user accounts."""
    result = fetch_one(
        "SELECT COALESCE(SUM(Balance), 0) AS TotalBalance FROM BankAccounts WHERE UserID = %s",
        (user_id,)
    )
    return result["TotalBalance"] if result else 0

def get_monthly_summary(user_id):
    """Get a summary of monthly income and expenses from View."""
    return fetch_all(
        "SELECT * FROM MonthlyFinancialSummary WHERE UserID = %s ORDER BY ReportYear, ReportMonth",
        (user_id,)
    )

def get_category_spending(user_id):
    """Get spending by category from View."""
    return fetch_all(
        "SELECT * FROM CategoryWiseSpending WHERE UserID = %s ORDER BY TotalAmount DESC",
        (user_id,)
    )