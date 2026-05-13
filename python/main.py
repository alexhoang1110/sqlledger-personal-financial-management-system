from gui.app import FinanceApp
from utils.csv_handler import import_all_csv
import os

if __name__ == "__main__":
    from database import fetch_all
    users = fetch_all("SELECT COUNT(*) AS cnt FROM Users")
    if users[0]["cnt"] == 0:
        import_all_csv()

    app = FinanceApp()
    app.start()