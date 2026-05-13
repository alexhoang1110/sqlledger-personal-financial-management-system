from database import fetch_all, execute, call_procedure

def add_expense(user_id, category_id, amount, date, description):
    """
    Add spending - call Stored Procedure AddExpense
    Procedure will check the balance before allowing the addition.
    """
    return call_procedure("AddExpense", [user_id, category_id, amount, date, description])

def get_expenses_by_user(user_id):
    """Retrieve spending history along with category names."""
    return fetch_all(
        """SELECT e.ExpenseID, ec.CategoryName, e.Amount, e.ExpenseDate, e.Description
            FROM Expenses e
            JOIN ExpenseCategories ec ON e.CategoryID = ec.CategoryID
            WHERE e.UserID = %s
            ORDER BY e.ExpenseDate DESC""",
        (user_id,)
    )

def get_categories():
    """Get a list of all spending categories."""
    return fetch_all("SELECT * FROM ExpenseCategories")

def get_monthly_expense(user_id, month, year):
    """Total spending in month X of year Y."""
    result = fetch_all(
        "SELECT GetTotalExpenses(%s, %s, %s) AS Total",
        (user_id, month, year)
    )
    return result[0] ["Total"] if result else 0

def get_budget_status(user_id, month, year):
    """Check budget status: SURPLUS / DEFICIT / BALANCED."""
    result = fetch_all(
        "SELECT GetBudgetStatus(%s, %s, %s) AS Status",
        (user_id, month, year)
    )
    return result[0]["Status"] if result else "UNKNOWN"

def delete_expense(expense_id):
    """Delete an expense entry by its ID."""
    return execute("DELETE FROM Expenses WHERE ExpenseID = %s", (expense_id,))