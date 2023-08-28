import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort
from werkzeug.exceptions import abort

def database_connection():
    conn = sqlite3.connect('freelanceflow.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_job(job_id):
    conn = database_connection()
    job = conn.execute('SELECT * FROM Jobs WHERE jobid = ?', (job_id,)).fetchone()
    conn.close()
    if job is None:
        abort(404)
    return job

app = Flask(__name__)
#app.config['SECRET_KEY'] = '1234567890'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/calendar')
def calendar():
    return render_template('calendar.html')

@app.route('/jobs')
def jobs():
    conn = database_connection()
    Jobs = conn.execute('SELECT * FROM Jobs').fetchall()
    conn.close()
    return render_template('jobs.html', Jobs=Jobs)

@app.route('/<int:job_id>')
def job(job_id):
    job = get_job(job_id)
    return render_template('job.html', job=job)

@app.route('/createjob/', methods=('GET', 'POST'))
def createjob():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        datecreated = request.form['datecreated']
        deadline = request.form['deadline']
        status = request.form['status']
        quotation = request.form['quotation']

        if not title:
            flash('Title is required!')
        elif not description:
            flash('Description is required!')
        else:
            conn = database_connection()
            conn.execute('INSERT INTO Jobs (title, description, datecreated, deadline, status, quotation) VALUES (?, ?, ?, ?, ?, ?)',
                         (title, description, datecreated, deadline, status, quotation))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('createjob.html')

@app.route('/<int:job_id>/modifyjob/', methods=('GET', 'POST'))
def modifyjob(job_id):
    job = get_job(job_id)

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        datecreated = request.form['datecreated']
        deadline = request.form['deadline']
        status = request.form['status']
        quotation = request.form['quotation']

        if not title:
            flash('Title is required!')
        elif not description:
            flash('Description is required!')
        else:
            conn = database_connection()
            conn.execute('UPDATE Jobs SET title = ?, description = ?, datecreated = ?, deadline = ?, status = ?, quotation = ? WHERE jobid = ?', (title, description, datecreated, deadline, status, quotation))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('modifyjob.html', job=job)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080')