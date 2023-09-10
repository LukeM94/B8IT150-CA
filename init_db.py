#Importing the required libraries
import sqlite3
from flask_bcrypt import Bcrypt 

#Creating the Bcrypt object for password hashing
bcrypt = Bcrypt()

#Creating the database connection to freelanceflow.db
connection = sqlite3.connect('freelanceflow.db')

#Creating the database schema
with open('schema.sql') as f:
    connection.executescript(f.read())

#Seeding the database with some data for testing
cur = connection.cursor()

cur.execute('INSERT INTO Jobs (title, description, datecreated, deadline, status, quotation, createdby) VALUES (?, ?, ?, ?, ?, ?, ?)',
            ('Create API for XYZ Company', 'XYZ have requested a Python API for their Video CMS', '2023-08-30', '2023-09-22', 'Backlog', 1050.99, 1)
            )

cur.execute('INSERT INTO Jobs (title, description, datecreated, deadline, status, quotation, createdby) VALUES (?, ?, ?, ?, ?, ?, ?)',
            ('Create UI for ABC Company', 'ABC have requested a some UI mockups for their new iOS app', '2023-08-30', '2023-09-22', 'Backlog', 500.99, 2)
            )

cur.execute('INSERT INTO Jobs (title, description, datecreated, deadline, status, quotation, createdby) VALUES (?, ?, ?, ?, ?, ?, ?)',
            ('Create QA Plan for QWERTY Company', 'QWERTY have requested a QA plan for their new release', '2023-08-30', '2023-09-22', 'Backlog', 700.99, 3)
            )

password = 'password'
pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')

cur.execute('INSERT INTO Users (username, password, emailaddress, firstname, lastname, accounttype) VALUES (?, ?, ?, ?, ?, ?)',
            ('qa', pw_hash, 'qa@freelanceflow.local', 'Luke', 'Morton', 'admin')
            )

cur.execute('INSERT INTO Users (username, password, emailaddress, firstname, lastname) VALUES (?, ?, ?, ?, ?)',
            ('tester', pw_hash, 'qa@test.local', 'Morton', 'Luke')
            )

cur.execute('INSERT INTO Users (username, password, emailaddress, firstname, lastname) VALUES (?, ?, ?, ?, ?)',
            ('quality', pw_hash, 'qa@luke.local', 'L', 'M')
            )

#Committing the changes and closing the connection
connection.commit()
connection.close()