from pickle import TRUE
from re import sub
import stat
from kafka.metrics.stats import total
import db
import json
from flask import Flask, request, render_template, session, redirect, url_for, jsonify
from flask import jsonify
from googleapiclient.discovery import build
import isodate
import time

app = Flask(__name__)
app.secret_key = 'your_very_secure_secret_key'  # You should generate a secure key

# users = db.users
# trending_videos = db.userdb.trending_videos
# videos = db.userdb.videos
# most_watched_segment=db.userdb.most_watched_segment

# KAFKA_ENDPOINT = 'localhost:9093'

# kafkaProducer = KafkaProducer(
#     bootstrap_servers=[KAFKA_ENDPOINT],
#     value_serializer=lambda v: json.dumps(v).encode('utf-8')
# )




@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template("signup.html")


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    
    status, email, name , username= db.check_user()
    
    data = {
        "username": name,
        "status": status
    }
    if status:
        session['username'] = username  # Store the username in session
        session['email'] = email
    return json.dumps(data)


@app.route('/register', methods=['GET', 'POST'])
def register():
    status = db.insert_data()
    return json.dumps(status)


@app.route('/home', methods=['GET', 'POST'])
def display():
    username = session.get('username')
    email = session.get('email')
    return render_template("requiredfeatures.html")
    # else:
    #     return redirect(url_for('home'))  # Redirect to login if no user is logged in


@app.route('/find-item', methods=['GET','POST'])
def get_item():
    status,location_data=db.get_item_data()
    print(status)
    data={
        'status': status,
        'locations': location_data
    }
    return json.dumps(data)

@app.route('/find-order', methods=['GET','POST'])
def get_order():
    status,location_data=db.get_order_data()
    data={
        'status': status,
        'locations': location_data
    }
    return json.dumps(data)

@app.route('/add-donation', methods=['GET','POST'])
def add_donation():

    cursor=db.db.cursor(buffered=True,dictionary=True)
    query="""
        SELECT roleID
        FROM Act 
        WHERE userName = %s AND roleID = 'staff';
        """
    cursor.execute(query,(session['username'], ))
    ans=cursor.fetchone()
    if ans==None:
        
        return json.dumps(db.dict_message(False,"Not a staff Member"))
    else:
        print("....... In add donation with staff id..........\n\n")
        result=db.add_order()
        print(result)
        return json.dumps(result)

@app.route('/staff-page', methods=['GET','POST'])
def open_page():
    return render_template("staffordermanagement.html")    

@app.route('/save-order-session',methods=['GET','POST'])
def save_order_ID_session():
    print(".......... Inside Order Data ..........\n\n")
    if not (db.check_column_values('Act',{'userName':session['username'],'roleID': 'staff'})):
        data=db.dict_message(False,"User is not a staff member")
        return json.dumps(data)
    if not (db.check_column_values('Act',{'userName':request.form["clientUsername"],'roleID': 'client'})):
        data=db.dict_message(False,"Entered user is not a client")
        return json.dumps(data)
    
    status,orderID=db.get_orderID()
    session['orderID']=orderID
    session["clientUsername"]=request.form["clientUsername"]
    data=db.dict_message(status,"OrderID Saved")
    print(session['orderID'])
    print(session['clientUsername'])
    return json.dumps(data)    

@app.route('/get-options', methods=['GET','POST'])
def list_of_categories():
    mainCategory,subCategory=db.get_category_options()
    data={
        'mainCategory': mainCategory,
        'subCategory' : subCategory
    }

    print(mainCategory)
    print(subCategory)

    return json.dumps(data)

@app.route('/get-item-list',methods=['GET','POST'])
def get_item_list():
    item_list=db.db_get_item_list()
    return json.dumps(item_list)

@app.route('/add-item-into-order',methods=['GET','POST'])
def add_item_into_order():
    cursor=db.db.cursor(buffered=True)
    if not db.check_column_values('Ordered',{'orderID':session['orderID']}):
        insert_query = """
            INSERT INTO Ordered (orderID, orderDate, supervisor, client)
            VALUES (%s, NOW(), %s, %s)
            """
        cursor.execute(insert_query,(session['orderID'],session['username'],session['clientUsername']))
        db.db.commit()
    
    query="""
        INSERT INTO ItemIn (ItemID,orderID)
        VALUES (%s, %s)
        """
    cursor.execute(query,(request.form['item-list'],session['orderID']))
    return json.dumps(True)

# def get200_resp():
#     return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}'

@app.route('/prepare-order',methods=['GET','POST'])
def prepare_order():
    if not db.check_column_values('Ordered',{'orderID':request.form['orderID']}):
        return json.dumps(db.dict_message(False,'Wrong order ID'))
    db.db_prepare_order()
    return json.dumps(db.dict_message(True,"Order has been prepared"))



if __name__ == '__main__':
    app.run(debug=True)
