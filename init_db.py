import sqlite3

connection = sqlite3.connect('freelanceflow.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO Jobs (title, description, datecreated, deadline, status, quotation) VALUES (?, ?, ?, ?, ?, ?)",
            ('Create API for XYZ Company', 'XYZ have requested a Python API for their Video CMS', '2023‐08‐20', '2023‐09‐20', 'Backlog', 1050.99)
            )

cur.execute("INSERT INTO Jobs (title, description, datecreated, deadline, status, quotation) VALUES (?, ?, ?, ?, ?, ?)",
            ('Create UI for ABC Company', 'ABC have requested a some UI mockups for their new iOS app', '2023‐08‐20', '2023‐09‐20', 'Backlog', 500.99)
            )

cur.execute("INSERT INTO Jobs (title, description, datecreated, deadline, status, quotation) VALUES (?, ?, ?, ?, ?, ?)",
            ('Create QA Plan for QWERTY Company', 'QWERTY have requested a QA plan for their new release', '2023‐08‐20', '2023‐09‐20', 'Backlog', 700.99)
            )

connection.commit()
connection.close()