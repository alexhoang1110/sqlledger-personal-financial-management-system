-- User
CREATE USER IF NOT EXISTS 'finance_app_user'@'localhost' IDENTIFIED BY 'User1234';
GRANT SELECT, INSERT, UPDATE ON PersonalFinanceDB.* TO 'finance_app_user'@'localhost';

-- Viewer User
CREATE USER IF NOT EXISTS 'finance_viewer'@'localhost' IDENTIFIED BY 'View1234';
GRANT SELECT ON PersonalFinanceDB.* TO 'finance_viewer'@'localhost';

FLUSH PRIVILEGES;