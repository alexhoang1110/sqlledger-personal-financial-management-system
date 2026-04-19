USE personalfinancedb;

-- Insert sample records into Users table
INSERT INTO Users (UserName, Email, PhoneNumber) VALUES
('Alex Hoang', 'alex.hoang@email.com', '0912345678'),
('John Doe', 'john.doe@email.com', '0987654321');

-- Insert sample categories into ExpenseCategories
INSERT INTO ExpenseCategories (CategoryName) VALUES
('Food & Dining'),
('Transportation'),
('Utilities'),
('Entertainment'),
('Healthcare');

-- Insert sample accounts into BankAccounts
INSERT INTO BankAccounts (UserID, BankName, Balance) VALUES
(1, 'Vietcombank', 15000000.00),
(1, 'Techcombank', 5000000.00),
(2, 'MB Bank', 20000000.00);

-- Insert sample revenue into Income table
INSERT INTO Income (UserID, Amount, IncomeDate, Description) VALUES
(1, 10000000.00, '2026-04-01', 'Freelance Project Settlement'),
(1, 5000000.00, '2026-04-10', 'Content Developer Salary'),
(2, 20000000.00, '2026-04-05', 'Monthly Fixed Salary');

-- Insert sample transactions into Expenses table
INSERT INTO Expenses (UserID, CategoryID, Amount, ExpenseDate, Description) VALUES
(1, 1, 150000.00, '2026-04-12', 'Dinner with friends'),
(1, 2, 50000.00, '2026-04-13', 'Ride-hailing service'),
(1, 4, 300000.00, '2026-04-15', 'Weekend movie tickets'),
(2, 3, 1000000.00, '2026-04-10', 'Monthly electricity bill'),
(2, 1, 200000.00, '2026-04-14', 'Supermarket groceries');