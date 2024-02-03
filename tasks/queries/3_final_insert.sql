-- Transactions for rollback
BEGIN TRANSACTION;

-- DeDupe Posts (Keep Latest)
DELETE FROM
    Post USING Post_temp
WHERE
    Post.Self_Url = Post_temp.Self_Url;

-- Final Insertion
INSERT INTO
    Post
SELECT
    *
FROM
    Post_temp;

END TRANSACTION;

-- Cleanup
DROP TABLE Post_temp;
