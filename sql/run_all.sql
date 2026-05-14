-- Create the main database for the personal finance system
CREATE DATABASE IF NOT EXISTS PersonalFinanceDB;
USE PersonalFinanceDB;

-- ===== 01_schema.sql =====
-- 1. Create Users table to store profile information
CREATE TABLE IF NOT EXISTS Users ( 
	UserID INT AUTO_INCREMENT PRIMARY KEY, 
    UserName VARCHAR(100) NOT NULL, 
    Email VARCHAR(100) UNIQUE NOT NULL, 
    PhoneNumber VARCHAR(15),
    CreatedAt   DATETIME DEFAULT CURRENT_TIMESTAMP,
    PasswordHash VARCHAR(255) NOT NULL DEFAULT ''
);

-- 2. Create BankAccounts table to track balance
CREATE TABLE IF NOT EXISTS BankAccounts (
	AccountID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT NOT NULL,
    BankName VARCHAR(100) NOT NULL,
    Balance DECIMAL(15, 2) DEFAULT 0.00,
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
);

-- 3. Create Income table for revenue tracking
CREATE TABLE IF NOT EXISTS Income (
	IncomeID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT NOT NULL,
    Amount DECIMAL(15, 2) NOT NULL CHECK (Amount > 0),
    IncomeDate DATE NOT NULL,
    Description VARCHAR(255),
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
);

-- 4. Create ExpenseCategories table for spending classification
CREATE TABLE IF NOT EXISTS ExpenseCategories (
	CategoryID INT AUTO_INCREMENT PRIMARY KEY,
    CategoryName VARCHAR(100) UNIQUE NOT NULL
);

-- 5. Create Expenses table for daily transaction records
CREATE TABLE IF NOT EXISTS Expenses (
	ExpenseID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT NOT NULL,
    CategoryID INT NOT NULL,
    Amount DECIMAL(15, 2) NOT NULL CHECK (Amount > 0),
    ExpenseDate DATE NOT NULL,
    Description VARCHAR(255),
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE,
    FOREIGN KEY (CategoryID) REFERENCES ExpenseCategories(CategoryID) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS BalanceAuditLog (
    LogID      INT AUTO_INCREMENT PRIMARY KEY,
    AccountID  INT NOT NULL,
    OldBalance DECIMAL(15,2),
    NewBalance DECIMAL(15,2),
    ChangeType VARCHAR(20),
    ChangedAt  DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (AccountID) REFERENCES BankAccounts(AccountID) ON DELETE CASCADE
);

-- ===== 02_indexes.sql =====
DROP PROCEDURE IF EXISTS drop_index_if_exists;

DELIMITER //
CREATE PROCEDURE drop_index_if_exists(
    IN p_table VARCHAR(100),
    IN p_index VARCHAR(100)
)
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.STATISTICS
        WHERE table_schema = DATABASE()
          AND table_name   = p_table
          AND index_name   = p_index
    ) THEN
        SET @sql = CONCAT('DROP INDEX ', p_index, ' ON ', p_table);
        PREPARE stmt FROM @sql;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;
    END IF;
END //
DELIMITER ;

CALL drop_index_if_exists('Expenses', 'idx_expense_date');
CALL drop_index_if_exists('Income',   'idx_income_date');

DROP PROCEDURE IF EXISTS drop_index_if_exists;
CREATE INDEX idx_expense_date ON Expenses(ExpenseDate);
CREATE INDEX idx_income_date  ON Income(IncomeDate);

-- ===== 03_views.sql =====
-- View 1: MonthlyFinancialSummary
CREATE OR REPLACE VIEW MonthlyFinancialSummary AS
SELECT
    u.UserID,
    u.UserName,
    combined.ReportYear,
    combined.ReportMonth,
    COALESCE(SUM(combined.TotalIncome), 0)  AS TotalIncome,
    COALESCE(SUM(combined.TotalExpense), 0) AS TotalExpense,
    COALESCE(SUM(combined.TotalIncome), 0) - COALESCE(SUM(combined.TotalExpense), 0) AS NetSavings
