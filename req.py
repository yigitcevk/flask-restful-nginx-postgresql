import requests
import json

endpoint = "http://127.0.0.1:5000/"
create_user = "user/create"
onlineusers = "onlineusers"


myData = {
            "username": "yc",
            "firstname": "yigit",
            "middlename": "null",
            "lastname": "cevik",
            "birthdate": "1.1.1",
            "email": "asdffggf@",
            "password": "aadsyrw"}

r = requests.post(endpoint+create_user, data=json.dumps(myData))
r.status_code