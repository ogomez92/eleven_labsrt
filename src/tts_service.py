import sys

class TTSService:
    """
    Base interface shared by all text-to-speech providers.

    Subclasses must implement populate_voice_list() (filling self.voices with
    normalized voice dicts) and generate_audio(text) (writing the result to
    temp.mp3). Everything downstream (AudioManager, VocalCache) only depends on
    this interface, so providers are fully interchangeable.

    Normalized voice dict shape:
        {"name": str, "voice_id": str, "category": str, "description": str|None}
    """

    def __init__(self) -> None:
        self.voices = []  # list of normalized voice dicts
        self.voice_id = None

    def populate_voice_list(self):
        raise NotImplementedError

    def generate_audio(self, text):
        raise NotImplementedError

    def list_voices(self):
        self.populate_voice_list()
        print("Available voices:\n")
        for v in self.voices:
            print(
                f"- Name: {v['name']} | ID: {v['voice_id']} "
                f"| Category: {v.get('category', 'unknown')} "
                f"| Description: {v.get('description')}"
            )

    def set_voice(self, voice_identifier):
        """voice_identifier can be a voice name or a voice_id."""
        self.populate_voice_list()
        for v in self.voices:
            if v["name"] == voice_identifier or v["voice_id"] == voice_identifier:
                self.voice_id = v["voice_id"]
                return
        print(
            f"Invalid voice specified or not found in your account. "
            f"Tried: {voice_identifier}"
        )
        sys.exit(1)
