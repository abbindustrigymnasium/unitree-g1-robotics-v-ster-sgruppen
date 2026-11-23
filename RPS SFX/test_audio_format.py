from pathlib import Path
import wave

AUDIO_DIR = Path(__file__).parent / "audio"

files = sorted(AUDIO_DIR.glob("*.wav"))

assert len(files) == 10, (
    f"Expected 10 WAV files, found {len(files)}"
)

for path in files:
    with wave.open(str(path), "rb") as wav:
        assert wav.getframerate() == 16000, path
        assert wav.getnchannels() == 1, path
        assert wav.getsampwidth() == 2, path
        assert wav.getcomptype() == "NONE", path

    print(f"PASS: {path.name}")

print("\nAll 10 audio files are G1-compatible.")