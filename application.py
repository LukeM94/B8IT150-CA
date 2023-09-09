#Importing the required libraries
import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort, make_response
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
from werkzeug.exceptions import abort
from flask_bcrypt import Bcrypt
from reportlab.pdfgen import canvas

#Creating the Flask application. If the system was being deployed for real customers I'd make the secret key more secure
app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = '1234567890'
login_manager = LoginManager(app)
login_manager.login_view = 'login'
bcrypt = Bcrypt(app)

#Creating the database connection to freelanceflow.db
def database_connection():
    conn = sqlite3.connect('freelanceflow.db')
    conn.row_factory = sqlite3.Row
    return conn

#Creating the User class used by Flask-Login
class User(UserMixin):
    def __init__(self, id, emailaddress, password, firstname, lastname, username, accounttype):
        self.id = id
        self.emailaddress = emailaddress
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.accounttype = accounttype
        self.authenticated = False

    def is_active(self):
        return self.authenticated
    def is_anonymous(self):
        return False
    def is_authenticated(self):
        return self.authenticated
    def get_id(self):
        return self.id

#Creating the load_user function used by Flask-Login
@login_manager.user_loader
def load_user(user_id):
    conn = database_connection()
    user_data = conn.execute('SELECT * FROM Users WHERE userid = ?', (user_id,)).fetchone()
    conn.close()
    if user_data is None:
        return None
    user = User(user_data['userid'], user_data['emailaddress'], user_data['password'], user_data['firstname'], user_data['lastname'], user_data['username'], user_data['accounttype'])
    return user

#Function to get one job from the database based on the Job ID
def get_job(job_id):
    conn = database_connection()
    job = conn.execute('SELECT * FROM Jobs WHERE jobid = ?', (job_id,)).fetchone()
    conn.close()
    if job is None:
        abort(404)
    return job

#Function to get all jobs from the database where the current user is the creator
def get_all_jobs():
    conn = database_connection()
    all_jobs = conn.execute('SELECT * FROM Jobs WHERE createdby = ?', (current_user.id,)).fetchall()
    conn.close()
    return all_jobs

#Function to get all users from the database
def get_all_users():
    conn = database_connection()
    all_users = conn.execute('SELECT * FROM Users').fetchall()
    conn.close()
    return all_users

#Creating the routes for the application
#This route is for the homepage
@app.route('/')
def index():
    return render_template('index.html')

#This route is for the about page
@app.route('/about')
def about():
    return render_template('about.html')

#This route is for the calendar page
#Function gets all jobs from the database where the current user is the creator and displays them in the calendar
@app.route('/calendar')
@login_required
def calendar():
    conn = database_connection()
    Jobs = conn.execute('SELECT * FROM Jobs WHERE createdby = ?', (current_user.id,)).fetchall()
    conn.close()

    events = []
    for job in Jobs:
        events.append({
            'title': job['title'],
            'start': job['deadline']
        })
    return render_template('calendar.html', events=events)

#This route is for the jobs page
#Function gets all jobs from the database where the current user is the creator. If there are no jobs, the user is redirected to the createjob page with a message to create their first job
@app.route('/jobs')
@login_required
def jobs():
    conn = database_connection()
    Jobs = conn.execute('SELECT * FROM Jobs WHERE createdby = ?', (current_user.id,)).fetchall()
    conn.close()
    if not Jobs:
        flash('Create your first job here!')
        return redirect(url_for('createjob'))
    else:
        return render_template('jobs.html', Jobs=Jobs)

#This route is for the register page
#Function checks if all fields are filled in and then inserts the data into the database
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        emailaddress = request.form['emailaddress']
        firstname = request.form['firstname']
        lastname = request.form['lastname']

        if not username or not password or not emailaddress or not firstname or not lastname:
            flash('All fields are required!')
        else:
            pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
            conn = database_connection()
            conn.execute('INSERT INTO Users (username, password, emailaddress, firstname, lastname) VALUES (?, ?, ?, ?, ?)',
                         (username, pw_hash, emailaddress, firstname, lastname))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))

    return render_template('register.html')

#This route is for the login page
#Function checks if the email address and password are correct and then logs the user in. If the email address or password are incorrect a message is displayed stating the email address or password is invalid
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    if request.method == 'POST':
        emailaddress = request.form['emailaddress']
        password = request.form['password']

        conn = database_connection()
        user_data = conn.execute('SELECT * FROM Users WHERE emailaddress = ?', (emailaddress,)).fetchone()
        conn.close()

        if user_data and bcrypt.check_password_hash(user_data['password'], password):
            user = User(user_data['userid'], user_data['emailaddress'], user_data['password'], user_data['firstname'], user_data['lastname'], user_data['username'], user_data['accounttype'])
            user.authenticated = True
            login_user(user)
            return redirect(url_for('profile'))
        else:
            flash('Invalid email address or password!')

    return render_template('login.html')

