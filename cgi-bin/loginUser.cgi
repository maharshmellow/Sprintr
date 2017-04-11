#!/home/maharshmellow/anaconda3/bin/python3.5
# -*- coding: UTF-8 -*-

import cgitb
import os
import cgi
import mysql.connector
import time
import hashlib

cgitb.enable()

print("Content-Type: text/html;charset=utf-8")
print()

def main():
    form = cgi.FieldStorage()
    email = form.getvalue("email").lower()
    password = form.getvalue("password")

    cnx = mysql.connector.connect(user="FILLER_USERNAME", password="FILLER_PASSWORD", host="FILLER_HOST", database="FILLER_DBNAME")
    cursor = cnx.cursor(buffered=True)       # holds the information when the table is queried

    if validateLogin(email, password, cnx, cursor)  == 0:
        # username / password not found
        print(1)
    else:
        # update lastlogin time after successful login
        query = ("UPDATE users SET lastlogin=%s WHERE email=%s")
        t = int(time.time())
        cursor.execute(query, (t, email))
        cnx.commit()
        print("https://www.maharsh.net/cgi-bin/sprintr/reader.cgi?a=" + hashlib.sha512((email + "cow").encode("utf-8")).hexdigest() + "&b=" + email + "&c=" + str(t))
        # proper url: http://ec2.maharsh.net/cgi-bin/reader.cgi?e=email&a=hashedEmail&i=lastTime

    cnx.close()

def validateLogin(email, password, cnx, cursor):
    query = ("SELECT * FROM users WHERE email=%s AND password=%s")
    hashedPassword = hashlib.sha512((email + password).encode("utf-8")).hexdigest()

    cursor.execute(query, (email, hashedPassword))
    return(cursor.rowcount) # 0 if not matched to any user
main()