FROM Users u
JOIN (
    SELECT UserID, 
           YEAR(IncomeDate)  AS ReportYear, 
           MONTH(IncomeDate) AS ReportMonth,
           SUM(Amount)       AS TotalIncome, 
           0                 AS TotalExpense
    FROM Income 
    GROUP BY UserID, YEAR(IncomeDate), MONTH(IncomeDate)

    UNION ALL

    SELECT UserID, 
           YEAR(ExpenseDate)  AS ReportYear, 
           MONTH(ExpenseDate) AS ReportMonth,
           0                  AS TotalIncome,
           SUM(Amount)        AS TotalExpense
    FROM Expenses 
    GROUP BY UserID, YEAR(ExpenseDate), MONTH(ExpenseDate)
) combined ON u.UserID = combined.UserID
GROUP BY u.UserID, u.UserName, combined.ReportYear, combined.ReportMonth;

-- View 2: CategoryWiseSpending
CREATE OR REPLACE VIEW CategoryWiseSpending AS
SELECT 
    e.UserID,
    c.CategoryName,
    YEAR(e.ExpenseDate) AS SpendingYear,
    MONTH(e.ExpenseDate) AS SpendingMonth,
    SUM(e.Amount) AS TotalAmount
FROM Expenses e
JOIN ExpenseCategories c ON e.CategoryID = c.CategoryID
GROUP BY e.UserID, c.CategoryName, SpendingYear, SpendingMonth;

-- ===== 04_functions.sql =====
DROP FUNCTION IF EXISTS GetTotalExpenses;
DROP FUNCTION IF EXISTS GetTotalIncome;
DROP FUNCTION IF EXISTS GetBudgetStatus;

DELIMITER //

-- Function: GetTotalExpenses
CREATE FUNCTION GetTotalExpenses(TargetUserID INT, TargetMonth INT, TargetYear INT) 
RETURNS DECIMAL(15,2)
DETERMINISTIC
BEGIN
    DECLARE Total DECIMAL(15,2);
    SELECT COALESCE(SUM(Amount), 0) INTO Total
    FROM Expenses
    WHERE UserID = TargetUserID AND MONTH(ExpenseDate) = TargetMonth AND YEAR(ExpenseDate) = TargetYear;
    RETURN Total;
END //

CREATE FUNCTION GetTotalIncome(TargetUserID INT, TargetMonth INT, TargetYear INT) 
RETURNS DECIMAL(15,2) DETERMINISTIC
BEGIN
    DECLARE Total DECIMAL(15,2);
    SELECT COALESCE(SUM(Amount), 0) INTO Total
    FROM Income
    WHERE UserID = TargetUserID 
      AND MONTH(IncomeDate) = TargetMonth 
      AND YEAR(IncomeDate) = TargetYear;
    RETURN Total;
END //

CREATE FUNCTION GetBudgetStatus(TargetUserID INT, TargetMonth INT, TargetYear INT)
RETURNS VARCHAR(20) DETERMINISTIC
BEGIN
    DECLARE net DECIMAL(15,2);
    SET net = GetTotalIncome(TargetUserID, TargetMonth, TargetYear)
            - GetTotalExpenses(TargetUserID, TargetMonth, TargetYear);
    IF    net > 0  THEN RETURN 'SURPLUS';
    ELSEIF net = 0 THEN RETURN 'BALANCED';
    ELSE               RETURN 'DEFICIT';
    END IF;
END //

DELIMITER ;

-- ===== 05_triggers.sql =====
DROP TRIGGER IF EXISTS AfterExpenseInsert;
DROP TRIGGER IF EXISTS AfterIncomeInsert;
DROP TRIGGER IF EXISTS AfterBalanceUpdate;

DELIMITER //

