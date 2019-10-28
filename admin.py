from config import *
from validators import *


@app.route("/register", methods=['GET','POST'])
def register():
    form = User(request.form)
    if request.method == "POST" and form.validate(): 
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(str(form.password.data))

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(username, email, password)VALUES (%s, %s, %s)",(username,email,password))
        mysql.connection.commit()
        cur.close
        flash("Registration complete login","success")
        redirect(url_for("login"))
    return render_template("admin/register.html",form = form)


@app.route("/login", methods=["GET","POST"])
def login():
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
                session['logged_in'] = True
                session['username'] = username
                session['id'] = id
                flash("You are currently logged in","success")
                return redirect(url_for('dashboard'))
            else:
                error = "Invalid login credentials"
                return render_template("admin/login.html", error = error)
        else:
            error = "User not found"
            return render_template("admin/login.html",error = error)
    return render_template("admin/login.html")

def is_logged_in(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            flash("Unauthorized access please login","danger")
            return redirect(url_for('login'))
    return wrap

@app.route("/logout")
def logout():
    session.clear()
    flash("You are currently logged out","success")
    return redirect(url_for('login'))

@app.route('/dashboard', methods=['GET','POST'])
#@is_logged_in
def dashboard():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from question")
    result = cur.fetchall()
    return render_template('admin/dashboard.html', questions = result)

@app.route('/python', methods=['GET','POST'])
def python():
    category = "python"
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from questions WHERE category=%s",[category])
    result = cur.fetchall()
    return render_template('admin/dashboard_python.html', questions = result)

@app.route('/php', methods=['GET','POST'])
def php():
    category = "php"
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from questions WHERE category=%s",[category])
    result = cur.fetchall()
    return render_template('admin/dashboard_php.html', questions = result)

@app.route('/javascript', methods=['GET','POST'])
def javascript():
    category = "javascript"
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from questions WHERE category=%s",[category])
    result = cur.fetchall()
    return render_template('admin/dashboard_javascript.html', questions = result)


@app.route('/add', methods=['GET','POST'])
def add():
    form = Add(request.form)
    if request.method == 'POST' and form.validate():
        number = request.form['number']
        question = request.form['question']
        correct = request.form['correct']
        cur = mysql.connection.cursor()
        cur.execute("INSERT into question(id, question) VALUES(%s, %s)",(number,question))
        mysql.connection.commit()
        cur.close()

        # Creating a list of options
        options = []
        options.append(request.form['option_a'])
        options.append(request.form['option_b'])
        options.append(request.form['option_c'])
        options.append(request.form['option_d'])

        for option in options:
            if  option == correct:
                is_correct = 1
            else:
                is_correct =0
            cur = mysql.connection.cursor()
            cur.execute("INSERT into choices(question_number, is_correct,choice) VALUES(%s, %s,%s)",(number,is_correct,option))
            mysql.connection.commit()
            cur.close()
        flash("Question Added successfully","success")
        #return redirect(url_for("dashboard"))
    return render_template('admin/add.html', form=form)


@app.route("/update/<string:id>", methods=['GET','POST'])
def update(id):
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT *  questions WHERE id=%s",[id])
    question = cur.fetchone()
    form = Add(request.form)
    form.question.data = question['question']
    form.category.data = question['category']
    form.option_a.data = question['a']
    form.option_b.data = question['b']
    form.option_c.data = question['c']
    form.option_d.data = question['d']
    form.author.data = question['author']

    if request.method == 'POST' and form.validate():
        question_num = request.form['question_num']
        question = request.form['question']
        # Creating a list of options
        options = []
        optilt = cur.execute("SELECT *  questions WHERE id=%s",[id])
    question = cur.fetchone()on[0] = request.form['option_a']
        option[1] = request.form['option_b']
        option_[2] = request.form['option_c']
        option[3] = request.form['option_d']
        author = "admin"
        cur.execute("UPDATE questions SET question=%s, category =%s, option_a = %s, option_b = %s, option_c = %s, option_d = %s WHERE id = %s",(question,category,option_a, option_b, option_c,option_d, author))
        mysql.connection.commit()
        cur.close()
        flash("Update Successfull","success")
        return redirect(url_for("dashboard"))
    return render_template("admin/update.html",form=form)


@app.route("/delete/<string:id>/",methods=['POST'])
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM question WHERE id=%s",[id])
    mysql.connection.commit()
    cur.close()
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM choices WHERE  question_number=%s",[id])
    mysql.connection.commit()
    cur.close()
    flash("Deleted","danger")
    return redirect(url_for('dashboard'))


if  __name__ == "__main__":
    app.run(debug=True)
