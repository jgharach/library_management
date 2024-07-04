DELIMITER //
DROP PROCEDURE IF EXISTS IssueBook;

CREATE PROCEDURE IssueBook(
    IN book_id INT,
    IN student_id INT,
    OUT error_code INT
)
BEGIN
    DECLARE book_quantity INT;
    DECLARE student_exists INT;

    -- Initialize the error_code to 0 (no error)
    SET error_code = 0;

    -- Check if the student exists
    SELECT COUNT(*) INTO student_exists
    FROM student
    WHERE ID = student_id;

    IF student_exists = 0 THEN
        SET error_code = 45000;
        ROLLBACK;
    ELSE
        -- Check if the book is available
        SELECT Qte INTO book_quantity
        FROM book
        WHERE ID = book_id;

        IF book_quantity IS NULL OR book_quantity <= 0 THEN
            SET error_code = 45001;
            ROLLBACK;
        ELSE
            -- Insert into Book_Issue
            INSERT INTO Book_Issue (B_ID, S_ID) VALUES (book_id, student_id);

            -- Update the book quantity
            UPDATE book
            SET Qte = Qte - 1
            WHERE ID = book_id;
        END IF;
    END IF;
END;

DELIMITER ;
