import os
import subprocess
import select
from pathlib import Path
from typing import Protocol

from dotenv import load_dotenv


load_dotenv(Path(__file__).resolve().parents[2] / ".env")
UNITREE_G1_IP = os.getenv("UNITREE_G1_IP")
assert UNITREE_G1_IP, "UNITREE_G1_IP must be set in .env"


class RobotHand(Protocol):
    def set_hand_pose(self, pose: str) -> None:
        ...


class SimulatedHand:
    def set_hand_pose(self, pose: str) -> None:
        print(f"[Robot hand] {pose}")


class ArmGestureController:

    def __init__(
        self,
        host=None,
        executable="/home/unitree/unitree_sdk2-2.0.2/build/bin/g1_rps_gestures",
    ):
        self.host = host or f"unitree@{UNITREE_G1_IP}"
        self.executable = executable
        self.process = None

    def is_available(self):
        return True

    def start_ready(self):

        if self.process and self.process.poll() is None:
            return True

        remote_command = (
            f"bash --noprofile --norc -c "
            f"'test -x {self.executable} && echo READY'"
        )

        print("Preparing robot...")
        print(f"Connecting via SSH to {self.host}...")

        try:
            ssh_command = [
                "ssh",
                "-o", "BatchMode=yes",
                "-o", "ConnectTimeout=5",
                "-o", "ConnectionAttempts=1",
                self.host,
                remote_command,
            ]

            result = subprocess.run(
                ssh_command,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=10,
            )

            output = result.stdout.strip()
            if output:
                print(output)

            if result.returncode != 0:
                raise RuntimeError(
                    f"SSH readiness check failed (exit status {result.returncode})."
                )

            if output.splitlines()[-1].strip() != "READY":
                raise RuntimeError(
                    "Robot executable was not found or did not respond with READY."
                )

            print("Robot is ready.")
            self.process = None
            return True

        except subprocess.TimeoutExpired:
            print("Preparation failed: SSH readiness check timed out.")
            return False
        except Exception as error:
            print(f"Preparation failed: {error}")
            self.stop()
            return False

    def perform_gesture(self, move):

        move = move.strip().upper()

        if move not in {"ROCK", "PAPER", "SCISSORS"}:
            return False

        remote_command = (
            f"{self.executable} eth0 {move}"
        )

        try:
            print(f"Sending {move} to G1...")

            result = subprocess.run(
                [
                    "ssh",
                    "-o", "BatchMode=yes",
                    "-o", "ConnectTimeout=5",
                    "-o", "ConnectionAttempts=1",
                    self.host,
                    remote_command,
                ],
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=20,
                bufsize=1,
            )

            if result.stdout:
                print(result.stdout, end="")

            if result.returncode != 0:
                print(
                    f"Movement failed: remote gesture exited "
                    f"with status {result.returncode}."
                )
                return False

            return True

        except subprocess.TimeoutExpired:
            print("Movement failed: gesture timed out.")
            return False
        except Exception as error:
            print(f"Movement failed: {error}")
            self.stop()
            return False

    def stop(self):

        if self.process:
            try:
                if self.process.poll() is None:
                    self.process.stdin.close()
                    self.process.wait(timeout=5)

            except Exception:
                self.process.kill()
                self.process.wait()

            self.process = None


def reveal_gesture(robot_hand, robot_arms, move):
    return robot_arms.perform_gesture(move)