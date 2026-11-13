import time
from inspire_rh56dftp import InspireHand


class RobotHand:

    def __init__(self):
        self.hand = None

        try:
            self.hand = InspireHand(ip="192.168.123.210")
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
            return

        if self.hand is None:
            print(f"Warning: skipping hand gesture {move}; hand is unavailable.")
            return

        print(f"Robot hand performing: {move}")
        self.hand.send_raw(self.gestures[move])

    def relax(self):
        if self.hand is None:
            return

        print("Opening hand...")
        self.hand.send_raw([1000, 1000, 1000, 1000, 1000, 500])

    def close(self):
        if self.hand is not None:
            self.hand.close()
            print("Hand disconnected.")