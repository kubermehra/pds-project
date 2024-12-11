import json
import mysql.connector
from flask import request, jsonify, session
from mysql.connector import cursor



db=mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="pds"
)

db.autocommit=True

def check_column_values(table_name, column_values):
    
    

    cursor = db.cursor(buffered=True)

    # Build the query
    conditions = " AND ".join([f"{column} = %s" for column in column_values.keys()])
    query = f"SELECT EXISTS (SELECT 1 FROM {table_name} WHERE {conditions})"
    
    # Execute the query
    cursor.execute(query, tuple(column_values.values()))
    result = cursor.fetchone()

    # Return True if the values exist, False otherwise
    return bool(result[0])

def dict_message(status,message):
    data={
        'status': status,
        'message' : message
    }
    return data


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
            return False, "", "", ""
        else:
            return True, user_data["email"], user_data["fname"], user_data['userName']

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

def get_order_data():
    if request.method == 'POST':
        orderID=request.form['orderID']
        cursor=db.cursor(dictionary=True,buffered=True)
        query = """
            SELECT 
                ii.ItemID,
                JSON_ARRAYAGG(
                    JSON_OBJECT(
                        'roomNum', p.roomNum,
                        'shelfNum', p.shelfNum
                    )
                ) AS Locations
            FROM 
                ItemIn ii
            JOIN 
                Ordered o ON ii.orderID = o.orderID
            JOIN 
                Piece p ON p.ItemID = ii.ItemID
            WHERE 
                o.orderID = %s
            GROUP BY 
                ii.ItemID;
            """
        cursor.execute(query,(orderID,))
        location_data=cursor.fetchall()
        cursor.close()
        print(location_data)
        if len(location_data)==0:
            return False,[]
        else:
            return True, location_data


def add_order():
    if request.method == 'POST':
        print("....... In add order..........\n\n")

        cursor=db.cursor(buffered=True)
        donorID=request.form['donorID']
        itemID=request.form['itemID']
        idescription=request.form['iDescription']
        pdescription=request.form['pDescription']
        photo=request.form['photo']
        color=request.form['color']
        isNew=int(request.form['isNew'] =='true')
        hasPieces=int(request.form['hasPieces'] == 'true')
        size=request.form['size']
        material=request.form['material']
        mainCategory=request.form['mainCategory']
        subCategory=request.form['subCategory']
        location=request.form['location']
        pNotes=request.form['pNotes']
        location=location.split(',')

        
        for i in location:
            if not i.isdigit():
                return dict_message(False,"Location not filled properly")

        roomNum=int(location[0])
        shelfNum=int(location[1])

        size=size.split(',')
        for i in size:
            if not i.isdigit():
                return dict_message(False,"Size not filled properly")

        length=int(size[0])
        width=int(size[1])
        height=int(size[2])

        query="""
        SELECT userName 
        FROM Act 
        WHERE userName = %s AND roleID = 'donor';
        """

        cursor.execute(query,(donorID, ))
        val=cursor.fetchone()
        if not val:
            return dict_message(False,"Wrong Donor username")
        else:
            if isNew:
                query = """
                INSERT INTO Category (mainCategory, subCategory)
                VALUES (%s, %s)
                """
                cursor.execute(query,(mainCategory,subCategory))
                db.commit()

                query = """
                INSERT INTO Item (
                    iDescription, 
                    photo, 
                    color, 
                    isNew, 
                    hasPieces, 
                    material, 
                    mainCategory, 
                    subCategory
                ) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                """
                cursor.execute(query, (idescription, photo, color, isNew, hasPieces, material, mainCategory, subCategory))

                db.commit()
                cursor=db.cursor(buffered=True)
                cursor.execute("Select LAST_INSERT_ID();")
                itemID=cursor.fetchone()[0]

            if not check_column_values('Item',{'ItemID':itemID}):
                return dict_message(False,"Item ID not correct")

            
            query="""
                Select max(pieceNum)
                From Piece
                Where ItemID=1
                group by ItemID;
                """
            cursor.execute(query)
            pieceNum=cursor.fetchone()
            if pieceNum==None:
                pieceNum=0
            else:
                pieceNum=pieceNum[0]
            pieceNum+=1

            query = """
            INSERT INTO Piece (
                ItemID, 
                pieceNum, 
                pDescription, 
                length, 
                width, 
                height, 
                roomNum, 
                shelfNum, 
                pNotes
            ) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            cursor.execute(query, (itemID, pieceNum, pdescription, length, width, height, roomNum, shelfNum, pNotes))
            db.commit()


            query="""
            INSERT INTO DonatedBy (
                ItemID, 
                userName, 
                donateDate
            ) 
            VALUES (%s, %s, NOW());"""
            cursor.execute(query,(itemID,donorID))
            db.commit()

            return dict_message(True,"Item added")

def get_orderID():
    if request.method=='POST':
        cursor=db.cursor(buffered=True)
        query="""
        SELECT MAX(`orderID`) 
        FROM Ordered
        """
        cursor.execute(query)
        orderID=cursor.fetchone()[0]
        orderID+=1
        return True,orderID

def get_category_options():
    if request.method=='POST':
        cursor=db.cursor(buffered=True)
        
        # Finds distinct main category

        query="""
        SELECT DISTINCT(mainCategory) FROM Category
        """
        cursor.execute(query)
        maincategory=cursor.fetchall()


        # Finds distinct sub category

        query="""
        SELECT DISTINCT(subCategory) FROM Category
        """
        cursor.execute(query)
        subcategory=cursor.fetchall()

        return maincategory,subcategory

def db_get_item_list():
    if request.method=='POST':
        query = """

        SELECT 
            i.ItemID, 
            i.iDescription
        FROM 
            Item i
        LEFT JOIN 
            ItemIn ii 
            ON i.ItemID = ii.ItemID AND ii.orderID = %s
        WHERE 
            i.mainCategory = %s 
            AND i.subCategory = %s 
            AND i.isNew = 1 
            AND ii.ItemID IS NULL;
        """
    cursor=db.cursor(buffered=True,dictionary=True)
    cursor.execute(query,(session['orderID'],request.form['mainCategory'],request.form['subCategory']))
    item_list=cursor.fetchall()
    return item_list

def db_prepare_order():
    if request.method=='POST':
        cursor=db.cursor(buffered=True,dictionary=True)
        orderID=request.form['orderID']
        # orderID=5

        #placing order in delivery room


        query="""
        UPDATE Piece
        SET roomNum = 10, shelfNum = 1
        WHERE ItemID IN (
            SELECT ItemID
            FROM ItemIn
            WHERE orderID = %s
        );

        """
        cursor.execute(query,(orderID,))
        db.commit()

        #updating new database
        query="""
        UPDATE Item
        SET isNew = 0
        WHERE ItemID IN (
            SELECT ItemID
            FROM ItemIn
            WHERE orderID = %s
        );
        """
        cursor.execute(query,(orderID,))
        db.commit()
        
        

        

        


        
        

