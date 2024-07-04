-- Active: 1692532684514@@127.0.0.1@3306@library
DELIMITER //

DROP PROCEDURE IF EXISTS DeleteBook;

CREATE PROCEDURE DeleteBook(
    IN book_id INT,
    OUT error_code INT
)
BEGIN
    DECLARE book_exist INT;
    DECLARE book_borrowed INT;

    -- Initialize the error_code to 0 (no error)
    SET error_code = 0;

    -- Vérifier si le livre existe
    SELECT ID INTO book_exist
    FROM book
    WHERE ID = book_id;

    IF book_exist IS NULL THEN
        SET error_code = 45003; -- No book with the given ID
        ROLLBACK;
    ELSE
        -- Vérifier si le livre est déjà emprunté
        SELECT COUNT(*) INTO book_borrowed
        FROM book_issue
        WHERE B_ID = book_id;

        -- Vérifier si le livre n'est pas emprunté
        IF book_borrowed = 0 THEN
            -- Supprimer le livre définitivement
            DELETE FROM book
            WHERE ID = book_id;
        ELSE
            SET error_code = 45002; -- Book is issued
            ROLLBACK;
        END IF;
    END IF;

END;

DELIMITER ;

