CREATE TABLE IF NOT EXISTS Post (
    Title varchar(500) NOT NULL,
    Url varchar(500) NOT NULL,
    Self_Url varchar(500) NOT NULL PRIMARY KEY,
    Domain varchar(50) NOT NULL,
    Flair varchar(20) NOT NULL,
    Create_Date varchar(20) NOT NULL,
    Username varchar(20) NOT NULL,
    User_Link varchar(200) NOT NULL,
    Comments int NOT NULL,
    Upvotes int NOT NULL,
    Post_Type varchar(20) NOT NULL,
    Create_Only_Date varchar(20) NOT NULL,
    Create_Time varchar(20) NOT NULL,
    Created_At varchar(20) NOT NULL,
    Upvote_Range varchar(20) NOT NULL
);
