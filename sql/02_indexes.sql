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