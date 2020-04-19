from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import mysql.connector

"""
Main file for my CRUD application for 471
This file serves as the main file that creates the app and houses routes
Program uses Python 3.73, Flask, SQL Alchemy, a mySQL server, and PHPmyAdmin

Author - Alejandro Penaloza
Last updated - 4/18/2020
"""

# Creating the app using Flask
app = Flask(__name__)
app.secret_key = "mysecretkey"

config = {
  'user': 'root',
  'password': 'root',
  'host': 'localhost:8889',
  'database': 'inventory',
  'raise_on_warnings': True,
}

db = mysql.connector.connect(**config)

# db = SQLAlchemy(app)

# Create router for the landing page
@app.route('/')
def Index():
    return render_template("index.html")

# TODO: follow mysql.connector guide to udpate this method
@app.route('/insert', methods = ['POST'])
def insertEmployee():
    if request.method == 'POST':
        SSN = request.form['SSN']
        DOB = request.form['DOB']
        Fname = request.form['Fname']
        Minit = request.form['Minit']
        Lname = request.form['Lname']
        Address = request.form['Address']

    my_employee = 

    return redirect(url_for('Index'))
        
if __name__ == "__main__":
    app.run(debug = True)

