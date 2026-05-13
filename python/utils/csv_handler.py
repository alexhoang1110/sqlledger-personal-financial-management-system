import csv
import os
from models.user import create_user, get_user_by_email
from database import execute

DATA_DIR = os.path.join(os.path.dirname(__file__), "../data")

def import_all_csv():
    """Import all CSV files into the database."""
    print("Importing CSV data...")
    _import_users()
    _import_bank_accounts()
    _import_income()
    _import_expense_categories() 
    _import_expenses()
    print("CSV import completed.")

def _import_users():
    path = os.path.join(DATA_DIR, "users.csv")
    with open(path, newline = "", encoding = "utf-8-sig") as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            # Skip if user with same email already exists
            if get_user_by_email(row["Email"]):
                continue
            create_user(
                row["UserName"],
                row["Email"],
                row.get("PhoneNumber", ""),
                row["Password"]
            )
            count += 1
    print(f"Users: {count} imported")

def _import_bank_accounts():
    path = os.path.join(DATA_DIR, "bank_accounts.csv")
    with open(path, newline = "", encoding = "utf-8-sig") as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            execute(
                """INSERT IGNORE INTO BankAccounts (UserID, BankName, Balance)
                   VALUES (%s, %s, %s)""",
                (row["UserID"], row["BankName"], row["Balance"])
            )
            count += 1
    print(f"BankAccounts: {count} imported")

def _import_income():
    path = os.path.join(DATA_DIR, "income.csv")
    with open(path, newline = "", encoding = "utf-8-sig") as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            execute(
                """INSERT IGNORE INTO Income (UserID, Amount, IncomeDate, Description)
                   VALUES (%s, %s, %s, %s)""",
                (row["UserID"], row["Amount"], row["IncomeDate"], row["Description"])
            )
            count += 1
    print(f"Income: {count} imported")

def _import_expense_categories():
    path = os.path.join(DATA_DIR, "expense_categories.csv")
    with open(path, newline = "", encoding = "utf-8-sig") as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            execute(
                """INSERT IGNORE INTO ExpenseCategories (CategoryID, CategoryName)
                   VALUES (%s, %s)""",
                (row["CategoryID"], row["CategoryName"])
            )
            count += 1

def _import_expenses():
    path = os.path.join(DATA_DIR, "expenses.csv")
    with open(path, newline = "", encoding = "utf-8-sig") as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            execute(
                """INSERT IGNORE INTO Expenses 
                   (UserID, CategoryID, Amount, ExpenseDate, Description)
                   VALUES (%s, %s, %s, %s, %s)""",
                (row["UserID"], row["CategoryID"], row["Amount"],
                 row["ExpenseDate"], row["Description"])
            )
            count += 1
    print(f"Expenses: {count} imported")

if __name__ == "__main__":
    import_all_csv()