from config import *
from validators import *

@app.route("/")
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from questions")
    result = cur.fetchall()
    return render_template("index.html", questions = result)



@app.route("/register_user", methods=['GET','POST'])
def register_user():
    form = User(request.form)
    if request.method == "POST" and form.validate(): 
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(str(form.password.data))
        stack = form.stack.data

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(username, email, password, stack)VALUES (%s, %s, %s, %s)",(username,email,password,stack))
        mysql.connection.commit()
        cur.close
        flash("Registration complete login","success")
        redirect(url_for("login_user"))
    return render_template("register_user.html",form = form)



@app.route("/login_user", methods=["GET","POST"])
def login_user():
    if request.method =="POST":
        username = request.form['username']
        password_candidate = request.form['password']
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM users WHERE username=%s",[username])
        if result > 0:
            data = cur.fetchone()
            password = data["password"]
            id = data["id"]
            if sha256_crypt.verify(password_candidate,password):
                session['logged_user'] = True
                session['username'] = username
                session['id'] = id
                flash("You are currently logged in","success")
                return redirect(url_for('welcome'))
            else:
                error = "Invalid login credentials"
                return render_template("login_user.html", error = error)
        else:
            error = "User not found"
            return render_template("login_user.html",error = error)
    return render_template("login_user.html")

@app.route("/welcome")
def welcome():
    return render_template("welcome.html")

@app.route("/quiz", methods=['GET','POST'])
def quiz():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from questions")
    result = cur.fetchall()

    if request.method == "POST":
        selected = request.form['a']
        #print(selected)
        return render_template("quiz.html", select=selected)            
    return render_template("quiz.html", questions=result)