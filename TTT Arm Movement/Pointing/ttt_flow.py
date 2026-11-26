import random
import sys
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

SFX_DIR = PROJECT_ROOT / "RPS SFX"
AUDIO_DIR = SFX_DIR / "audio"

sys.path.insert(0, str(SFX_DIR))

from sfx import get_sound


# ============================================================
# BOARD POSITIONS
# ============================================================

# Board layout:
#
#     0 | 1 | 2
#    ---+---+---
#     3 | 4 | 5
#    ---+---+---
#     6 | 7 | 8
#
# Each position has:
#   - Row audio
#   - Column audio
#   - Pointing coordinates (to be calibrated)
#
# IMPORTANT:
# Coordinates are placeholders and must be calibrated
# for the actual G1 and whiteboard setup.
#
# Coordinate frame and arm configuration must also be
# established before physical movement is enabled.

POSITIONS = {
    0: {
        "row": "top",
        "column": "left",
        "coordinates": None,
    },
    1: {
        "row": "top",
        "column": "center",
        "coordinates": None,
    },
    2: {
        "row": "top",
        "column": "right",
        "coordinates": None,
    },
    3: {
        "row": "middle",
        "column": "left",
        "coordinates": None,
    },
    4: {
        "row": "middle",
        "column": "center",
        "coordinates": None,
    },
    5: {
        "row": "middle",
        "column": "right",
        "coordinates": None,
    },
    6: {
        "row": "bottom",
        "column": "left",
        "coordinates": None,
    },
    7: {
        "row": "bottom",
        "column": "center",
        "coordinates": None,
    },
    8: {
        "row": "bottom",
        "column": "right",
        "coordinates": None,
    },
}


# ============================================================
# AUDIO PLAYER
# ============================================================

class AudioPlayer:
    """
    Plays existing WAV recordings.

    By default, uses Windows playback for testing.

    On the G1, provide a playback function that accepts
    a WAV file path and plays it through the robot.
    """

    def __init__(self, playback_function=None):
        self.playback_function = playback_function

    def play_file(self, path):
        path = Path(path)

        if not path.is_file():
            raise FileNotFoundError(
                f"Audio file not found: {path}"
            )

        if self.playback_function is not None:
            self.playback_function(path)
            return

        # Local Windows testing
        if sys.platform == "win32":
            import winsound

            winsound.PlaySound(
                str(path),
                winsound.SND_FILENAME
            )

        else:
            # No hardware playback configured
            print(f"[AUDIO] {path.name}")

    def play(self, name):
        """
        Play an existing named recording.

        Example:
            play("hello")
            play("choose")
            play("top")
        """

        path = AUDIO_DIR / f"{name}.wav"

        self.play_file(path)

    def play_random(self, result):
        """
        Play one random result recording.

        result:
            win
            lose
        """

        path = get_sound(result)

        self.play_file(path)


# ============================================================
# POINTING CONTROLLER
# ============================================================

class PointingController:
    """
    Handles the nine whiteboard positions.

    A movement function can later be connected
    to the actual G1 arm controller.
    """

    def __init__(self, movement_function=None):
        self.movement_function = movement_function

    def point_at(self, position):

        if position not in POSITIONS:
            raise ValueError(
                f"Invalid board position: {position}"
            )

        coordinates = POSITIONS[position]["coordinates"]

        # Local testing
        if self.movement_function is None:
            print(f"[POINT] Position {position}")
            return

        # Hardware mode
        if coordinates is None:
            raise ValueError(
                f"Position {position} has no calibrated coordinates."
            )

        self.movement_function(coordinates)


# ============================================================
# TIC TAC TOE VOICE CONTROLLER
# ============================================================

class TTTVoiceController:
    """
    Handles the spoken announcements for Tic Tac Toe.
    """

    def __init__(self, audio_player):
        self.audio = audio_player

    def announce_position(self, position):
        """
        Announce a board position using two audio files.
        """

        if position not in POSITIONS:
            raise ValueError(
                f"Invalid board position: {position}"
            )

        data = POSITIONS[position]

        self.audio.play(data["row"])
        self.audio.play(data["column"])

    def hello(self):
        self.audio.play("hello")

    def goodbye(self):
        self.audio.play("goodbye")

    def play_again(self):
        self.audio.play("play_again")

    def announce_choose(self, position):
        """
        Example:
        Jag väljer + längst upp + till vänster
        """

        self.audio.play("choose")
        self.announce_position(position)

    def announce_move(self, source, destination):
        """
        Example:
        Jag flyttar + längst upp + till vänster
        + till + längst ner + till höger
        """

        self.audio.play("move")

        self.announce_position(source)

        self.audio.play("to")

        self.announce_position(destination)

    def announce_result(self, result):
        """
        Result is relative to the robot.

        win  = Robot wins
        lose = Human wins
        """

        if result not in ("win", "lose"):
            raise ValueError(
                f"Invalid result: {result}"
            )

        self.audio.play_random(result)


# ============================================================
# TIC TAC TOE FLOW CONTROLLER
# ============================================================

