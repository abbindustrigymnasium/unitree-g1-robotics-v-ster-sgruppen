import os
import subprocess
from typing import Protocol


class RobotHand(Protocol):
    """Kept for compatibility with the existing project."""

    def set_hand_pose(self, pose: str) -> None:
        ...


class SimulatedHand:
    """Fallback hand implementation."""

    def set_hand_pose(self, pose: str) -> None:
        print(f"[Robot hand] {pose}")


def move_rock(robot):
    robot.perform_gesture("ROCK")


def move_paper(robot):
    robot.perform_gesture("PAPER")


def move_scissors(robot):
    robot.perform_gesture("SCISSORS")


MOVEMENTS = {
    "rock": move_rock,
    "paper": move_paper,
    "scissors": move_scissors,
}

CHOICES = tuple(MOVEMENTS)


class ArmGestureController:
    """Execute RPS arm gestures on the G1 through SSH."""

    def __init__(
        self,
        host: str = "unitree@192.168.123.164",
        executable: str = "/home/unitree/unitree_sdk2-2.0.2/build/bin/g1_rps_gestures",
    ) -> None:
        self.host = host
        self.executable = executable

    def is_available(self) -> bool:
        return True

    def perform_gesture(self, move: str) -> bool:
        move = move.strip().upper()

        if move not in {"ROCK", "PAPER", "SCISSORS"}:
            print(f"Unknown arm gesture: {move}")
            return False

        remote_command = (
            f"bash --noprofile --norc -c "
            f"'exec {self.executable} eth0 {move}'"
        )

        print(f"Sending {move} gesture to G1...")

        try:
            subprocess.run(
                [
                    "ssh",
                    "-o", "BatchMode=yes",
                    "-o", "ConnectTimeout=5",
                    self.host,
                    remote_command,
                ],
                check=True,
            )
            print(f"G1 completed {move}.")
            return True

        except (OSError, subprocess.SubprocessError) as error:
            print(f"Warning: remote arm gesture failed: {error}")
            return False


def reveal_gesture(robot_hand, robot_arms: ArmGestureController, move: str) -> bool:
    """Perform the RPS gesture using the robot's arms."""
    return robot_arms.perform_gesture(move)


