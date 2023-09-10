#Importing the required libraries
import unittest
import sqlite3
from flask_bcrypt import Bcrypt

#Creating the Bcrypt object for password hashing
bcrypt = Bcrypt()

#Creating the database connection to freelanceflow.db
def database_connection():
    conn = sqlite3.connect('freelanceflow.db')
    conn.row_factory = sqlite3.Row
    return conn

#Creating the unit tests
def tests():unittest.main(argv=['ignored'],exit=False)

class TestFreelanceFlow(unittest.TestCase):
    def test_user_registration(self):
        username = 'testuser'
        password = 'password'
        emailaddress = 'testuser@freelanceflow.com'
        firstname = 'Test'
        lastname = 'User'
        pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        conn = database_connection()
        conn.execute('INSERT INTO Users (username, password, emailaddress, firstname, lastname) VALUES (?, ?, ?, ?, ?)',
                        (username, pw_hash, emailaddress, firstname, lastname))
        conn.commit()
        conn.close()
        conn = database_connection()
        user_data = conn.execute('SELECT * FROM Users WHERE emailaddress = ?', (emailaddress,)).fetchone()
        conn.close()
        self.assertEqual(user_data['username'], username)
        self.assertEqual(user_data['emailaddress'], emailaddress)
        self.assertEqual(user_data['firstname'], firstname)
        self.assertEqual(user_data['lastname'], lastname)
    
    def test_job_creation(self):
        title = 'Test Job UnitTest'
        description = 'Test Description'
        datecreated = '01/01/23'
        deadline = '01/12/23'
        status = 'Open'
        quotation = 150
        conn = database_connection()
        conn.execute('INSERT INTO Jobs (title, description, datecreated, deadline, status, quotation) VALUES (?, ?, ?, ?, ?, ?)',
                        (title, description, datecreated, deadline, status, quotation))
        conn.commit()
        conn.close()
        conn = database_connection()
        job_data = conn.execute('SELECT * FROM Jobs WHERE title = ?', (title,)).fetchone()
        conn.close()
        self.assertEqual(job_data['title'], title)
        self.assertEqual(job_data['description'], description)
        self.assertEqual(job_data['datecreated'], datecreated)
        self.assertEqual(job_data['deadline'], deadline)
        self.assertEqual(job_data['status'], status)
        self.assertEqual(job_data['quotation'], quotation)

    def test_modifying_job(self):
        title = 'Updated Title'
        conn = database_connection()
        jobid = conn.execute('SELECT jobid FROM Jobs WHERE title = ?', ('Test Job UnitTest',)).fetchone()['jobid']
        conn.execute('UPDATE Jobs SET title = ? WHERE jobid = ?', (title, jobid))
        conn.commit()
        conn.close()
        conn = database_connection()
        job_data = conn.execute('SELECT * FROM Jobs WHERE jobid = ?', (jobid,)).fetchone()
        conn.close()
        self.assertEqual(job_data['title'], title)

    def test_deleting_job(self):
        conn = database_connection()
        jobid = conn.execute('SELECT jobid FROM Jobs WHERE title = ?', ('1111',)).fetchone()['jobid']
        conn.execute('DELETE FROM Jobs WHERE jobid = ?', (jobid,))
        conn.commit()
        conn.close()
        conn = database_connection()
        job_data = conn.execute('SELECT * FROM Jobs WHERE jobid = ?', (jobid,)).fetchone()
        conn.close()
        self.assertIsNone(job_data)

#Running the unit tests
tests()