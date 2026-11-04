from game_logic import determine_winner

print(determine_winner("ROCK", "SCISSORS"))    # ROBOT
print(determine_winner("PAPER", "SCISSORS"))   # PLAYER
print(determine_winner("ROCK", "ROCK"))        # DRAW
print(determine_winner("INVALID", "ROCK"))     # INVALID