import os
import sys
import elevenlabs

from decouple import config

class ElevenLabsService:
    api_key = ''

    def __init__(self) -> None:
        self.api_key = config('ELEVENLABS_API_KEY')
    
        if not self.api_key:
            print("Error: ELEVENLABS_API_KEY is missing in the .env file.", file=sys.stderr)
            sys.exit(1)

        elevenlabs.set_api_key(self.API_KEY)
