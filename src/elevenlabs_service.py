import os
import sys
import elevenlabs

from decouple import config


class ElevenLabsService:
    api_key = ""
    voices = [];
    voice = None

    def __init__(self) -> None:
        self.api_key = config("ELEVENLABS_API_KEY")

        if not self.api_key:
            print(
                "Error: ELEVENLABS_API_KEY is missing in the .env file.",
                file=sys.stderr,
            )
            sys.exit(1)

        elevenlabs.set_api_key(self.api_key)

    def list_voices(self):
        self.populate_voice_list()

        for voice in self.voices:
            print(f"{voice.name}: {voice.description}")

    def populate_voice_list(self):
        voices = elevenlabs.voices()
        self.voices = list(filter(lambda x: x.category == "cloned", voices))
        
    def set_voice(self, voice_name):
        self.populate_voice_list()

        for voice in self.voices:
            if voice.name == voice_name:
                self.voice = voice
                return

        print(f"Invalid voice specified or not found in your ElevenLabsAccount. The voice you tried to use was: {voice_name}. Please make sure this voice is available in your account using the API key you provided in the env file.")
        exit(1)

    def generate_audio(self, text):
        audio = elevenlabs.generate(text, voice = self.voice, model="eleven_multilingual_v2")
        
        with open("temp.mp3", "wb") as f:
            f.write(audio)

