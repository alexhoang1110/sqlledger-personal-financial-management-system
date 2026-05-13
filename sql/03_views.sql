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