#This route is for the logout page. The function logs the user out and redirects them to the homepage
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

#This route is for the profile page
@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

#This route is for the job page
#Function gets the job from the database based on the Job ID and displays it
@app.route('/<int:job_id>')
@login_required
def job(job_id):
    job = get_job(job_id)
    return render_template('job.html', job=job)

#This route is for the createjob page
#Function checks if all fields are filled in and then inserts the data into the database
@app.route('/createjob', methods=('GET', 'POST'))
@login_required
def createjob():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        datecreated = request.form['datecreated']
        deadline = request.form['deadline']
        status = request.form['status']
        quotation = request.form['quotation']

        if not title or not description:
            flash('Title and Description are required!')
        else:
            conn = database_connection()
            conn.execute('INSERT INTO Jobs (title, description, datecreated, deadline, status, quotation, createdby) VALUES (?, ?, ?, ?, ?, ?, ?)',
                         (title, description, datecreated, deadline, status, quotation, current_user.id))
            conn.commit()
            conn.close()
            return redirect(url_for('jobs'))

    return render_template('createjob.html')

#This route is for the modifyjob page
#Function gets the job from the database based on the Job ID and displays it
#Function also checks if all fields are filled in and then updates the data in the database
@app.route('/<int:job_id>/modifyjob', methods=('GET', 'POST'))
@login_required
def modifyjob(job_id):
    job = get_job(job_id)

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        datecreated = request.form['datecreated']
        deadline = request.form['deadline']
        status = request.form['status']
        quotation = request.form['quotation']
        createdby = current_user.id

        conn = database_connection()
        conn.execute('UPDATE Jobs SET title = ?, description = ?, datecreated = ?, deadline = ?, status = ?, quotation = ?, createdby = ? WHERE jobid = ?', (title, description, datecreated, deadline, status, quotation, createdby, job_id))
        conn.commit()
        conn.close()
        return redirect(url_for('jobs'))

    return render_template('modifyjob.html', job=job)

#This route is to delete a job
#Function deletes the job from the database based on the Job ID
@app.route('/<int:job_id>/deletejob', methods=('GET', 'POST'))
@login_required
def deletejob(job_id):
    job = get_job(job_id)
    conn = database_connection()
    conn.execute('DELETE FROM Jobs WHERE jobid = ?', (job_id,))
    conn.commit()
    conn.close()
    flash('Job deleted!')
    return redirect(url_for('jobs'))

#This route is for the admin page
#Function checks the current user is an admin and gets all users from the database and displays them
@app.route('/admin')
@login_required
def admin():
    if current_user.accounttype == 'admin':
        all_users = get_all_users()
        return render_template('admin.html', all_users)
    else:
        return redirect(url_for('index'))

#This route is to generate a report
#Function generates a PDF report with all jobs from the database where the current user is the creator
# TO DO - Add more job data
@app.route('/generate_report')
@login_required
def generate_report():
    pdf = canvas.Canvas('report.pdf', pagesize=(595.27, 841.89))
    pdf.setTitle('FreelanceFlow Report')
    pdf.setFont('Helvetica', 12)

    pdf.drawString(100, 800, 'Below is a list of all your jobs:')

    all_jobs = get_all_jobs()

    line_height = 800

    for job in all_jobs:
        line_height = line_height - 20
        job_string = job['title'] + ' - ' + job['description']
        pdf.drawString(100, line_height, job_string)

    pdf.showPage()
    pdf.save()

    response = make_response(open('report.pdf', 'rb').read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=report.pdf'

    return response

#This route is for the search page
#Function gets all jobs from the database where the title or ID match the search term AND where the current user is the creator and displays them
@app.route('/search', methods=['GET'])
@login_required
def search():
    search_term = request.args.get('search_term')

    if search_term is None:
        return render_template('search.html')
    else:
        conn = database_connection()
        Jobs = conn.execute('SELECT * FROM Jobs WHERE (title LIKE ? OR jobid LIKE ?) AND createdby = ?', ('%' + search_term + '%', '%' + search_term + '%', current_user.id)).fetchall()
        conn.close()
        return render_template('search.html', Jobs=Jobs, search_term=search_term)

#This block of code runs the application
if __name__ == '__main__':
    app.run(port='8000')