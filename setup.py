from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

"""
Main file for my CRUD application for 471
This file serves as the main file that creates the app and houses routes
Program uses Python 3.73, Flask, SQL Alchemy, a mySQL server, and PHPmyAdmin

Author - Alejandro Penaloza
Last updated - 4/22/2020
"""

#######################################################################################
#                                   WEB APP AND DATABASE SETUP
#######################################################################################


# Creating the app using Flask
app = Flask(__name__)
app.secret_key = "mysecretkey"

# Configurations for the database

# HEROKU DATABASE
"""
config = {
    'user': 'b273314baed36f',
    'password': '58715fe4',
    'host': 'us-cdbr-iron-east-01.cleardb.net',
    'port': '3306',
    'database': 'heroku_f0232cf140aaa44',
    'raise_on_warnings': True,
}
"""

# LOCAL DATABASE

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

#######################################################################################
#                                   CONTROLS FOR THE MAIN PAGE
#######################################################################################

# Create router for the landing page
@app.route('/')
def Index():

    dbCursor.execute("SELECT * FROM employee")
    allData = dbCursor.fetchall()

    dbCursor.execute("SELECT * FROM department")
    departmentData = dbCursor.fetchall()

    dbCursor.execute("SELECT * FROM project")
    projectData = dbCursor.fetchall()

    dbCursor.execute("SELECT * FROM works")
    worksData = dbCursor.fetchall()

    return render_template("index.html", employees = allData, departments = departmentData, projects = projectData, works = worksData)

#######################################################################################
#                                   CONTROLS FOR THE EMPLOYEE DATABASE
#######################################################################################

@app.route('/insertEmployee', methods = ['POST'])
def insertEmployee():

    addEmployeeCommand = ("INSERT INTO employee (SSN, DOB, Fname, Minit, Lname, Address) VALUES (%s, %s, %s, %s, %s, %s)")

    if request.method == 'POST':
        SSN = request.form['SSN']
        DOB = request.form['DOB']
        Fname = request.form['Fname']
        Minit = request.form['Minit']
        Lname = request.form['Lname']
        Address = request.form['Address']

    try:
        employeeData = (SSN, DOB, Fname, Minit, Lname, Address)

        dbCursor.execute(addEmployeeCommand, employeeData)
        db.commit()
        flash("Employee inserted successfully", 'employee')
    except:
        db.rollback()
        flash("SSN ALREADY EXISTS. TRY AGAIN", "employee")

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


#######################################################################################
#                                   CONTROLS FOR THE DEPARTMENT DATBASE
#######################################################################################

@app.route('/insertDepartment', methods = ['POST'])
def insertDepartment():

    addDepartmentCommand = ("INSERT INTO department (DeptNum, DeptName, managerSSN) VALUES (%s, %s, %s)")

    if request.method == 'POST':
        DeptNum = request.form['DeptNum']
        DeptName = request.form['DeptName']
        managerSSN = request.form['managerSSN']

    try:
        departmentData = (DeptNum, DeptName, managerSSN)

        dbCursor.execute(addDepartmentCommand, departmentData)
        db.commit()
        flash("Department inserted successfully")
    except:
        db.rollback()
        flash("DEPARTMENT ALREADY EXISTS. TRY AGAIN")

    return redirect(url_for('Index'))


@app.route('/updateDepartment', methods = ['GET', 'POST'])
def updateDepartment():

    updateDepartmentName = ("UPDATE department SET DeptName = %s WHERE DeptNum = %s")
    updateManagerSSN = ("UPDATE department SET managerSSN = %s WHERE DeptNum = %s")

    if request.method == 'POST':
        DeptNum = request.form['DeptNum']
        requestedDeptName = request.form['DeptName']
        requestedManagerSSN = request.form['managerSSN']

    newValueDeptName = (requestedDeptName, DeptNum)
    newValueManagerSSN = (requestedManagerSSN, DeptNum)

    dbCursor.execute(updateDepartmentName, newValueDeptName)
    dbCursor.execute(updateManagerSSN, newValueManagerSSN)

    db.commit()
    flash("Department updated successfully")

    return redirect(url_for('Index'))


@app.route('/deleteDepartment/<DeptNum>', methods = ['GET', 'POST'])
def deleteDepartment(DeptNum):

    deleteDepartmentCommand = ("DELETE FROM department WHERE DeptNum = %s")
    DeptNum = (DeptNum, )
    dbCursor.execute(deleteDepartmentCommand, DeptNum)

    db.commit()
    flash("Department deleted successfully")

    return redirect(url_for('Index'))


