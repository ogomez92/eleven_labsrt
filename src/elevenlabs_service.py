import sys
from elevenlabs.client import ElevenLabs
from decouple import config
from tts_service import TTSService

class ElevenLabsService(TTSService):
    def __init__(self) -> None:
        super().__init__()
        self.api_key = config("ELEVENLABS_API_KEY", default="")
        if not self.api_key:
            print(
                "Error: ELEVENLABS_API_KEY is missing in the .env file.",
                file=sys.stderr,
            )
            sys.exit(1)
        self.elevenlabs = ElevenLabs(api_key=self.api_key)

    def populate_voice_list(self):
        resp = self.elevenlabs.voices.get_all()
        # The SDK might return a structure, adapt accordingly
        try:
            voices_list = list(resp)[0][1]
        except Exception:
            voices_list = resp
        self.voices = [
            {
                "name": v.name,
                "voice_id": v.voice_id,
                "category": getattr(v, "category", "unknown"),
                "description": getattr(v, "description", None),
            }
            for v in voices_list
        ]

    def generate_audio(self, text):
        if not self.voice_id:
            print("Error: No voice_id has been set.")
            sys.exit(1)
        # Use convert method per current SDK
        response = self.elevenlabs.text_to_speech.convert(
            text=text,
            voice_id=self.voice_id,
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128"
        )
        with open("temp.mp3", "wb") as f:
            for chunk in response:
                if chunk:
                    f.write(chunk)
