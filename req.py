import requests
import json

endpoint = "http://127.0.0.1:5000/"
create_user = "user/create"
onlineusers = "login"
logout = "logout"
update = "user/update/"

user_data = {
            "username": "yc",
            "firstname": "yigit",
            "middlename": "null",
            "lastname": "cevik",
            "birthdate": "1.1.1",
            "email": "asdffggf@",
            "password": "aadsyrw"}

onlineusers_data = {
            "username": "yc",
            "ipaddress": "192.168.0.183",
            "logindatetime": "null"
}

update_path = "yc"
update_data = {
            "username": "yc",
            "firstname": "yigit",
            "middlename": "babafingo",
            "lastname": "cevik",
            "birthdate": "1.1.1",
            "email": "asdffggf@",
            "password": "aadsyrw"}


#r = requests.post(endpoint+create_user, data=json.dumps(user_data))
#r = requests.post(endpoint+onlineusers, data=json.dumps(onlineusers_data))
r = requests.put(endpoint+update+update_path, data=json.dumps(update_data))
#r = requests.delete(endpoint+logout, data=json.dumps(onlineusers_data))

r.status_code