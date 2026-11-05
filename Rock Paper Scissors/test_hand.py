from communication.robot_hand import RobotHand
import time

hand = RobotHand()

try:
    hand.perform_gesture("ROCK")
    time.sleep(2)

    hand.perform_gesture("PAPER")
    time.sleep(2)

    hand.perform_gesture("SCISSORS")
    time.sleep(2)

    hand.relax()

finally:
    hand.close()