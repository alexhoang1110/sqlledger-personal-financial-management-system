-- Create the main database for the personal finance system
CREATE DATABASE IF NOT EXISTS PersonalFinanceDB;
USE PersonalFinanceDB;

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
    ChangeType VARCHAR(20),   -- 'INCOME' hoặc 'EXPENSE'
    ChangedAt  DATETIME DEFAULT CURRENT_TIMESTAMP
);