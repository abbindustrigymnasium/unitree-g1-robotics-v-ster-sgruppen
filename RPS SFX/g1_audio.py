from pathlib import Path

from unitree_sdk2py.core.channel import ChannelFactoryInitialize
from unitree_sdk2py.g1.audio.g1_audio_client import AudioClient


class G1AudioPlayer:

    def __init__(self, network_interface):
        ChannelFactoryInitialize(0, network_interface)

        self.client = AudioClient()
        self.client.SetTimeout(10.0)
        self.client.Init()

    def play(self, wav_path):
        """
        Play a WAV file through the G1's speakers.
        """

        import wave
        import time
        import uuid

        wav_path = Path(wav_path)

        with wave.open(str(wav_path), "rb") as wav:
            if (
                wav.getframerate() != 16000
                or wav.getnchannels() != 1
                or wav.getsampwidth() != 2
                or wav.getcomptype() != "NONE"
            ):
                raise ValueError(
                    "G1 requires 16 kHz, mono, 16-bit PCM WAV."
                )

            pcm_data = wav.readframes(wav.getnframes())

        app_name = "rps_sfx"
        stream_id = uuid.uuid4().hex

        # Send PCM data in chunks.
        chunk_size = 96000

        for offset in range(0, len(pcm_data), chunk_size):
            chunk = pcm_data[offset:offset + chunk_size]

            result, _ = self.client.PlayStream(
                app_name,
                stream_id,
                chunk,
            )

            if result != 0:
                raise RuntimeError(
                    f"G1 audio playback failed: {result}"
                )

            time.sleep(1.0)

        # Give the last chunk time to finish playing.
        time.sleep(min(len(pcm_data) / 32000, 3.0))

        self.client.PlayStop(app_name)