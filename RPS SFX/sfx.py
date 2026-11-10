import random
import winsound
from pathlib import Path


AUDIO_DIR = Path(__file__).parent / "audio"

SOUNDS = {
    "win": [
        "win_01.wav",
        "win_02.wav",
        "win_03.wav",
        "win_04.wav",
        "win_05.wav",
    ],
    "lose": [
        "lose_01.wav",
        "lose_02.wav",
        "lose_03.wav",
        "lose_04.wav",
        "lose_05.wav",
    ],
}


def get_sound(result):
    """
    Randomly selects a sound from the correct category.

    result: "win" or "lose"
    Returns: Path to the selected WAV file.
    """

    if result not in SOUNDS:
        raise ValueError(
            f"Invalid result: {result}. Expected 'win' or 'lose'."
        )

    filename = random.choice(SOUNDS[result])
    path = AUDIO_DIR / filename

    if not path.is_file():
        raise FileNotFoundError(f"Missing audio file: {path}")

    return path


def play_result(result):
    """Play a randomly selected sound on Windows."""

    sound = get_sound(result)

    print(f"Playing: {sound.name}")

    winsound.PlaySound(
        str(sound),
        winsound.SND_FILENAME
    )