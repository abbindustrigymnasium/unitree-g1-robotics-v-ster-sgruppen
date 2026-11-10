import random

PHRASES = {
    "win": [
        "Haha! Jag vann!",
        "Bättre lycka nästa gång!",
        "Du får nog öva lite mer!",
        "Ännu en seger för robotarna!",
        "Människan noll, roboten ett!"
    ],

    "lose": [
        "Åh nej! Du vann!",
        "Okej, den rundan fick du!",
        "Jag kräver revansch!",
        "Det där var bara tur!",
        "Mina beräkningar måste vara fel!"
    ],

    "draw": [
        "Oavgjort! Vi kör igen!",
        "Vi tänkte visst likadant!",
        "Ingen vinnare den här gången!",
        "Det blev lika!",
        "En gång till!"
    ]
}


def get_phrase(result):
    if result not in PHRASES:
        raise ValueError(f"Invalid result: {result}")

    return random.choice(PHRASES[result])