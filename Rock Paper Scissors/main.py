# Use this in script:

from camera_recognition import CameraRecognizer

camera = CameraRecognizer()

player_move = camera.detect_player_move()

print("Player chose:", player_move)

camera.close()

# It returns "ROCK", "PAPER", "SCISSORS" or "UNKNOWN" if it can't confidently recognize the gesture.