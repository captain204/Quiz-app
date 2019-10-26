from flask import(Flask,render_template,redirect,request,flash,url_for,session,logging)
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
from wtforms import Form, StringField, TextAreaField,PasswordField,SelectField, validators
from functools import wraps

app = Flask(__name__)

mysql = MySQL(app)

app.config['SECRET_KEY'] = 'fjfjkfkjssmdjdjdmdm'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'quiz'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
