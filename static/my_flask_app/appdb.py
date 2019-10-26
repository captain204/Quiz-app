from flask import Flask, redirect, render_template, request 
from flask_mysqldb import MySQL

app = Flask(__name__)
mysql = MySQL(app)


#Configure mysql database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskdb'
mysql = MySQL(app)
@app.route("/register", methods=['GET','POST'])
def register():
    if request.method == "POST":
        fellows = request.form
        eName = fellows['name']
        email = fellows['email']
        eState = fellows['state']
        
        if not eName or not eState:
            return render_template('failiure.html')
        cur = mysql.connection.cursor()
        cur.execute("INSERT into fellows(name, email, state_origin)VALUES(%s,%s,%s)", (eName,email,eState))
        mysql.connection.commit()
        cur.close()
        return redirect('/registerants')
    if request.method == "GET":
        return render_template("register.html")

    
@app.route("/registrants")
def registerdFellows():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM fellows")
    data = cur.fetchall()
    return render_template("registered.html",fellows=data)


    