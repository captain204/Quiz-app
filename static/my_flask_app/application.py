from flask import Flask, redirect, render_template, request 
from flask_mysqldb import MySQL
app = Flask(__name__)
fellows = []
@app.route("/")
def index():
    name=request.args.get("name","Earth")
    return render_template("index.html", name=name)


@app.route("/registrants")
def registerdFellows():
    return render_template("registered.html",fellows=fellows)

@app.route("/register", methods=["GET"])
def registrationform():
    return render_template('register.html')



@app.route("/register", methods=["POST"])

def register():
    name = request.form.get("name")
    state = request.form.get("state")

    if not name or not state:
        return render_template("failiure.html")
    fellows.append(f"{name} Your are from {state} Nigeria")
    return redirect("/registrants")


@app.route("/about")
def about():
    return render_template("about.html")



@app.route("/contact")
def contact():
    return render_template("contact.html")