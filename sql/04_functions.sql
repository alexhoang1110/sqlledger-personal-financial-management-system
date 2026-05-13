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