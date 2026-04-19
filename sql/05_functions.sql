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

DELIMITER ;