class TTTFlow:
    """
    Coordinates audio and pointing.

    This class does not calculate legal moves or determine
    the winner. Those responsibilities belong to the
    existing Tic Tac Toe game logic.
    """

    def __init__(self, audio, pointing):

        self.audio = audio
        self.pointing = pointing

        self.voice = TTTVoiceController(audio)

        self.reset()

    def reset(self):
        """
        Reset game-related flow state.
        """

        self.robot_placements = 0
        self.game_finished = False
        self.game_started = False

    # --------------------------------------------------------
    # GAME START
    # --------------------------------------------------------

    def start_game(self):
        """
        Called when a player starts a game.
        """

        self.reset()

        self.game_started = True

        self.voice.hello()

    # --------------------------------------------------------
    # PLACEMENT PHASE
    # --------------------------------------------------------

    def choose_position(self, position):
        """
        Robot announces and points at a new position.

        Intended for the first three robot moves.
        """

        if not self.game_started:
            raise RuntimeError("Game has not started.")

        if self.game_finished:
            raise RuntimeError("Game is already finished.")

        if self.robot_placements >= 3:
            raise RuntimeError(
                "Placement phase is complete."
            )

        if position not in POSITIONS:
            raise ValueError(
                f"Invalid position: {position}"
            )

        print(
            f"\n[PLACEMENT {self.robot_placements + 1}/3]"
        )

        # Speak
        self.voice.announce_choose(position)

        # Point
        self.pointing.point_at(position)

        self.robot_placements += 1

    # --------------------------------------------------------
    # MOVEMENT PHASE
    # --------------------------------------------------------

    def move_position(self, source, destination):
        """
        Robot announces its move and points at both squares.

        Intended for the movement phase after all three
        robot pieces have been placed.
        """

        if not self.game_started:
            raise RuntimeError("Game has not started.")

        if self.game_finished:
            raise RuntimeError("Game is already finished.")

        if self.robot_placements < 3:
            raise RuntimeError(
                "Placement phase is not complete."
            )

        if source not in POSITIONS:
            raise ValueError(
                f"Invalid source position: {source}"
            )

        if destination not in POSITIONS:
            raise ValueError(
                f"Invalid destination position: {destination}"
            )

        if source == destination:
            raise ValueError(
                "Source and destination cannot be the same."
            )

        print(
            f"\n[MOVE] {source} -> {destination}"
        )

        # Speak
        self.voice.announce_move(
            source,
            destination
        )

        # Point to original square
        self.pointing.point_at(source)

        # Point to destination square
        self.pointing.point_at(destination)

    # --------------------------------------------------------
    # GAME RESULT
    # --------------------------------------------------------

    def end_game(self, result):
        """
        Called when the game logic detects a winner.
        """

        if not self.game_started:
            raise RuntimeError("Game has not started.")

        if self.game_finished:
            return

        if result not in ("win", "lose"):
            raise ValueError(
                "Result must be 'win' or 'lose'."
            )

        self.game_finished = True

        print(f"\n[RESULT] {result}")

        self.voice.announce_result(result)

        self.voice.play_again()

    # --------------------------------------------------------
    # REPLAY HANDLING
    # --------------------------------------------------------

    def handle_replay(self, play_again):
        """
        Handle the player's response after a completed game.

        play_again:
            True  = Start another game
            False = Say goodbye
        """

        if not self.game_finished:
            raise RuntimeError(
                "Cannot handle replay before game ends."
            )

        if play_again:
            self.start_game()

        else:
            self.voice.goodbye()
            self.game_started = False


# ============================================================
# LOCAL TESTING
# ============================================================

def print_board():

    print("""
       WHITEBOARD

        0 | 1 | 2
       ---+---+---
        3 | 4 | 5
       ---+---+---
        6 | 7 | 8
    """)


def main():

    audio = AudioPlayer()

    pointing = PointingController()

    game = TTTFlow(
        audio=audio,
        pointing=pointing,
    )

    print("\nTIC TAC TOE FLOW TEST")

    print_board()

    game.start_game()

    while True:

        if game.game_finished:

            choice = input(
                "\nPlay again? (y/n): "
            ).strip().lower()

            if choice == "y":
                game.handle_replay(True)
                continue

            elif choice == "n":
                game.handle_replay(False)
                break

            else:
                print("Invalid choice.")
                continue

        print("\nOPTIONS")

        if game.robot_placements < 3:
            print("1. Choose position")
        else:
            print("1. Move piece")

        print("2. Robot wins")
        print("3. Robot loses")
        print("4. Exit")

        choice = input("\nChoose: ").strip()

        try:

            if choice == "1":

                print_board()

                if game.robot_placements < 3:

                    position = int(
                        input("Position (0-8): ")
                    )

                    game.choose_position(position)

                else:

                    source = int(
                        input("From (0-8): ")
                    )

                    destination = int(
                        input("To (0-8): ")
                    )

                    game.move_position(
                        source,
                        destination
                    )

            elif choice == "2":

                game.end_game("win")

            elif choice == "3":

                game.end_game("lose")

            elif choice == "4":

                game.voice.goodbye()
                break

            else:
                print("Invalid choice.")

        except (ValueError, RuntimeError) as error:
            print(f"[ERROR] {error}")


if __name__ == "__main__":
    main()