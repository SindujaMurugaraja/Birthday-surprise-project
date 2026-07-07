from apscheduler.schedulers.background import BackgroundScheduler
from datetime import date

from models import db, User
from mail import send_birthday_mail

scheduler = BackgroundScheduler()


def daily_mail_job(app):

    with app.app_context():

        users = User.query.all()

        today = date.today()

        for user in users:

            # Birthday date
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

            days_left = (birthday - today).days

            # Skip if already sent today
            if user.last_mail_sent == today:
                continue

            # Default countdown page
            surprise_link = (
    f"https://birthday-surprise-project.onrender.com/countdown/{user.token}"
)
            

            # Birthday day → Birthday page
            if days_left == 0:
                surprise_link = (
    f"https://birthday-surprise-project.onrender.com/birthday/{user.token}"
)

            try:

                send_birthday_mail(
                    app=app,
                    receiver_email=user.email,
                    receiver_name=user.name,
                    surprise_link=surprise_link,
                    days_left=days_left
                )

                user.last_mail_sent = today

                print(f"✅ Daily Mail Sent -> {user.email}")

            except Exception as e:

                print(f"❌ Failed -> {user.email}")
                print(e)

        db.session.commit()


def start_scheduler(app):

    scheduler.add_job(
        func=lambda: daily_mail_job(app),
        trigger="interval",
        days=1,
        id="daily_birthday_mail",
        replace_existing=True
    )

    scheduler.start()

    print("✅ Daily Mail Scheduler Started")