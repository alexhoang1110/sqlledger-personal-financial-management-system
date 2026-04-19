-- View 1: MonthlyFinancialSummary
CREATE VIEW MonthlyFinancialSummary AS
SELECT 
    u.UserID,
    u.UserName,
    YEAR(COALESCE(e.ExpenseDate, i.IncomeDate)) AS ReportYear,
    MONTH(COALESCE(e.ExpenseDate, i.IncomeDate)) AS ReportMonth,
    SUM(DISTINCT i.Amount) AS TotalIncome,
    SUM(DISTINCT e.Amount) AS TotalExpense
FROM Users u
LEFT JOIN Income i ON u.UserID = i.UserID 
LEFT JOIN Expenses e ON u.UserID = e.UserID
GROUP BY u.UserID, u.UserName, ReportYear, ReportMonth;

-- View 2: CategoryWiseSpending
CREATE VIEW CategoryWiseSpending AS
SELECT 
    e.UserID,
    c.CategoryName,
    YEAR(e.ExpenseDate) AS SpendingYear,
    MONTH(e.ExpenseDate) AS SpendingMonth,
    SUM(e.Amount) AS TotalAmount
FROM Expenses e
JOIN ExpenseCategories c ON e.CategoryID = c.CategoryID
GROUP BY e.UserID, c.CategoryName, SpendingYear, SpendingMonth;