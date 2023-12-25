import os
import sys
import elevenlabs

from decouple import config


class ElevenLabsService:
    api_key = ""
    voices = [];

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
        
    # def set_voice(voice_name):
        # self.populate_voice_list()

    # def generate_subtitle(text):
        # use caching
    