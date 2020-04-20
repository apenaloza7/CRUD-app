from flask import Flask, render_template, request, redirect, url_for, flash
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

# Configurations for the database
config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'port': '8889',
    'database': 'csc471',
    'raise_on_warnings': True,
}

# Give the database a variable
db = mysql.connector.connect(**config)

# Create a cursor for the database
dbCursor = db.cursor()


# Create router for the landing page
@app.route('/')
def Index():
    dbCursor.execute("SELECT * FROM employee")
    allData = dbCursor.fetchall()

    return render_template("index.html", employees = allData)


# TODO: follow mysql.connector guide to udpate this method
@app.route('/insert', methods = ['POST'])
def insertEmployee():

    addEmployeeCommand = ("INSERT INTO employee (SSN, DOB, Fname, Minit, Lname, Address) VALUES (%s, %s, %s, %s, %s, %s)")

    if request.method == 'POST':
        SSN = request.form['SSN']
        DOB = request.form['DOB']
        Fname = request.form['Fname']
        Minit = request.form['Minit']
        Lname = request.form['Lname']
        Address = request.form['Address']

    employeeData = (SSN, DOB, Fname, Minit, Lname, Address)

    dbCursor.execute(addEmployeeCommand, employeeData)
    db.commit()

    flash("Employee inserted successfully")

    return redirect(url_for('Index'))


@app.route('/updateEmployee', methods = ['GET', 'POST'])
def updateEmployee():

    updateDOB = ("UPDATE employee SET DOB = %s WHERE SSN = %s")
    updateFname = ("UPDATE employee SET Fname = %s WHERE SSN = %s")
    updateMinit = ("UPDATE employee SET Minit = %s WHERE SSN = %s")
    updateLname = ("UPDATE employee SET Lname = %s WHERE SSN = %s")
    updateAddress = ("UPDATE employee SET Address = %s WHERE SSN = %s")

    if request.method == 'POST':
        SSN = request.form['SSN']
        requestedDOB = request.form['DOB']
        requestedFname = request.form['Fname']
        requestedMinit = request.form['Minit']
        requestedLname = request.form['Lname']
        requestedAddress = request.form['Address']

    newValueDOB = (requestedDOB, SSN)
    newValueFname = (requestedFname, SSN)
    newValueMinit = (requestedMinit, SSN)
    newValueLname = (requestedLname, SSN)
    newValueAddress = (requestedAddress, SSN)

    dbCursor.execute(updateDOB, newValueDOB)
    dbCursor.execute(updateFname, newValueFname)
    dbCursor.execute(updateMinit, newValueMinit)
    dbCursor.execute(updateLname, newValueLname)
    dbCursor.execute(updateAddress, newValueAddress)

    db.commit()
    flash("Employee updated successfully")
    
    return redirect(url_for('Index'))
        

@app.route('/deleteEmployee/<SSN>', methods = ['GET', 'POST'])
def deleteEmployee(SSN):

    deleteEmployeeCommand = ("DELETE FROM employee WHERE SSN = %s")
    employeeSSN = (SSN, )
    dbCursor.execute(deleteEmployeeCommand, employeeSSN)

    db.commit()
    flash("Employee deleted successfully")

    return redirect(url_for('Index'))

if __name__ == "__main__":
    app.run()
