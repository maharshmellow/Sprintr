#!/home/maharshmellow/anaconda3/bin/python3.5
# -*- coding: UTF-8 -*-
# TODO NOT YET COMPLETE - DOES NOT WORK AND IS NOT IMPLEMENTED

import cgitb
import cgi
import mysql.connector

cgitb.enable()

print("Content-Type: text/html;charset=utf-8")
print()

form = cgi.FieldStorage()
email = form.getvalue("email").lower()
position = int(form.getvalue("position"))    # the position to start reading at for the next time

cnx = mysql.connector.connect(user="FILLER_USERNAME", password="FILLER_PASSWORD", host="FILLER_HOST", database="FILLER_DBNAME")
cursor = cnx.cursor(buffered=True)

query=("UPDATE users SET lastPosition=%s WHERE email=%s")
cursor.execute(query, (position, email))
cnx.commit()

cnx.close()
