import parser

from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import psycopg2
import json


def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database="flask_web_app_db",
                            user="yc",
                            password="labris",
                            port="5432")
    return conn


app = Flask(__name__)
api = Api(app)

init = {'Intern task': 'Flask-web-app-project',
        }
fake_db = {
    1: {
        "username": "yc",
        "firstname": "yigit",
        "middlename": "null",
        "lastname": "cevik",
        "birthdate": "1.1.1",
        "email": "asdffggf@",
        "password": "aadsyrw"},
    2: {
        "username": "od99",
        "firstname": "onur",
        "middlename": "gocuman",
        "lastname": "deniz",
        "birthdate": "2.2.2",
        "email": "fashdosd@",
        "password": "fkldkreks"
    },
    3: {
        "username": "dfame",
        "firstname": "dogukan",
        "middlename": "dodo",
        "lastname": "unlu",
        "birthdate": "3.3.3",
        "email": "kirieibre@irbf",
        "password": "iffflslri"
    }
}


class ProjectStart(Resource):
    def get(self):
        # Default to 200 OK
        return init


class Login(Resource):
    def get(self):
        return {'login': 'world'}


class Logout(Resource):
    def get(self):
        return {'logout': 'world'}


class UserList(Resource):
    def get(self):
        return {'userList': 'world'}


class UserCreate(Resource):
    def get(self):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''select * from users;''')
        users = cur.fetchall()
        return jsonify(users)

    def post(self):
        conn = get_db_connection()
        cur = conn.cursor()
        if json.loads(request.data) is not None:
            data = json.loads(request.data)
            print(data)
            username = data['username']
            firstname = data['firstname']
            middlename = data['middlename']
            lastname = data['lastname']
            birthdate = data['birthdate']
            email = data['email']
            password = data['password']
        else:
            return 'id must be defined', 400

        addQuery = '''insert into users 
        (username,firstname,middlename,lastname,birthdate,email,password)
        values (%s,%s,%s,%s,%s,%s,%s)'''

        cur.execute(addQuery, (username, firstname, middlename, lastname, birthdate, email, password))
        conn.commit()


class Delete(Resource):
    def get(self):
        return {'hello': 'world'}


class Update(Resource):
    def get(self):
        return {'hello': 'world'}


class OnlineUsers(Resource):
    def get(self):
        return {
            "username": "",
            "ipaddress": "",
            "logindatetime": ""
        }

    def post(self):
        pass


api.add_resource(ProjectStart, '/')

api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(UserList, '/user/list')
api.add_resource(UserCreate, '/user/create')
api.add_resource(Delete, '/delete/<string:id>')
api.add_resource(Update, '/update/<string:id>')
api.add_resource(OnlineUsers, '/onlineusers')

if __name__ == '__main__':
    app.run(debug=True)
