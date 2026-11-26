import random
import threading

from game.game_logic import determine_winner
from communication import robot_speech
from camera.camera_recognition import CameraRecognizer

from robot.robot_movement import (
    ArmGestureController,
    reveal_gesture
)

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

ROBOT_OUTPUT = "enp129s0"

sys.path.insert(
    0,
    str(PROJECT_ROOT / "RPS SFX")
)

from g1_audio import G1AudioPlayer





def choose_robot_move():
    return random.choice(["ROCK", "PAPER", "SCISSORS"])


def play_round(camera, robot_arms):

    robot_move = choose_robot_move()

    robot_speech.start_round()

    while True:

        # Prepare robot before countdown.
        if not robot_arms.start_ready():
            print("Could not prepare robot.")
            return False

        # Start robot movement in a separate thread.
        movement_thread = None

        def start_robot_movement():
            nonlocal movement_thread

            movement_thread = threading.Thread(
                target=reveal_gesture,
                args=(None, robot_arms, robot_move)
            )

            movement_thread.start()

        # Robot starts moving exactly when "Påse!" is announced.
        # Camera recognition starts immediately afterward.
        robot_speech.countdown(
            on_reveal=start_robot_movement
        )

        player_move = camera.detect_player_move()

        # Wait until robot finishes its gesture.
        if movement_thread is not None:
            movement_thread.join()

        if player_move != "UNKNOWN":
            break

        robot_speech.ask_for_retry()

    print(f"\nPlayer chose: {player_move}")
    print(f"Robot chose: {robot_move}")

    robot_speech.announce_move(robot_move)

    result = determine_winner(
        robot_move,
        player_move
    )

    robot_speech.announce_result(result)

    return True


def main():

    camera = CameraRecognizer()
    robot_arms = ArmGestureController()

    g1_player = G1AudioPlayer(ROBOT_OUTPUT)

    robot_speech.configure_audio(
        g1_player.play
    )

    try:

        robot_speech.introduce()

        while True:

            if not play_round(camera, robot_arms):
                break

            robot_speech.play_again()
            
            again = input(
                "\nPlay another round? (y/n): "
            ).strip().lower()

            if again != "y":
                break

    except KeyboardInterrupt:
        print("\nStopping game...")

    finally:
        robot_arms.stop()
        camera.close()
        robot_speech.goodbye()


if __name__ == "__main__":
    main()