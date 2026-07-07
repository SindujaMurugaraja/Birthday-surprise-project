from flask_mail import Mail, Message
from flask import current_app
from quotes import get_random_quote

mail = Mail()


def send_birthday_mail(
    app,
    receiver_email,
    receiver_name,
    surprise_link,
    days_left
):

    quote = get_random_quote()

    # Subject based on birthday
    if days_left == 0:
        subject = f"🎉 Happy Birthday {receiver_name}! 🎂"
        heading = "🎂 Happy Birthday 🎂"
        days_text = "🎉 Today is Your Special Day! 🎉"
        button_text = "🎁 Open Your Birthday Surprise"
    else:
        subject = f"{quote['subject']} 💖"
        heading = "Advance Happy Birthday 🎂"
        days_text = f"🎉 Only {days_left} Days Left 🎉"
        button_text = "🎁 Open Your Surprise"

    html = f"""
<!DOCTYPE html>
<html>

<head>

<meta charset="UTF-8">

<style>

*{{
margin:0;
padding:0;
box-sizing:border-box;
}}

body{{
background:#fff3fa;
font-family:Verdana,sans-serif;
}}

.wrapper{{
width:100%;
padding:50px 0;
background:
linear-gradient(
180deg,
#ffd8ec,
#fff4fb,
#ffffff
);
}}

.card{{
width:720px;
margin:auto;
background:white;
border-radius:30px;
overflow:hidden;
box-shadow:
0 0 40px rgba(255,105,180,.35);
}}

.header{{
padding:45px;
text-align:center;
background:
linear-gradient(
90deg,
#ff4fa3,
#ff84c3,
#ffc8e5
);
}}

.header h1{{
color:white;
font-size:42px;
}}

.header p{{
margin-top:15px;
font-size:22px;
color:white;
}}

.content{{
padding:50px;
text-align:center;
}}

.title{{
font-size:42px;
font-weight:bold;
color:#ff2d92;
}}

.name{{
font-size:55px;
font-weight:bold;
color:#ff1493;
margin-top:20px;
margin-bottom:20px;
}}

.days{{
font-size:34px;
font-weight:bold;
color:#7d009d;
margin-bottom:30px;
}}

.quote{{
font-size:21px;
line-height:40px;
color:#555;
padding:20px;
}}

.button{{
display:inline-block;
margin-top:40px;
padding:18px 45px;
background:#ff3d92;
color:white;
text-decoration:none;
font-size:22px;
font-weight:bold;
border-radius:50px;
}}

.footer{{
padding:35px;
background:#fff6fb;
text-align:center;
font-size:18px;
color:#666;
line-height:34px;
}}

</style>

</head>

<body>

<div class="wrapper">

<div class="card">

<div class="header">

<h1>
💖 Hello {receiver_name}
</h1>

<p>
Your Birthday Journey Begins ✨
</p>

</div>

<div class="content">

<div class="title">

{heading}

</div>

<div class="name">

{receiver_name} ❤️

</div>

<div class="days">

{days_text}

</div>

<div class="quote">

{quote["message"].replace(chr(10), "<br>")}

</div>

<a
class="button"
href="{surprise_link}"
>
{button_text}
</a>
</div>

<div class="footer">

🌸 Every new sunrise brings your birthday one step closer.<br><br>

Stay Happy ❤️ Stay Blessed ❤️ Keep Smiling.

</div>

</div>

</div>

</body>

</html>
"""

    msg = Message(
        subject=subject,
        sender=current_app.config["MAIL_DEFAULT_SENDER"],
        recipients=[receiver_email]
    )

    msg.html = html

    try:

        with app.app_context():

            print("=" * 60)
            print("📧 Sending Mail...")
            print(f"👤 Name : {receiver_name}")
            print(f"📩 Email : {receiver_email}")
            print(f"📅 Days Left : {days_left}")

            mail.send(msg)

            print("✅ Mail Sent Successfully")
            print("=" * 60)

    except Exception as e:

        print("=" * 60)
        print("❌ MAIL SENDING FAILED")
        print(e)
        print("=" * 60)
        