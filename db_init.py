import psycopg2
import os

conn = psycopg2.connect(database="flask_web_app_db", user="yc", password="labris", host="127.0.0.1", port="5432")
cur = conn.cursor()

cur.execute('''create table if not EXISTS users (
    username varchar(30) DEFAULT NULL,
    firstname varchar(30) DEFAULT NULL,
    middlename varchar(30) DEFAULT NULL,
    lastname varchar(30) DEFAULT NULL,
    birthdate varchar(30) DEFAULT NULL,
    email varchar(30) DEFAULT NULL,
    password varchar(256) DEFAULT NULL,

    PRIMARY KEY (username)
);''')

cur.execute('''create table if not EXISTS onlineusers (
    username varchar(30) DEFAULT NULL,
    ipaddress varchar(30) DEFAULT NULL,
    logindatetime varchar(30) DEFAULT NULL,

    PRIMARY KEY (ipaddress),
    constraint FK_username
        foreign key(username)
            references users(username)
);''')

cur.execute('''
            INSERT INTO users VALUES ('yc', 'yigit', 'null', 'cevik', '1.1.1', 'asdffggf@', 'aadsyrw');
            INSERT INTO users VALUES ('od99', 'onur', 'gocuman', 'deniz', '2.2.2','fashdosd@', 'fkldkreks');
            INSERT INTO users VALUES ('dfame', 'dogukan', 'dodo', 'unlu', '3.3.3', 'kirieibre@irbf', 'iffflslri');
            ''')

conn.commit()
conn.close()
