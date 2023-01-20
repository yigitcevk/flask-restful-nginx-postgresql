
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import psycopg2
import json
import hashlib
from datetime import datetime
import re
import uuid

pattern_password = re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$")
pattern_email = re.compile("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+$")


def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database="flaskapp_db",
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
    def post(self):
        conn = get_db_connection()
        cur = conn.cursor()
        if json.loads(request.data) is not None:
            data = json.loads(request.data)
            print(data)
            username = data['username']
            ipaddress = request.remote_addr
            logindatetime = datetime.now()
            password = data['password']
        else:
            return 'id must be defined', 400

        cur.execute('''select password from users where username=%s;''', (username,))

        fetch = (cur.fetchall())
        real_password = json.dumps(fetch)
        real_password = real_password[2:len(real_password) - 2]
        print(real_password)

        hashedText, salt = real_password.split(':')

        print(hashlib.sha256(salt.encode() + password.encode()).hexdigest())
        if hashedText == hashlib.sha256(salt.encode() + password.encode()).hexdigest():
            addQuery = '''insert into onlineusers 
            (username,ipaddress,logindatetime,)
            values (%s,%s,%s)'''
            cur.execute(addQuery, (username, ipaddress, logindatetime))
        else:
            return 'password is wrong', 400

        conn.commit()
        cur.close()
        conn.close()


class Logout(Resource):
    def delete(self):
        conn = get_db_connection()
        cur = conn.cursor()
        if json.loads(request.data) is not None:
            data = json.loads(request.data)
            print(data)
            usernametemp = data['username']
        else:
            return 'id must be defined', 400

        cur.execute('''delete from onlineusers where username=%s''', (usernametemp,))
        conn.commit()
        cur.close()
        conn.close()


class UserList(Resource):
    def get(self):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''select * from users;''')
        users = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(users)


class UserCreate(Resource):
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

        if pattern_email.match(email) and pattern_password.match(password):
            salt = uuid.uuid4().hex
            hashed_password = hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt
            addQuery = '''insert into users 
            (username,firstname,middlename,lastname,birthdate,email,password,)
            values (%s,%s,%s,%s,%s,%s,%s)'''
        else:
            return 'password or email not satisfy', 400

        cur.execute(addQuery, (username, firstname, middlename, lastname, birthdate, email, hashed_password))
        conn.commit()
        cur.close()
        conn.close()


class Delete(Resource):
    def delete(self):
        conn = get_db_connection()
        cur = conn.cursor()
        if json.loads(request.data) is not None:
            data = json.loads(request.data)
            print(data)
            usernametemp = data['username']
        else:
            return 'id must be defined', 400

        cur.execute('''delete from users where username LIKE username''', (usernametemp,))
        conn.commit()
        cur.close()
        conn.close()


class Update(Resource):
    def put(self, id):
        print(id)

        conn = get_db_connection()
        cur = conn.cursor()

        if json.loads(request.data) is not None:
            data = json.loads(request.data)
            print(data)
            username = data['username']
            firstname = data['firstname']
            middlename = data['middlename']
            print(middlename)
            lastname = data['lastname']
            birthdate = data['birthdate']
            email = data['email']
            password = data['password']
        else:
            return 'id must be defined', 400

        if pattern_email.match(email) and pattern_password.match(password):
            updateQuery = '''update users set firstname=%s, middlename=%s, lastname=%s, birthdate=%s, email=%s, password=%s where username=%s'''
            cur.execute(updateQuery, (firstname, middlename, lastname, birthdate, email, password, id,))
        else:
            return 'password or email not satisfy', 400

        conn.commit()
        cur.close()
        conn.close()


class OnlineUsers(Resource):
    def get(self):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''select * from onlineusers;''')
        onlineusers = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(onlineusers)


class GetLogs(Resource):
    def get(self):
        try:
            logs = ""
            with open('/var/log/nginx/access.log', "r") as file:
                logs += file.read()

            return jsonify({'Logs': logs})
        except:
            return jsonify({'message': 'problem occurred'})


api.add_resource(ProjectStart, '/')

api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(UserList, '/user/list')
api.add_resource(UserCreate, '/user/create')
api.add_resource(Delete, '/user/delete/<string:id>')
api.add_resource(Update, '/user/update/<string:id>')
api.add_resource(OnlineUsers, '/onlineusers')
api.add_resource(GetLogs, '/logs')


if __name__ == '__main__':
    app.run(debug=True)