-- Trigger: AfterExpenseInsert
CREATE TRIGGER AfterExpenseInsert
AFTER INSERT ON Expenses
FOR EACH ROW
BEGIN
    -- Lấy AccountID đầu tiên của user để trừ tiền (có thể tùy chỉnh lại logic này)
    DECLARE TargetAccount INT;
    SELECT AccountID INTO TargetAccount FROM BankAccounts WHERE UserID = NEW.UserID LIMIT 1;
    
    UPDATE BankAccounts 
    SET Balance = Balance - NEW.Amount 
    WHERE AccountID = TargetAccount;
END //

-- Trigger: AfterIncomeInsert
CREATE TRIGGER AfterIncomeInsert
AFTER INSERT ON Income
FOR EACH ROW
BEGIN
    DECLARE TargetAccount INT;
    SELECT AccountID INTO TargetAccount FROM BankAccounts WHERE UserID = NEW.UserID LIMIT 1;
    
    UPDATE BankAccounts 
    SET Balance = Balance + NEW.Amount 
    WHERE AccountID = TargetAccount;
END //

CREATE TRIGGER AfterBalanceUpdate
AFTER UPDATE ON BankAccounts
FOR EACH ROW
BEGIN
    IF OLD.Balance <> NEW.Balance THEN
        INSERT INTO BalanceAuditLog(AccountID, OldBalance, NewBalance, ChangeType)
        VALUES (
            NEW.AccountID,
            OLD.Balance,
            NEW.Balance,
            IF(NEW.Balance > OLD.Balance, 'INCOME', 'EXPENSE')
        );
    END IF;
END //

DELIMITER ;

-- ===== 06_procedures.sql =====
DROP PROCEDURE IF EXISTS MonthlyClosure;
DROP PROCEDURE IF EXISTS AddIncome;
DROP PROCEDURE IF EXISTS AddExpense;

DELIMITER //

-- Procedure: MonthlyClosure
CREATE PROCEDURE MonthlyClosure(IN TargetUserID INT)
BEGIN
    SELECT 
        BankName, 
        Balance AS ClosingBalance, 
        CURRENT_DATE() AS ClosureDate
    FROM BankAccounts
    WHERE UserID = TargetUserID;
END //

CREATE PROCEDURE AddIncome(
    IN p_UserID      INT,
    IN p_Amount      DECIMAL(15,2),
    IN p_Date        DATE,
    IN p_Description VARCHAR(255)
)
BEGIN
    IF p_Amount <= 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Amount must be positive';
    END IF;

    INSERT INTO Income(UserID, Amount, IncomeDate, Description)
    VALUES (p_UserID, p_Amount, p_Date, p_Description);

    SELECT 'Income added successfully' AS Message, LAST_INSERT_ID() AS NewIncomeID;
END //

CREATE PROCEDURE AddExpense(
    IN p_UserID      INT,
    IN p_CategoryID  INT,
    IN p_Amount      DECIMAL(15,2),
    IN p_Date        DATE,
    IN p_Description VARCHAR(255)
)
BEGIN
    DECLARE v_Balance DECIMAL(15,2);

    SELECT Balance INTO v_Balance
    FROM BankAccounts WHERE UserID = p_UserID
    ORDER BY AccountID LIMIT 1;

    IF v_Balance < p_Amount THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Insufficient account balance';
    END IF;

    INSERT INTO Expenses(UserID, CategoryID, Amount, ExpenseDate, Description)
    VALUES (p_UserID, p_CategoryID, p_Amount, p_Date, p_Description);

    SELECT 'Expense recorded' AS Message,
           v_Balance - p_Amount AS RemainingBalance;
END //

DELIMITER ;

-- ===== 07_security.sql =====
-- User
CREATE USER IF NOT EXISTS 'finance_app_user'@'%' IDENTIFIED BY 'AVNS_6gOttD29pc4MSbLfUro';
GRANT SELECT, INSERT, UPDATE ON PersonalFinanceDB.* TO 'finance_app_user'@'%';

-- Viewer User
CREATE USER IF NOT EXISTS 'finance_viewer'@'%' IDENTIFIED BY 'AVNS_EJ7Ou954b5hrphQdnIG';
GRANT SELECT ON PersonalFinanceDB.* TO 'finance_viewer'@'%';

FLUSH PRIVILEGES;