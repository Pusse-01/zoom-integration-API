import jwt
from time import time
import json
import requests
from datetime import datetime

class ZOOM_CLIENT():

    def __init__(self) -> None:
        self.API_KEY = 'yoLTrtJESImvz06ruIbV4g'
        self.API_SECRET = 'k6VuQUeP3ylVxqJ99NfbLJjLqhJUtqiVBo9Y'
        self.BASE_URL = 'https://api.zoom.us/v2/'
        self.headers = {
            'authorization': 'Bearer ' + self.__generate_token(),
            'content-type': 'application/json'
        }

    def __generate_token(self):
        token = jwt.encode(
            # API Key & expiration time
            {'iss': self.API_KEY, 'exp': time() + 5000},
            # Secret used to generate token signature
            self.API_SECRET,
            # Specify the hashing alg
            algorithm = 'HS256'
        )
        return token

    def create_meeting(self, topic, agenda, start_time, invitees):
        _invitees, _emails = [], invitees.split(";")
        for _email in _emails:
            _invitees.append({
                "email": _email
            })

        payload =  {
            "agenda": agenda,
            "duration": 30,
            "password": "123456",
            "settings": {
                "approval_type": 2,
                "audio": "both",
                "auto_recording": "cloud",
                "calendar_type": 2,
                "contact_email": "dinesh@sp-solutiobs.biz",
                "contact_name": "Dinesh Wijesingha",
                "email_notification": True,
                "focus_mode": True,
                "host_video": False,
                "jbh_time": 5,
                "join_before_host": False,
                "meeting_authentication": False,
                "meeting_invitees": _invitees,
                "mute_upon_entry": True,
                "participant_video": True,
            },
            "start_time":  start_time,
            "timezone": "Asia/Colombo",
            "topic": topic,
            "type": 2
        }
        _meeting = json.loads(requests.post(self.BASE_URL + 'users/me/meetings'
            , headers=self.headers, data=json.dumps(payload)
        ).text)
        
        return {
            "id": _meeting["id"],
            "topic": _meeting["topic"],
            "start_time": _meeting["start_time"].split("T")[0] + " " + _meeting["start_time"].split("T")[1][:5],
            "join_url": _meeting["join_url"]
        }

    def list_meetings(self):
        meetings = requests.get(self.BASE_URL + 'users/me/meetings', headers=self.headers)
        meetings = json.loads(meetings.text)['meetings']

        return meetings[0]
