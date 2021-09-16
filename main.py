from flask import Flask, render_template,flash,redirect ,url_for,session
from flask_sqlalchemy import SQLAlchemy
from flask import request
import sqlalchemy 
from flask import Flask
from flask_mysqldb import MySQL
import re


mysql = MySQL()
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/ethdatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ""
app.config['MYSQL_DATABASE_DB'] = "ethdatabase"
app.config['MYSQL_DATABASE_HOST'] = "localhost"
mysql.init_app(app)
db = SQLAlchemy(app)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/students_login")
def StudentsLogin():
    return render_template('studlogin.html')



class Parentsdata(db.Model):
    Username = db.Column(db.String(80), primary_key=True)
    Password = db.Column(db.String(20), nullable=False)
    
@app.route("/parents_login" , methods=['GET', 'POST'])
def Parents_Login():
    def login():
    # Output message if something goes wrong...
     
    
       # Check if "username" and "password" POST requests exist (user submitted form)
     if request.method == 'POST' and 'Username' in request.form and 'Password' in request.form:
        # Create variables for easy access
        username = request.form['Username']
        password = request.form['Password']
         # Check if account exists using MySQL
        cursor = MySQL.connect.cursor()
        cursor.execute('SELECT * FROM parentsdata WHERE username = %s AND password = %s', (username, password,))
          # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['Username'] = account['Username']
            # Redirect to home page
            return 'Logged in successfully!'
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('parentlog1.html')

@app.route("/teachers_login")
def Teachers_Login():
    return render_template('teacherlog.html')

@app.route("/administration_login")
def Administration_Login():
    return render_template('adminlog.html')


class Contacts(db.Model):
    
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    subject = db.Column(db.String(120), nullable=False)
    message = db.Column(db.String(120), nullable=False)
    

@app.route("/contact", methods = ['GET', 'POST'])

def Contact():
    if( request.method =='POST'):
        '''Add entry to the database'''
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        entry = Contacts(name=name, email = email, subject = subject, message = message )
        db.session.add(entry)
        db.session.commit()
    return render_template('index.html')



app.run(debug=True)

