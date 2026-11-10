import subprocess
from pathlib import Path


import asyncio
import tempfile
import edge_tts
import parselmouth
from parselmouth.praat import call
import imageio_ffmpeg
import numpy as np
from scipy.io import wavfile
from scipy.signal import hilbert, butter, sosfilt


def robotify_audio(
    input_file,
    output_file,
    frequency_shift=40,
):
    """
    Apply a single-sideband frequency shift to speech.

    frequency_shift:
        0  = unchanged voice
        20 = mild electronic effect
        40 = metallic robot
        70 = strong sci-fi robot

    Unlike pitch shifting, this moves all frequencies
    by the same number of Hz rather than scaling them.
    """

    sample_rate, audio = wavfile.read(input_file)

    if np.issubdtype(audio.dtype, np.integer):
        info = np.iinfo(audio.dtype)
        audio = audio.astype(np.float64) / max(
            abs(info.min), info.max
        )
    else:
        audio = audio.astype(np.float64)

    if audio.ndim == 2:
        audio = audio.mean(axis=1)

    if len(audio) == 0:
        raise ValueError("Input audio is empty")

    # Remove very low-frequency rumble.
    sos = butter(
        3,
        90,
        btype="highpass",
        fs=sample_rate,
        output="sos",
    )

    audio = sosfilt(sos, audio)

    # Create an analytic signal.
    analytic = hilbert(audio)

    # Shift the entire frequency spectrum.
    t = np.arange(len(audio)) / sample_rate

    shifted = np.real(
        analytic * np.exp(
            2j * np.pi * frequency_shift * t
        )
    )

    # Very gentle saturation.
    shifted = np.tanh(shifted * 1.1)

    # Normalize volume.
    peak = np.max(np.abs(shifted))

    if peak > 0:
        shifted = shifted / peak * 0.9

    wavfile.write(
        output_file,
        sample_rate,
        (shifted * 32767).astype(np.int16),
    )


def convert_mp3_to_wav(mp3_path, wav_path):
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

    subprocess.run(
        [
            ffmpeg,
            "-y",
            "-loglevel", "error",
            "-i", str(mp3_path),
            "-ac", "1",
            "-ar", "24000",
            str(wav_path),
        ],
        check=True,
    )


def make_monotone(input_file, output_file, strength=0.45):
    """
    Reduce natural pitch variation.

    strength:
        0.0 = original intonation
        0.45 = moderately monotone
        1.0 = completely flat pitch
    """

    strength = max(0.0, min(1.0, strength))

    sound = parselmouth.Sound(str(input_file))

    manipulation = call(
        sound,
        "To Manipulation",
        0.01,
        65,
        450
    )

    pitch_tier = call(manipulation, "Extract pitch tier")

    count = int(call(pitch_tier, "Get number of points"))

    if count == 0:
        sound.save(str(output_file), "WAV")
        return

    points = []

    for i in range(1, count + 1):
        time = call(pitch_tier, "Get time from index", i)
        pitch = call(pitch_tier, "Get value at index", i)
        points.append((time, pitch))

    # Use the median pitch as the center.
    median_pitch = float(
        np.median([pitch for _, pitch in points])
    )

    # Remove existing pitch points.
    call(
        pitch_tier,
        "Remove points between",
        sound.xmin,
        sound.xmax
    )

    # Rebuild the pitch contour with reduced variation.
    for time, pitch in points:
        new_pitch = (
            median_pitch
            + (pitch - median_pitch) * (1 - strength)
        )

        call(pitch_tier, "Add point", time, new_pitch)

    call([pitch_tier, manipulation], "Replace pitch tier")

    result = call(
        manipulation,
        "Get resynthesis (overlap-add)"
    )

    result.save(str(output_file), "WAV")


def speed_up(input_file, output_file, speed=1.12):
    """
    Speed up speech without changing its pitch.
    """

    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

    subprocess.run(
        [
            ffmpeg,
            "-y",
            "-loglevel", "error",
            "-i", str(input_file),
            "-filter:a", f"atempo={speed}",
            str(output_file),
        ],
        check=True
    )
VOICE = "sv-SE-MattiasNeural"

PHRASES = {
    # Robot wins
    "win_01": "Jag vann. Det var nästan oväntat.",
    "win_02": "Mina beräkningar verkar fungera utmärkt.",
    "win_03": "Intressant strategi. Tyvärr fungerade den inte.",
    "win_04": "Ännu en seger för artificiell intelligens.",
    "win_05": "Jag skulle säga bra försök, men jag är programmerad att vara ärlig.",

    # Robot loses
    "lose_01": "Du vann. Det hade jag inte räknat med.",
    "lose_02": "Jag misstänker att du hade tur. Men bra spelat.",
    "lose_03": "Det här resultatet behöver jag analysera närmare.",
    "lose_04": "Tydligen är människan fortfarande konkurrenskraftig.",
    "lose_05": "Jag erkänner min förlust. Motvilligt.",
}


async def generate_audio():
    audio_dir = Path("audio")
    audio_dir.mkdir(exist_ok=True)

    for name, text in PHRASES.items():
        print(f"Generating {name}...")

        # Temporary files are deleted automatically.
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir = Path(temp_dir)

            mp3 = temp_dir / "original.mp3"
            wav = temp_dir / "original.wav"
            monotone = temp_dir / "monotone.wav"
            faster = temp_dir / "faster.wav"

            # 1. Generate Swedish speech
            speech = edge_tts.Communicate(
                text=text,
                voice=VOICE,
                rate="+0%",
                pitch="+0Hz",
            )

            await speech.save(str(mp3))

            # 2. Convert MP3 to WAV
            convert_mp3_to_wav(mp3, wav)

            # 3. Reduce pitch variation
            make_monotone(
                wav,
                monotone,
                strength=0.45,
            )

            # 4. Speed up without changing pitch
            speed_up(
                monotone,
                faster,
                speed=1.12,
            )

            # 5. Apply robotic frequency shifting
            output = audio_dir / f"{name}.wav"

            robotify_audio(
                faster,
                output,
                frequency_shift=40,
            )


            # Convert finished audio to the G1's required format.
            g1_output = temp_dir / "g1_ready.wav"

            ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

            subprocess.run(
                [
                    ffmpeg,
                    "-y",
                    "-loglevel", "error",
                    "-i", str(output),
                    "-ar", "16000",
                    "-ac", "1",
                    "-c:a", "pcm_s16le",
                    str(g1_output),
                ],
                check=True,
            )

            # Replace the original output with the converted version.
            g1_output.replace(output)

            print(f"Saved: {output}")

    print("\nAll audio generated successfully!")


if __name__ == "__main__":
    asyncio.run(generate_audio())