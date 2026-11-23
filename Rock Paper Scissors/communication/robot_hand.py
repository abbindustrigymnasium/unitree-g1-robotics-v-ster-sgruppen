import os
import time
from pathlib import Path

from dotenv import load_dotenv
from inspire_rh56dftp import InspireHand


load_dotenv(Path(__file__).resolve().parents[2] / ".env")
UNITREE_G1_IP = os.getenv("UNITREE_G1_IP")
assert UNITREE_G1_IP, "UNITREE_G1_IP must be set in .env"


class RobotHand:

    def __init__(self):
        self.hand = None

        try:
            self.hand = InspireHand(ip=UNITREE_G1_IP)
        except (OSError, RuntimeError, TimeoutError) as error:
            print(f"Warning: could not connect to Inspire hand: {error}")

        self.gestures = {
            "ROCK":     [0, 0, 0, 0, 0, 1000],
            "PAPER":    [1000, 1000, 1000, 1000, 0, 1000],
            "SCISSORS": [0, 0, 1000, 1000, 0, 1000]
        }

    def perform_gesture(self, move):
        if move not in self.gestures:
            print(f"Unknown gesture: {move}")
            return False

        if self.hand is None:
            print(f"Warning: skipping hand gesture {move}; hand is unavailable.")
            return False

        print(f"Robot hand performing: {move}")
        try:
            self.hand.send_raw(self.gestures[move])
            return True
        except (OSError, RuntimeError, TimeoutError) as error:
            print(f"Warning: hand gesture failed: {error}")
            return False

    def relax(self):
        if self.hand is None:
            return

        print("Opening hand...")
        self.hand.send_raw([1000, 1000, 1000, 1000, 1000, 500])

    def close(self):
        if self.hand is not None:
            self.hand.close()
            print("Hand disconnected.")