"""Rock-paper-scissors movements and a small playable game.

Hardware integration is deliberately kept behind ``RobotHand``: connect its
``set_hand_pose`` method to the hand-control API used by your robot. Without a
hardware adapter, the game runs in simulation and prints the requested pose.
"""

from __future__ import annotations

import random
import time
from typing import Protocol


class RobotHand(Protocol):
	"""Minimal interface expected from a robot-hand adapter."""

	def set_hand_pose(self, pose: str) -> None:
		"""Set the hand to ``rock``, ``paper``, or ``scissors``."""


class SimulatedHand:
	"""Safe fallback used when no hardware adapter is supplied."""

	def set_hand_pose(self, pose: str) -> None:
		print(f"[Robot hand] {pose}")


def move_rock(robot: RobotHand) -> None:
	"""Close the hand into a fist."""
	robot.set_hand_pose("rock")


def move_paper(robot: RobotHand) -> None:
	"""Open and spread the fingers."""
	robot.set_hand_pose("paper")


def move_scissors(robot: RobotHand) -> None:
	"""Extend the index and middle fingers; curl the others."""
	robot.set_hand_pose("scissors")


MOVEMENTS = {
	"rock": move_rock,
	"paper": move_paper,
	"scissors": move_scissors,
}
CHOICES = tuple(MOVEMENTS)


def play_round(player_choice: str, robot: RobotHand) -> str:
	"""Perform one robot gesture and return the round result."""
	player_choice = player_choice.strip().lower()
	if player_choice not in MOVEMENTS:
		raise ValueError("Choice must be rock, paper, or scissors.")

	robot_choice = random.choice(CHOICES)
	MOVEMENTS[robot_choice](robot)
	time.sleep(1)  # Give the hand time to finish its gesture.
	print(f"You: {player_choice} | Robot: {robot_choice}")

	if player_choice == robot_choice:
		result = "It's a tie!"
	elif (player_choice, robot_choice) in {
		("rock", "scissors"),
		("paper", "rock"),
		("scissors", "paper"),
	}:
		result = "You win!"
	else:
		result = "Robot wins!"
	print(result)
	return result


def play_game(robot: RobotHand | None = None) -> None:
	"""Play until the user enters ``q`` or ``quit``."""
	robot = robot or SimulatedHand()
	print("Rock Paper Scissors — enter rock, paper, scissors, or q to quit.")
	while True:
		choice = input("Your choice: ").strip().lower()
		if choice in {"q", "quit"}:
			print("Thanks for playing!")
			break
		if choice not in MOVEMENTS:
			print("Please enter rock, paper, or scissors.")
			continue
		play_round(choice, robot)


if __name__ == "__main__":
	play_game()

