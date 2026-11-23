import asyncio
import edge_tts

VOICE = "sv-SE-MattiasNeural"

TEXT = "Haha! Jag vann! Bättre lycka nästa gång!"


async def main():
    settings = [
        ("neutral", "+0%", "+0Hz"),
        ("higher", "+10%", "+20Hz"),
        ("synthetic_base", "+20%", "+35Hz"),
    ]

    for name, rate, pitch in settings:
        speech = edge_tts.Communicate(
            text=TEXT,
            voice=VOICE,
            rate=rate,
            pitch=pitch,
        )

        await speech.save(f"audio/{name}.mp3")

        print(f"Generated {name}.mp3")


asyncio.run(main())