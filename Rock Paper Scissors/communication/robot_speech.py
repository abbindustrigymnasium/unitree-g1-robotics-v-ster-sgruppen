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
# AUDIO CONFIGURATION
# ============================================================

# Optional G1 playback function.
# If None, use local Windows audio or print on Linux.
_playback_function = None


def configure_audio(playback_function):
    """
    Connect a playback function.

    The function must accept a WAV file path.

    Example:
        configure_audio(g1_player.play)
    """
    global _playback_function
    _playback_function = playback_function


def play_file(path):
    """
    Play a WAV file using the configured backend.
    """

    path = Path(path)

    if not path.is_file():
        raise FileNotFoundError(
            f"Audio file not found: {path}"
        )

    print(f"[AUDIO] {path.name}")

    if _playback_function is not None:
        _playback_function(path)
        return

    # Windows development/testing
    if sys.platform == "win32":
        import winsound

        winsound.PlaySound(
            str(path),
            winsound.SND_FILENAME
        )

    else:
        print("[AUDIO] No playback backend configured.")


def play(name):
    """
    Play a named WAV file.
    """
    play_file(AUDIO_DIR / f"{name}.wav")


# ============================================================
# GAME START / END
# ============================================================

def introduce():
    play("hello")


def start_round():
    """
    Called before the RPS countdown.

    The countdown handles its own audio.
    """
    print("\nStarting RPS round...")


def goodbye():
    play("goodbye")


# ============================================================
# COUNTDOWN
# ============================================================

def countdown(on_reveal=None):
    """
    Four-beat Swedish RPS countdown.

    Beat 1: Sten
    Beat 2: Sax
    Beat 3: På
    Beat 4: Sä

    Starts the reveal callback on beat 4.
    """

    play("rock")
    play("scissors")
    play("på")

    # Begin the robot's reveal movement.
    if on_reveal is not None:
        on_reveal()

    play("sä")


# ============================================================
# ROBOT MOVE ANNOUNCEMENT
# ============================================================

def announce_move(move):
    """
    Announce the robot's selected gesture.
    """

    sounds = {
        "ROCK": "rock",
        "PAPER": "paper",
        "SCISSORS": "scissors",
    }

    if move not in sounds:
        raise ValueError(
            f"Invalid robot move: {move}"
        )

    play("choose")
    play(sounds[move])


# ============================================================
# RESULT ANNOUNCEMENT
# ============================================================

def announce_result(result):
    """
    Result relative to the robot.

    ROBOT  -> random winning phrase
    PLAYER -> random losing phrase
    DRAW   -> no result announcement
    """

    if result == "ROBOT":
        play_file(get_sound("win"))

    elif result == "PLAYER":
        play_file(get_sound("lose"))

    elif result == "DRAW":
        print("[RESULT] Draw")

    elif result == "INVALID":
        print("[RESULT] Invalid round")

    else:
        raise ValueError(
            f"Unknown result: {result}"
        )


# ============================================================
# RETRY
# ============================================================

def ask_for_retry():
    """
    Camera could not recognize a human gesture.

    No dedicated retry recording exists yet.
    """
    print(
        "[ROBOT] Jag kunde inte se ditt tecken. "
        "Försök igen."
    )


# ============================================================
# PLAY AGAIN
# ============================================================

def play_again():
    play("play_again")