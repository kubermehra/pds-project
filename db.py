import mysql.connector
from flask import request, jsonify



db=mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="pds"
)


cursor=db.cursor()

cursor.execute("SELECT NOW()")

ans=cursor.fetchone()

print(ans[0])
 


# # client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
# # userdb = client['bigdata']
# # users = userdb.users


# def insert_data():
#     if request.method == 'POST':
#         name = request.form['name']
#         email = request.form['email']
#         password = request.form['pass']
        
#         reg_user = {}
#         reg_user['name'] = name
#         reg_user['email'] = email
#         reg_user['password'] = password
        
#         if users.find_one({"email": email}) == None:
#             users.insert_one(reg_user)
#             return True
#         else:
#             return False


# def check_user():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['pass']
        
#         user = {
#             "email": email,
#             "password": password
#         }
        
#         user_data = users.find_one(user)
#         if user_data == None:
#             return False, ""
#         else:
#             return True, user_data["email"], user_data["name"]
