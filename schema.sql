DROP TABLE IF EXISTS Jobs;
DROP TABLE IF EXISTS Users;

CREATE TABLE Jobs (
    jobid INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    datecreated TEXT NOT NULL,
    deadline TEXT NOT NULL,
    status TEXT NOT NULL,
    quotation REAL NOT NULL
    createdby INTEGER,
    FOREIGN KEY (createdby) REFERENCES Users(userid)
);

CREATE TABLE Users (
    userid INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    emailaddress TEXT NOT NULL,
    firstname TEXT NOT NULL,
    lastname TEXT NOT NULL
);