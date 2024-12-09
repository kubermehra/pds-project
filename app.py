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


def check_liked_lables():
    try:
        if request.method == 'POST':
            email = session.get('email')
            fields = 'liked_labels'
            user = {
                'email': email,
                fields: {"$exists": True}
            }
            user_data = users.find_one(user)
            
            if user_data is None:
                recommended_list = trending_videos.find({}, {'video_id': 1})
                counts = 0
                for vid in recommended_list:
                    counts = counts + 1
                
                print("COUNT: ", counts)
                if counts < 1:
                    recommended_list = videos.aggregate([
                        {"$group": {
                            "_id": "$video_id",
                            "total_views": {"$sum": "$view_count"}
                        }},
                        {"$sort": {"total_views": -1}},
                        {"$limit": 20}
                    ])
                    vid_list = [doc["_id"] for doc in recommended_list]
                else:
                    recommended_list = trending_videos.find({}, {'video_id': 1})
                    vid_list = [doc["video_id"] for doc in recommended_list]
                # recommended_list = trending_videos.find({}, {'video_id': 1})
                recommended_list = videos.aggregate([
                    {"$sortByCount": "$video_id"},
                    {"$sort": {"count": -1}},
                    {"$limit": 20}
                ])
                vid_list = [doc["_id"] for doc in recommended_list]
                
                # vid_list = [doc["video_id"] for doc in recommended_list]
                # Fetch video names from the MongoDB videos collection
                video_names = []
                for vid_id in vid_list:
                    video_doc = videos.find_one({"video_id": vid_id})
                    if video_doc:
                        video_names.append(video_doc["title"])
                    else:
                        video_names.append("Unknown")  # Handle if video not found in the database
                
                # Construct the response data
                data = {
                    'status': False,
                    'vid_list': vid_list,
                    'vid_name': video_names
                }
                return data
            else:
                pass
    
    except Exception as e:
        print(e)


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template("signup.html")


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    
    status, email, username = db.check_user()
    
    data = {
        "username": username,
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
    print(status)
    data={
        'status': status,
        'locations': location_data
    }
    return json.dumps(data)


# @app.route('/generate_list', methods=['GET', 'POST'])
# def get_recommendation():
#     data = check_liked_lables()
#     print("DATA:", data)
#     return json.dumps(data)
#     # return render_template('content.html', data=data)


# @app.route('/play_video/<videoId>')
# def play_video(videoId):
#     # length_seconds = get_video_length(videoId)
#     # print("LENGTH:",length_seconds)
#     famous_segment = None
#     # Query the most_watched_segment collection to get the famous segment for the given videoId
#     result = most_watched_segment.find_one({"video_id": videoId})
#     if result:
#         famous_segment = result.get("famous_segment")
#     return render_template('play_video.html', videoId=videoId, famous_segment=famous_segment)


# # Route to handle liking or disliking a video
# @app.route('/like_video/<video_id>', methods=['POST'])
# def like_video(video_id):
#     action = request.json.get('action')
#     user_email = session.get('email')
    
#     # Check if user exists
#     user_exists = users.find_one({'email': user_email})
#     print("ACTION:", action)
#     print("email:", user_email)
#     if not user_exists:
#         print(3)
#         return jsonify({'error': 'User not found'})
    
#     if action == 'like':
#         print("ADDING")
#         # Update user's liked videos array with video_id
#         users.update_one({'email': user_email}, {'$addToSet': {'liked_videos': video_id}})
#         return jsonify({'message': 'Video liked'})
#     elif action == 'dislike':
#         # Update user's disliked videos array with video_id
#         users.update_one({'email': user_email}, {'$addToSet': {'disliked_videos': video_id}})
#         return jsonify({'message': 'Video disliked'})
#     else:
#         return jsonify({'error': 'Invalid action'})


# # ------------------------------------------------------------
# #  Updating current time
# # ------------------------------------------------------------


# @app.route('/update_time', methods=['POST'])
# def update_time():
#     VID_SKIP_TIME_TOPIC = 'VID_SKIP_TIME_TOPIC'
    
#     user_email = session.get('email')
#     data = request.get_json()
#     video_id = data['video_id']
#     current_time = data['current_time']
#     total_time = data['total_time']
    
#     interval_value = total_time / 10
#     interval_number = current_time // interval_value
    
#     if current_time == total_time:
#         interval_number = 9
    
#     low_time = interval_number * interval_value
#     high_time = low_time + interval_value
    
#     curTime = datetime.datetime.now()
    
#     if user_email and video_id:
#         push_data = {'timestamp': str(curTime), 'video_id': video_id, 'email': user_email, 'current_time': current_time,
#                      'low_time': low_time, 'high_time': high_time}
#         print('Sending {} to Kafka'.format(push_data))
#         future = kafkaProducer.send(VID_SKIP_TIME_TOPIC, value=push_data)
        
#         r_meta = None
#         try:
#             r_meta = future.get(timeout=10)
#         except KafkaError as e:
#             print('Kafka error when pushing to topic {}: {}'.format(VID_SKIP_TIME_TOPIC, e))
#     else:
#         print('No user or video data')
#     return get200_resp()
    
#     # Increment the collection in MongoDB for the given video ID and current time frame
#     # Implement your MongoDB logic here
    
#     return jsonify({'message': 'Current time updated successfully'})


# # Set up the YouTube Data API client
# # youtube_api_key = 'AIzaSyDlUdNx5_dApzybPBoZhh1HATk-WNP1j5Y'
# # youtube = build('youtube', 'v3', developerKey=youtube_api_key)

# # def get_video_length(video_id):
# #     # Call the YouTube Data API to retrieve video details
# #     request = youtube.videos().list(
# #         part='contentDetails',
# #         id=video_id
# #     )
# #     response = request.execute()
# #     # Extract the duration from the response
# #     duration_str = response['items'][0]['contentDetails']['duration']
# #     # Parse the ISO 8601 duration format to get the length in seconds
# #     duration = isodate.parse_duration(duration_str)
# #     length_seconds = duration.total_seconds()
# #     return length_seconds


# # ------------------------------------------------------------
# # Analytics APIs
# # ------------------------------------------------------------

# @app.route('/ana/mark_opened', methods=['POST'])
# def mark_opened():
#     VID_OPEN_TOPIC = 'VID_OPEN_TOPIC'
#     user_email = session.get('email')
#     req_data = request.get_json()
#     video_id = req_data['video_id']
#     curTime = datetime.datetime.now()
#     users.update_one({'email': user_email},
#                      {'$addToSet': {'watched_history': {'current_time': curTime, 'video_id': video_id}}})
    
#     if user_email and video_id:
#         push_data = {'timestamp': str(curTime), 'video_id': video_id, 'email': user_email}
#         print('Sending {} to Kafka'.format(push_data))
#         future = kafkaProducer.send(VID_OPEN_TOPIC, value=push_data)
        
#         r_meta = None
#         try:
#             r_meta = future.get(timeout=10)
#         except KafkaError as e:
#             print('Kafka error when pushing to topic {}: {}'.format(VID_OPEN_TOPIC, e))
    
#     return get200_resp()


# def get200_resp():
#     return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


if __name__ == '__main__':
    app.run(debug=True)
