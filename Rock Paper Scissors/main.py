import random

from game.game_logic import determine_winner
from communication import robot_speech
from camera.camera_recognition import CameraRecognizer
from communication.robot_hand import RobotHand

# ============================================================

# ROBOT MOVE

# ============================================================

def choose_robot_move():
    moves = ["ROCK", "PAPER", "SCISSORS"]
    return random.choice(moves)

# ============================================================

# PLAY ONE ROUND

# ============================================================

def play_round(camera, robot_hand):
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

    print(f"\nPlayer chose: {player_move}")

    # Reveal robot's move
    robot_speech.announce_move(robot_move)
    robot_hand.perform_gesture(robot_move)

    # Determine winner
    result = determine_winner(robot_move, player_move)

    robot_speech.announce_result(result)


# ============================================================

# MAIN GAME

# ============================================================

def main():

    camera = CameraRecognizer()
    robot_hand = RobotHand()

    try:
        while True:
            play_round(camera, robot_hand)

            again = input("\nPlay another round? (y/n): ").strip().lower()

            if again != "y":
                break

    except KeyboardInterrupt:
        print("\nStopping game...")

    finally:
        robot_hand.relax()
        robot_hand.close()
        camera.close()

# ============================================================

# START

# ============================================================

if __name__ == "__main__":
    main()
