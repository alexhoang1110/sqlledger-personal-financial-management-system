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

DELIMITER ;