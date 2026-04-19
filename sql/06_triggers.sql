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

DELIMITER ;