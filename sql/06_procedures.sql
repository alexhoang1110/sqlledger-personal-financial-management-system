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