import sys
from elevenlabs.client import ElevenLabs
from decouple import config

class ElevenLabsService:
    api_key = ""
    voices = []  # list of voice metadata objects
    voice_id = None

    def __init__(self) -> None:
        self.api_key = config("ELEVENLABS_API_KEY")
        if not self.api_key:
            print(
                "Error: ELEVENLABS_API_KEY is missing in the .env file.",
                file=sys.stderr,
            )
            sys.exit(1)
        self.elevenlabs = ElevenLabs(api_key=self.api_key)

    def list_voices(self):
        self.populate_voice_list()
        print("Available voices:\n")
        for v in self.voices:
            print(f"- Name: {v.name} | ID: {v.voice_id} | Category: {getattr(v, 'category', 'unknown')} | Description: {v.description}")

    def populate_voice_list(self):
        resp = self.elevenlabs.voices.get_all()
        # The SDK might return a structure, adapt accordingly
        try:
            voices_list = list(resp)[0][1]
        except Exception:
            voices_list = resp
        # Filter or accept all categories, up to you
        self.voices = voices_list

    def set_voice(self, voice_identifier):
        """
        voice_identifier can be voice name or voice_id
        """
        self.populate_voice_list()
        for v in self.voices:
            if v.name == voice_identifier or v.voice_id == voice_identifier:
                self.voice_id = v.voice_id
                return
        print(f"Invalid voice specified or not found in your ElevenLabs account. Tried: {voice_identifier}")
        sys.exit(1)

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
