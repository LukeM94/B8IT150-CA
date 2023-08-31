import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
from werkzeug.exceptions import abort
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = '1234567890'
login_manager = LoginManager(app)
login_manager.login_view = "login"
bcrypt = Bcrypt(app)

def database_connection():
    conn = sqlite3.connect('freelanceflow.db')
    conn.row_factory = sqlite3.Row
    return conn

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

@login_manager.user_loader
def load_user(user_id):
    conn = database_connection()
    user_data = conn.execute('SELECT * FROM Users WHERE userid = ?', (user_id,)).fetchone()
    conn.close()
    if user_data is None:
        return None
    user = User(user_data['userid'], user_data['emailaddress'], user_data['password'], user_data['firstname'], user_data['lastname'], user_data['username'], user_data['accounttype'])
    return user

def get_job(job_id):
    conn = database_connection()
    job = conn.execute('SELECT * FROM Jobs WHERE jobid = ?', (job_id,)).fetchone()
    conn.close()
    if job is None:
        abort(404)
    return job

def get_all_users():
    conn = database_connection()
    all_users = conn.execute('SELECT * FROM Users').fetchall()
    conn.close()
    return all_users

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

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

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
        
@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@app.route('/<int:job_id>')
@login_required
def job(job_id):
    job = get_job(job_id)
    return render_template('job.html', job=job)

@app.route('/createjob/', methods=('GET', 'POST'))
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

@app.route('/<int:job_id>/modifyjob/', methods=('GET', 'POST'))
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

@app.route('/<int:job_id>/deletejob/', methods=('GET', 'POST'))
@login_required
def deletejob(job_id):
    job = get_job(job_id)
    conn = database_connection()
    conn.execute('DELETE FROM Jobs WHERE jobid = ?', (job_id,))
    conn.commit()
    conn.close()
    flash('Job deleted!')
    return redirect(url_for('jobs'))

@app.route('/admin')
@login_required
def admin():
    if current_user.accounttype == 'admin':
        all_users = get_all_users()
        return render_template('admin.html', all_users)
    else:
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080')