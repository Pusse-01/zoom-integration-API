import flask
from flask_cors import CORS, cross_origin
import json
from flask import jsonify, request, make_response
from zoom import ZOOM_CLIENT


app = flask.Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

_zoom = ZOOM_CLIENT()


@app.route("/")
@cross_origin()
def root():
    response = make_response("<h1>Zoom Integration - POC</h1>")
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response


@app.route('/createMeeting', methods=['POST'])
@cross_origin()
def create_meeting():
    data = json.loads(request.data)
    data = {
            "topic": "test ",
            "agenda": "test",
            "invitees": "rahalamrith@gmail.com",
            "start_date": "2022-05-11",
            "start_time": "20:44:00"
        }

    start_time = str(data["start_date"])+"T"+str(data["start_time"])
    d = _zoom.create_meeting(data["topic"], data["agenda"], start_time, data["invitees"])
    print(d)
    return d


@app.route('/listMeeting', methods=['GET'])
@cross_origin()
def list_meeting():
    _meeting = _zoom.list_meetings()
    response = make_response({
        "topic": _meeting["topic"],
        "start_time": _meeting["start_time"].split("T")[0] + " " + _meeting["start_time"].split("T")[1][:5],
        "join_url": _meeting["join_url"]
    })
    
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response


@app.route('/getMeeting', methods=['GET'])
@cross_origin()
def get_meeting():
    response = make_response(jsonify(_zoom.list_meetings()["id"]))
    response.headers.add("Access-Control-Allow-Origin", "*")
    
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
