#!/home/maharshmellow/anaconda3/bin/python3.5
# -*- coding: UTF-8 -*-

import cgitb
import os
import cgi
import mysql.connector
import time
from emailValidation import *
import hashlib
from shutil import copy

cgitb.enable()

print("Content-Type: text/html;charset=utf-8")
print()

def main():
    try:
        form = cgi.FieldStorage()
        email = form.getvalue("email").lower()
        password = form.getvalue("password")

        # check if email is valid
        if validateEmail(email):
            responsecode = saveUser(email, password)
        else:
            responsecode = 3    # invalid email

    except:
        responsecode = 2    # server error

    print(responsecode)

def saveUser(email, password):
    cnx = mysql.connector.connect(user="FILLER_USERNAME", password="FILLER_PASSWORD", host="FILLER_HOST", database="FILLER_DBNAME")
    cursor = cnx.cursor()       # holds the information when the table is queried

    currentTime = time.time()

    hashedPassword = hashlib.sha512((email + password).encode("utf-8")).hexdigest()

    add_user = ("INSERT INTO users (userid, email, password, joined, lastlogin) VALUES (%s, %s, %s, %s, %s)")
    data_user = (cursor.lastrowid, email, hashedPassword, currentTime, currentTime)

    # run the query
    try:
        cursor.execute(add_user, data_user)
        cnx.commit()
        cnx.close()
        responsecode = 0

    except:
        return(1)   # users already exists

    saveInitialBook(email)  # copies the template book and assigns the copied file to the user

    return(responsecode)

def saveInitialBook(email):
    """saves a book with title = hashed email"""

    bookname = hashlib.sha512((email + "cow").encode("utf-8")).hexdigest()
    copy("/var/www/books/intro.obj", "/var/www/books/"+bookname+".obj")

main()

# responsecode
# 0 = good
# 1 = user already exists
# 2 = server error occured
# 3 = invalid email
