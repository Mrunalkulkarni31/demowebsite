from flask import Flask, render_template,flash,redirect ,url_for,session
from flask_sqlalchemy import SQLAlchemy
from flask import request
import sqlalchemy 
from flask import Flask
from flask_mysqldb import MySQL
import re
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

import plotly.graph_objects as go



mysql = MySQL()
app = Flask(__name__)
db = SQLAlchemy(app)


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

@app.route("/secondpage")
def secondpage():
 return render_template('secondpage.html')

@app.route("/visualization")
def visualisation():
    
    data = pd.read_csv(r"C:\\Users\\Hp\AppData\\Local\\Programs\\Python\\Python39\\Subject wise data.csv")
    data.columns



    y1 = data.loc[0,"UT_1_CA"]
    y2 = data.loc[0,"Sem_1_CA"]
    y3 = data.loc[0,"UT_2_CA"]
    y4 = data.loc[0,"Sem_2_CA"]
    y_values = [y1,y2,y3,y4]

    x1= data.loc[0,"UT_1_AVG"]
    x2 = data.loc[0,"Sem_1_AVG"]
    x3 = data.loc[0,"UT_2_AVG"]
    x4 = data.loc[0,"Sem_2_AVG"]
    x_values = [x1,x2,x3,x4]

    x = ['UT_1','Sem_1','UT_2','Sem_2']

    plt.fill_between(x,x_values,alpha = 0.5,color="skyblue",edgecolor='black',label="Individual Performance")
    plt.fill_between(x,y_values,alpha = 0.2,color="red",edgecolor='black',label="Average Class Performance")
    plt.grid(True)
    plt.legend(loc=4)
    plt.title("Performance of Rina")
    plt.ylabel("Performance")
    plt.show()


    a1 = data.loc[19,"UT_1_CA"]
    a2 = data.loc[19,"Sem_1_CA"]
    a3 = data.loc[19,"UT_2_CA"]
    a4 = data.loc[19,"Sem_2_CA"]
    a_values = [a1,a2,a3,a4]

    b1= data.loc[19,"UT_1_AVG"]
    b2 = data.loc[19,"Sem_1_AVG"]
    b3 = data.loc[19,"UT_2_AVG"]
    b4 = data.loc[19,"Sem_2_AVG"]
    b_values = [b1,b2,b3,b4]

    plt.fill_between(x,a_values,alpha = 0.5,color="skyblue",edgecolor='black',label="Individual Performance")
    plt.fill_between(x,b_values,alpha = 0.3,color="red",edgecolor='black',label="Average Class Performance")
    plt.legend(loc=4)
    plt.title("Performance of Nikhil")
    plt.ylabel("Performance")
    plt.show()

    return render_template('index.html')




    
@app.route("/parents_login" , methods=['GET', 'POST'])
def Parents_Login():
    msg = "Logged in!"
    def login():
    # Output message if something goes wrong...
     
    
       # Check if "username" and "password" POST requests exist (user submitted form)
     if request.method == 'POST':
        # Create variables for easy access
        username = request.form['Username']
        password = request.form['Password']
        print(username,password)
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
# Username
# Teacher_Name
# Gender
# Nationality
# Education
# Teaching_Qualification
# Experience_in_the_field
# Passwor

class teachers_dataset(db.Model):
    
    Username = db.Column(db.String(50), primary_key=True)
    Teacher_Name = db.Column(db.String(80), nullable=False)
    Gender = db.Column(db.String(80), nullable=False)
    Nationality  = db.Column(db.String(80), nullable=False)
    Education = db.Column(db.String(80), nullable=False)
    Teaching_Qualification = db.Column(db.String(80), nullable=False)
    Experience_in_the_field = db.Column(db.String(80), nullable=False)
    Password = db.Column(db.String(80), nullable=False)

    @app.route("/teachers_login" ,methods = ['GET','POST'])
    def Teachers_Login():
        username1 = request.form.get('username1')
        password1 = request.form.get('password1')
        return "the username is {} and password is {}".format(username1,password1)


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

