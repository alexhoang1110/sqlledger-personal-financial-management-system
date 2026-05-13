from database import fetch_all, call_procedure, execute

def add_income(user_id, amount, date, description):
    """
    Add more income - call Stored Procedure AddIncome.
    Trigger AfterIncomeInsert will automatically add it to BankAccount.
    """
    return call_procedure("AddIncome", [user_id, amount, date, description])

def get_income_by_user(user_id):
    """Retrieve a user's income history."""
    return fetch_all(
        """SELECT IncomeID, Amount, IncomeDate, Description 
            FROM Income 
            WHERE UserID = %s 
            ORDER BY IncomeDate DESC""",
        (user_id,)
    )

def get_monthly_income(user_id, month, year):
    """Total monthly income of a user in month X of year Y."""
    result = fetch_all(
        "SELECT GetTotalIncome(%s, %s, %s) AS Total",
        (user_id, month, year)
    )
    return result[0]["Total"] if result else 0

def delete_income(income_id):
    """Delete an income entry by its ID."""
    return execute("DELETE FROM Income WHERE IncomeID = %s", (income_id,))