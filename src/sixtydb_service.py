import sys
import base64
import requests
from decouple import config
from tts_service import TTSService

class SixtyDBService(TTSService):
    BASE_URL = "https://api.60db.ai"

    # Hardcoded tuning defaults (match the 60db API defaults).
    DEFAULT_SPEED = 1
    DEFAULT_STABILITY = 50
    DEFAULT_SIMILARITY = 75
    DEFAULT_ENHANCE = True

    def __init__(self) -> None:
        super().__init__()
        self.api_key = config("SIXTYDB_API_KEY", default="")
        if not self.api_key:
            print(
                "Error: SIXTYDB_API_KEY is missing in the .env file.",
                file=sys.stderr,
            )
            sys.exit(1)
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        })

    def populate_voice_list(self):
        resp = self.session.get(f"{self.BASE_URL}/myvoices")
        resp.raise_for_status()
        payload = resp.json()
        # Response shape: {"success": ..., "message": ..., "data": [ ... ]}
        data = payload.get("data", []) if isinstance(payload, dict) else payload
        self.voices = [
            {
                "name": v.get("name"),
                "voice_id": v.get("voice_id"),
                "category": v.get("category", "unknown"),
                "description": v.get("description"),
            }
            for v in data
        ]

    def generate_audio(self, text):
        if not self.voice_id:
            print("Error: No voice_id has been set.")
            sys.exit(1)
        body = {
            "text": text,
            "voice_id": self.voice_id,
            "speed": self.DEFAULT_SPEED,
            "stability": self.DEFAULT_STABILITY,
            "similarity": self.DEFAULT_SIMILARITY,
            "enhance": self.DEFAULT_ENHANCE,
            "output_format": "mp3",
        }
        resp = self.session.post(f"{self.BASE_URL}/tts-synthesize", json=body)
        resp.raise_for_status()
        payload = resp.json()

        if not payload.get("success", True):
            raise RuntimeError(f"60db TTS failed: {payload.get('message')}")

        audio_b64 = payload.get("audio_base64")
        if not audio_b64:
            raise RuntimeError("60db TTS returned no audio data.")

        with open("temp.mp3", "wb") as f:
            f.write(base64.b64decode(audio_b64))
