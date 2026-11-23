from robot_voice import robotify_audio

robotify_audio(
    "audio/original.wav",
    "audio/robot.wav",
    intensity=1.0,
    robot_pitch=125,
    bands=18,
)

print("Robot voice generated!")