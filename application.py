from config import *
from validators import *

@app.route("/")
def index():
    #cur = mysql.connection.cursor()
    #cur.execute("SELECT * from questions")
    #result = cur.fetchall()
    return render_template("index.html")



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

def is_logged_in_user(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if 'logged_user' in session:
            return f(*args,**kwargs)
        else:
            flash("Unauthorized access please login","danger")
            return redirect(url_for('login_user'))
    return wrap

@app.route("/logout_user")
def logout_user():
    session.clear()
    flash("You are currently logged out","success")
    return redirect(url_for('login_user'))

@app.route("/welcome")
@is_logged_in_user
def welcome():
    return render_template("welcome.html")

@app.route("/quiz", methods=['GET','POST'])
@is_logged_in_user
def quiz():
    number =1
    cur = mysql.connection.cursor() 
    cur.execute("SELECT * from question WHERE id=%s",[number])
    result = cur.fetchone()
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from choices WHERE question_number=%s",[number])
    choice = cur.fetchall()

    if request.method == "POST":
        choice = int(request.form['choice'])
        number = int(request.form['number'])+1
        is_correct = 1
        #session['score'] = 0
        cur = mysql.connection.cursor()
        cur.execute("SELECT * from choices WHERE is_correct=%s",[is_correct])
        correct = cur.fetchone()
        correct_choice = int(correct['id'])
        if choice == correct_choice:
            flash("Correct Choice","success")   
            session['score']=+1
        if number > 2:# Total number of questions in database *Make it dynamic later
            return redirect(url_for("result"))
        cur = mysql.connection.cursor() 
        cur.execute("SELECT * from question WHERE id=%s",[number])
        result = cur.fetchone()
        cur = mysql.connection.cursor()
        cur.execute("SELECT * from choices WHERE question_number=%s",[number])
        choice = cur.fetchall()
    return render_template("quiz.html", number=number, choices = choice, questions=result)


@app.route("/result")
@is_logged_in_user
def result():
    return render_template("result.html")
