from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for
)

from datetime import datetime, date
import uuid

from config import Config
from models import db, User
from mail import mail, send_birthday_mail
from scheduler import start_scheduler

app = Flask(__name__)
app.config.from_object(Config)

# ==========================================
# INITIALIZE EXTENSIONS
# ==========================================

db.init_app(app)
mail.init_app(app)

# ==========================================
# CREATE DATABASE
# ==========================================

with app.app_context():
    db.create_all()

# ==========================================
# START SCHEDULER
# ==========================================

start_scheduler(app)

# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def home():
    return render_template("index.html")


# ==========================================
# LOGIN PAGE
# ==========================================

@app.route("/login")
def login():
    return render_template("login.html")


# ==========================================
# REGISTER PAGE
# ==========================================

@app.route("/register")
def register():
    return render_template("register.html")


# ==========================================
# EMAIL PAGE
# ==========================================

@app.route("/email")
def email():
    return render_template("email.html")


# ==========================================
# DETAILS PAGE
# ==========================================

@app.route("/details")
def details():

    email = request.args.get("email")

    if not email:
        return redirect(url_for("email"))

    return render_template(
        "details.html",
        email=email
    )


# ==========================================
# SAVE USER
# ==========================================

@app.route("/save", methods=["POST"])
def save():

    name = request.form.get("name")
    email = request.form.get("email")
    dob = request.form.get("dob")

    if not name or not email or not dob:
        return "<h2>Missing Details!</h2>"

    dob = datetime.strptime(
        dob,
        "%Y-%m-%d"
    ).date()

    existing_user = User.query.filter_by(
        email=email
    ).first()
    print("Entered Email:", email)
    print("Found User:", existing_user)
    print("=" * 50)

    if existing_user:

        return """
        <h2 style="
        text-align:center;
        margin-top:100px;
        font-family:Arial;
        color:red;
        ">
        ❌ This Email is Already Registered!
        </h2>
        """

    token = str(uuid.uuid4())

    user = User(
        name=name,
        email=email,
        dob=dob,
        token=token
    )

    db.session.add(user)
    db.session.commit()

    today = date.today()

    birthday = date(
        today.year,
        dob.month,
        dob.day
    )

    if birthday < today:
        birthday = date(
            today.year + 1,
            dob.month,
            dob.day
        )

    days_left = (
        birthday - today
    ).days

    surprise_link = url_for(
        "countdown",
        token=token,
        _external=True
    )

 #try:
#       send_birthday_mail(
#            app=app,
#            receiver_email=email,
#            receiver_name=name,
#            surprise_link=surprise_link,
#            days_left=days_left
#        )
#
 #       print("✅ First Mail Sent Successfully")
#
#    except Exception as e:
#
#       print("❌ Mail Sending Failed")
#       print(e)
#
 #   return redirect(
#        url_for("wait")
#    )


# ==========================================
# WAIT PAGE
# ==========================================

@app.route("/wait")
def wait():
    return render_template("wait.html")


# ==========================================
# COUNTDOWN PAGE
# ==========================================

@app.route("/countdown/<token>")
def countdown(token):

    user = User.query.filter_by(
        token=token
    ).first()

    if not user:
        return "<h2>Invalid Link</h2>"

    today = date.today()

    birthday = date(
        today.year,
        user.dob.month,
        user.dob.day
    )

    if birthday < today:
        birthday = date(
            today.year + 1,
            user.dob.month,
            user.dob.day
        )

    days_left = (
        birthday - today
    ).days

    return render_template(
        "countdown.html",
        name=user.name,
        days_left=days_left,
        token=user.token
    )
# ==========================================
# BIRTHDAY PAGE
# ==========================================

@app.route("/birthday/<token>")
def birthday(token):

    user = User.query.filter_by(
        token=token
    ).first()

    if not user:
        return "<h2>Invalid Link</h2>"

    today = date.today()

    # Allow only on the user's birthday
    if (
        today.month != user.dob.month or
        today.day != user.dob.day
    ):

        return render_template(
            "not_birthday.html",
            name=user.name
        )

    return render_template(
        "birthday.html",
        name=user.name,
        token=user.token
    )


# ==========================================
# FINAL SURPRISE PAGE
# ==========================================

@app.route("/surprise/<token>")
def surprise(token):

    user = User.query.filter_by(
        token=token
    ).first()

    if not user:
        return "<h2>Invalid Link</h2>"

    today = date.today()

    # Surprise page is available only on birthday
    if (
        today.month != user.dob.month or
        today.day != user.dob.day
    ):

        return render_template(
            "not_birthday.html",
            name=user.name
        )

    return render_template(
        "surprise.html",
        name=user.name
    )


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True
    )

