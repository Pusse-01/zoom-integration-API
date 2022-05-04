import flask
import jwt
import requests
from zoomus import ZoomClient
import json
from flask import jsonify, request
from time import time

app = flask.Flask(__name__)
app.config["DEBUG"] = True


# Enter your API key and your API secret
API_KEY = 'pnnUcpQSS4-aV1pPrFi9Ng'
API_SEC = 'hnZYNbmowkIs039SJE3MKx6umc4p29YxbA6H'

# connect to Zoom Client
client = ZoomClient(API_KEY, API_SEC)


def generateToken(API_KEY, API_SEC):
    token = jwt.encode(

        # Create a payload of the token containing
        # API Key & expiration time
        {'iss': API_KEY, 'exp': time() + 5000},

        # Secret used to generate token signature
        API_SEC,

        # Specify the hashing alg
        algorithm='HS256'
    )
    return token


def createMeeting(meetingdetails, API_KEY, API_SEC):
    headers = {'authorization': 'Bearer ' + generateToken(API_KEY, API_SEC),
               'content-type': 'application/json'}
    r = requests.post(
        f'https://api.zoom.us/v2/users/me/meetings',
        headers=headers, data=json.dumps(meetingdetails))

    print("\n creating zoom meeting ... \n")
    # print(r.text)
    # converting the output into json and extracting the details

    return r


def get_meetings(client):
    # Find if Meeting got created
    user_list = json.loads(client.user.list().content)
    for user in user_list['users']:
        user_id = user['id']
        meetings = client.meeting.list(user_id=user_id).content
        return (json.loads(meetings))


@app.route("/")
def home_view():
    return "<h1>Zoom Integration - POC</h1>"


@app.route('/createmeeting', methods=['POST'])
def new_meetings():
    data = json.loads(request.data)
    time = str(data["start_date"])+"T"+str(data["start_time"])
    meetingdetails = {
        "topic": data["topic"],
        "type": 2,
        "start_time": time,
        "duration": "40",
        "timezone": "",
        "agenda": data["agenda"],
        "password": "123456",
        "pre_schedule": False,
        "recurrence": {
            "type": 1,
            "repeat_interval": 1
        },
        "settings": {
            "host_video": "true",
            "participant_video": "true",
            "join_before_host": "False",
            "mute_upon_entry": "False",
            "watermark": "true",
            "audio": "voip",
            "auto_recording": "cloud"
        }
    }
    r = createMeeting(
        meetingdetails, API_KEY, API_SEC)
    print(data["topic"])
    y = json.loads(r.text)
    # join_URL = y["join_url"]
    # meetingPassword = y["password"]
    # res = {join_URL, meetingPassword}
    return jsonify(y)


@app.route('/get_meetings', methods=['GET'])
def getMeetings():
    meetings = get_meetings(client)
    print(meetings['meetings'][0]['id'])
    return jsonify(meetings['meetings'][0]['id'])


app.run()