#######################################################################################
#                                   CONTROLS FOR THE PROJECT DATBASE
#######################################################################################

@app.route('/insertProject', methods = ['POST'])
def insertProject():

    addProjectCommand = ("INSERT INTO project (ProjName, ProjNum, ProjDesc) VALUES (%s, %s, %s)")

    if request.method == 'POST':
        ProjName = request.form['ProjName']
        ProjNum = request.form['ProjNum']
        ProjDesc = request.form['ProjDesc']

    try:
        projectData = (ProjName, ProjNum, ProjDesc)

        dbCursor.execute(addProjectCommand, projectData)
        db.commit()
        flash("Project inserted successfully")
    except:
        db.rollback()
        flash("PROJECT ALREADY EXISTS. TRY AGAIN")

    return redirect(url_for('Index'))


@app.route('/updateProject', methods = ['GET', 'POST'])
def updateProject():

    updateProjName = ("UPDATE project SET ProjName = %s WHERE ProjNum = %s")
    updateProjDesc = ("UPDATE project SET ProjDesc = %s WHERE ProjNum = %s")

    if request.method == 'POST':
        ProjNum = request.form['ProjNum']
        requestedProjName = request.form['ProjName']
        requestedProjDesc = request.form['ProjDesc']

    newValueProjName = (requestedProjName, ProjNum)
    newValueProjDesc = (requestedProjDesc, ProjNum)

    dbCursor.execute(updateProjName, newValueProjName)
    dbCursor.execute(updateProjDesc, newValueProjDesc)

    db.commit()
    flash("Project updated successfully")

    return redirect(url_for('Index'))


@app.route('/deleteProject/<ProjNum>', methods = ['GET', 'POST'])
def deleteProject(ProjNum):

    deleteProjectCommand = ("DELETE FROM project WHERE ProjNum = %s")
    ProjNum = (ProjNum, )
    dbCursor.execute(deleteProjectCommand, ProjNum)

    db.commit()
    flash("Project deleted successfully")

    return redirect(url_for('Index'))

#######################################################################################
#                                   CONTROLS FOR THE WORKS DATBASE
#######################################################################################

@app.route('/insertWorks', methods = ['POST'])
def insertWorks():

    addWorksCommand = ("INSERT INTO works (SSN, ProjName, ProjNum, DeptNum) VALUES (%s, %s, %s, %s)")

    if request.method == 'POST':
        SSN = request.form['SSN']
        ProjName = request.form['ProjName']
        ProjNum = request.form['ProjNum']
        DeptNum = request.form['DeptNum']

    try:
        worksData = (SSN, ProjName, ProjNum, DeptNum)

        dbCursor.execute(addWorksCommand, worksData)
        db.commit()
        flash("Work relationship inserted successfully")
    except:
        db.rollback()
        flash("INVALID VALUES TRY AGAIN")

    return redirect(url_for('Index'))


@app.route('/updateWorks', methods = ['GET', 'POST'])
def updateWorks():

    updateProjName = ("UPDATE works SET ProjName = %s WHERE SSN = %s")
    updateProjNum = ("UPDATE works SET ProjNum = %s WHERE SSN = %s")
    updateDeptNum = ("UPDATE works SET DeptNum = %s WHERE SSN = %s")

    if request.method == 'POST':
        SSN = request.form['SSN']
        requestedProjName = request.form['ProjName']
        requestedProjNum = request.form['ProjNum']
        requestedDeptNum = request.form['DeptNum']

    try:
        newValueProjName = (requestedProjName, SSN)
        newValueProjNum = (requestedProjNum, SSN)
        newValuesDeptNum = (requestedDeptNum, SSN)

        dbCursor.execute(updateProjName, newValueProjName)
        dbCursor.execute(updateProjNum, newValueProjNum)
        dbCursor.execute(updateDeptNum, newValuesDeptNum)

        db.commit()
        flash("Work relationship updated successfully")
    except:
        db.rollback()
        flash("VALUES DO NOT MATCH")


    return redirect(url_for('Index'))


@app.route('/deleteWorks/<SSN>', methods = ['GET', 'POST'])
def deleteWorks(SSN):

    deleteWorksCommand = ("DELETE FROM works WHERE SSN = %s")
    SSN = (SSN, )
    dbCursor.execute(deleteWorksCommand, SSN)

    db.commit()
    flash("Works relationship deleted successfully")

    return redirect(url_for('Index'))

#######################################################################################
#                                   LAUNCH
#######################################################################################
if __name__ == "__main__":
    app.run()
