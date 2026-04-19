CREATE USER 'finance_app_user'@'localhost' IDENTIFIED BY 'SecureAppPassword123!';
GRANT SELECT, INSERT, UPDATE ON PersonalFinanceDB.* TO 'finance_app_user'@'localhost';
FLUSH PRIVILEGES;