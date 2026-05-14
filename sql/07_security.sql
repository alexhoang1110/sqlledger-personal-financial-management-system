-- User
CREATE USER IF NOT EXISTS 'finance_app_user'@'%' IDENTIFIED BY 'AVNS_6gOttD29pc4MSbLfUro';
GRANT SELECT, INSERT, UPDATE ON PersonalFinanceDB.* TO 'finance_app_user'@'%';

-- Viewer User
CREATE USER IF NOT EXISTS 'finance_viewer'@'%' IDENTIFIED BY 'AVNS_EJ7Ou954b5hrphQdnIG';
GRANT SELECT ON PersonalFinanceDB.* TO 'finance_viewer'@'%';

FLUSH PRIVILEGES;