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
    #This test will create a user with the data below and verify it was inserted into the database as expected
    def a_test_user_registration(self):
        username = 'unittestuser'
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
        conn = database_connection()
        conn.execute('DELETE FROM Users WHERE username = ?', ('unittestuser',))
        conn.commit()
        conn.close()
    
    #This test will create a job with the data below and verify it was inserted into the database as expected
    def b_test_job_creation(self):
        title = 'Test Job UnitTest'
        description = 'Test Description'
        datecreated = '01/01/23'
        deadline = '01/12/23'
        status = 'Open'
        quotation = 150
        createdby = 8
        conn = database_connection()
        conn.execute('INSERT INTO Jobs (title, description, datecreated, deadline, status, quotation, createdby) VALUES (?, ?, ?, ?, ?, ?, ?)',
                        (title, description, datecreated, deadline, status, quotation, createdby))
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

    #This test will update the previously created job with a new title and verify it was inserted into the database as expected
    def c_test_modifying_job(self):
        title = 'Updated Title UnitTest'
        conn = database_connection()
        jobid = conn.execute('SELECT jobid FROM Jobs WHERE title = ?', ('Test Job UnitTest',)).fetchone()['jobid']
        conn.execute('UPDATE Jobs SET title = ? WHERE jobid = ?', (title, jobid))
        conn.commit()
        conn.close()
        conn = database_connection()
        job_data = conn.execute('SELECT * FROM Jobs WHERE jobid = ?', (jobid,)).fetchone()
        conn.close()
        self.assertEqual(job_data['title'], title)

    #This test will delete the previously updated job and verify it's no longer available in the database
    def d_test_deleting_job(self):
        conn = database_connection()
        job_to_delete = conn.execute('SELECT jobid FROM Jobs WHERE title = ?', ('Updated Title UnitTest',)).fetchone()['jobid']
        conn.execute('DELETE FROM Jobs WHERE jobid = ?', (job_to_delete,))
        conn.commit()
        conn.close()
        conn = database_connection()
        job_data = conn.execute('SELECT * FROM Jobs WHERE jobid = ?', (job_to_delete,)).fetchone()
        conn.close()
        self.assertEqual(job_data, None)

#Running the unit tests
tests()