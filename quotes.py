import random


quotes = [

    {
        "subject": "Your Special Day is Coming",
        "message": """🌸 Every birthday is a fresh beginning.

Keep smiling.
Keep dreaming.
Beautiful memories are waiting for you.

Something magical is on the way... ✨"""
    },

    {
        "subject": "A Beautiful Surprise Awaits",
        "message": """💖 Happiness grows when it is shared.

Your birthday is getting closer.

A lovely surprise is waiting only for you. 🎁"""
    },

    {
        "subject": "Just A Few More Days",
        "message": """🎂 Time flies...

Every sunrise brings your birthday one step closer.

Stay excited.
Your special day is almost here ❤️"""
    },

    {
        "subject": "Smile More Today",
        "message": """😊 Smile today.

Smile tomorrow.

Smile every day.

Because your happiest celebration is getting closer. 💕"""
    },

    {
        "subject": "Keep Counting",
        "message": """✨ Beautiful moments take time.

Keep counting the days.

Your birthday magic is almost ready. 🎉"""
    },

    {
        "subject": "Someone Has A Surprise",
        "message": """💝 Someone has prepared something special.

Don't worry...

You'll see it on your birthday. 🎂"""
    },

    {
        "subject": "Advance Happy Birthday",
        "message": """🎈 Advance Happy Birthday!

May every day before your birthday be filled with happiness.

See you on your special day. ❤️"""
    },

    {
        "subject": "The Countdown Begins",
        "message": """⏳ Your birthday countdown has officially started.

Every day brings you closer to smiles,
love,
and wonderful memories. 🌸"""
    }

]


def get_random_quote():
    return random.choice(quotes)