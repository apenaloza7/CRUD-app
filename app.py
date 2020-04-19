from flask import Flask, render_template

"""
Main file for my CRUD application for 471
This file serves as the main file that creates the app and houses routes
Program uses Python 3.73, Flask, SQL Alchemy, a mySQL server, and PHPmyAdmin

Author - Alejandro Penaloza
Last updated - 4/18/2020
"""

# Creating the app using Flask
app = Flask(__name__)

# Create router for the landing page
@app.route('/')
def Index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug = True)

