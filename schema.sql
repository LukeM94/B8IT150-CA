DROP TABLE IF EXISTS Jobs;

CREATE TABLE Jobs (
    jobid INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    datecreated TEXT NOT NULL,
    deadline TEXT NOT NULL,
    status TEXT NOT NULL,
    quotation REAL NOT NULL
);