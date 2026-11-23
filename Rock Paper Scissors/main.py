import random

from game.game_logic import determine_winner
from communication import robot_speech
from camera.camera_recognition import CameraRecognizer

# ============================================================

# ROBOT MOVE

# ============================================================

def choose_robot_move():
    moves = ["ROCK", "PAPER", "SCISSORS"]
    return random.choice(moves)

# ============================================================

# PLAY ONE ROUND

# ============================================================

def play_round(camera):
    robot_move = choose_robot_move()

    robot_speech.start_round()

    input("\nTryck ENTER när du är redo...")

    # Countdown
    robot_speech.countdown()

    # Camera takes pictures AFTER "Påse!"
    player_move = camera.detect_player_move()

    while player_move == "UNKNOWN":
        robot_speech.ask_for_retry()

        input("\nTryck ENTER för att försöka igen...")
        robot_speech.countdown()

        player_move = camera.detect_player_move()

    print(f"\nSpelarens val: {player_move}")

    # Reveal robot's move
    robot_speech.announce_move(robot_move)

    # Determine winner
    result = determine_winner(robot_move, player_move)

    robot_speech.announce_result(result)


# ============================================================

# MAIN GAME

# ============================================================

def main():
    camera = None

    try:
        robot_speech.introduce()
        print("\nStartar kameran...")
        camera = CameraRecognizer()

        while True:
            play_round(camera)
            again = input("\nVill du spela en gång till? (j/n): ")
            if again.lower() != "j":
                break

        robot_speech.goodbye()

    except KeyboardInterrupt:
        print("\nSpelet avbröts.")

    except Exception as error:
        print(f"\nEtt fel uppstod: {error}")

    finally:
        if camera is not None:
            camera.close()

# ============================================================

# START

# ============================================================

if __name__ == "__main__":
    main()
