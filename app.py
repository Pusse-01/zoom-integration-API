import flask
import json
from flask import jsonify, request
from zoom import ZOOM_CLIENT


app = flask.Flask(__name__)
_zoom = ZOOM_CLIENT()


@app.route("/")
def root():
    response = "<h1>Zoom Integration - POC</h1>"
    
    return response


@app.route('/createMeeting', methods=['POST'])
def create_meeting():
    data = json.loads(request.data)
    start_time = str(data["start_date"])+"T"+str(data["start_time"])
    
    return _zoom.create_meeting(data["topic"], data["agenda"], start_time, data["invitees"])


@app.route('/listMeeting', methods=['GET'])
def list_meeting():
    _meeting = _zoom.list_meetings()
    _response = {
        "topic": _meeting["topic"],
        "start_time": _meeting["start_time"].split("T")[0] + " " + _meeting["start_time"].split("T")[1][:5],
        "join_url": _meeting["join_url"]
    }

    return _response


@app.route('/getMeeting', methods=['GET'])
def get_meeting():
    return jsonify(_zoom.list_meetings()["id"])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
