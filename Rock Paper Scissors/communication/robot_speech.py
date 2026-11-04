import time

def countdown():
	print("\nSten...")
	time.sleep(0.7)

	print("Sax...")
	time.sleep(0.7)

	print("Påse!")
	time.sleep(0.2)

	print("VISA DITT TECKEN!")


def say(message):
	"""Simulates the robot speaking."""
	print(f"\n Robot: {message}")

def introduce():
	say("Hej! Vad roligt att du vill spela med mig!")

def start_round():
	say("Då kör vi! Sten, sax, påse!")

def announce_move(move):
	messages = {
		"ROCK": "Jag väljer sten!",
		"PAPER": "Jag väljer påse!",
		"SCISSORS": "Jag väljer sax!"
	}

	say(messages.get(move, "Jag vet inte vad jag ska välja!"))

def announce_result(result):
	messages = {
		"ROBOT": "Yes! Jag vann!",
		"PLAYER": "Snyggt spelat! Du vann!",
		"DRAW": "Oavgjort! Vi kör igen!",
		"INVALID": "Det var en testrunda. Vi kör igen!"
	}

	say(messages.get(result, "Jag förstår inte resultatet."))

def ask_for_retry():
	say("Hmm, jag kunde inte se vad du visade. Kan du försöka igen?")

def goodbye():
	say("Tack för att du spelade med mig! Hejdå!")