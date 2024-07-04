DELIMITER //

DROP PROCEDURE IF EXISTS ReturnBook;

CREATE PROCEDURE ReturnBook(
    IN book_id INT,
    IN student_id INT,
    OUT error_code INT

)
BEGIN
    DECLARE book_exists INT;
    DECLARE rows_deleted INT;

    -- Initialize the error_code to 0 (no error)
    SET error_code = 0;


    -- Delete the record from Book_Issue table
    DELETE FROM book_issue
    WHERE S_ID = student_id AND B_ID = book_id;

    -- Get the number of deleted rows
    SET rows_deleted = ROW_COUNT();

    -- Check if any rows were deleted
    IF rows_deleted > 0 THEN
      -- Increment the stock quantity of the book
        UPDATE book
        SET Qte = Qte + 1
        WHERE ID = book_id;
    ELSE
        -- Initialize the error_code to 0 (no error)
        SET error_code = 45004;
        -- SET MESSAGE_TEXT = "Student has not issued this book.";
        ROLLBACK;
    END IF;   

END //

DELIMITER ;