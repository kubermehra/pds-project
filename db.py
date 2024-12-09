import mysql.connector
from flask import request, jsonify
from mysql.connector import cursor



db=mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="pds"
)

db.autocommit=True



def insert_data():
    if request.method == 'POST':
        username=request.form['username']
        password = request.form['pass']
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        phone = request.form['phone']

        
        
        user=(username,password,fname,lname,email)

        cursor=db.cursor(buffered=True)
        users=cursor.execute(f"SELECT userName FROM Person where userName = '{username}' ")

        if users == None:
            query="INSERT INTO Person(userName,password,fname,lname,email) VALUES (%s,%s,%s,%s,%s);"
            cursor.execute(query,user)
            return True
        else:
            return False


def check_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['pass']
        print(username)
        
        cursor=db.cursor(dictionary=True)

        user_data=cursor.execute(f"Select * from Person where username='{username}' and password='{password}'")
        user_data=cursor.fetchone()
        if user_data == None:
            return False, "", ""
        else:
            return True, user_data["email"], user_data["fname"]

def get_item_data():
    if request.method == 'POST':
        itemId=request.form['itemID']
        cursor=db.cursor(dictionary=True,buffered=True)
        cursor.execute(f"select roomNum,\
                                     shelfNum\
                                     From Piece\
                                     where itemID= {itemId} ",)
        
        location_data=cursor.fetchall()
        cursor.close()
        print(location_data)
        if len(location_data)==0:
            return False,[]
        else:
            return True, location_data

