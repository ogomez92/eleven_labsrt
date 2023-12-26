import json
import uuid
import os

class VocalCache:
    cache_filename = 'cache'
    cache_directory = 'cache'
    voice = None

    def __init__(self, voice_name):
        self.cache = {}
        self.voice = voice_name
        self.cache_directory = os.path.join(self.cache_directory, voice_name)
        self.cache_filename = f"{self.cache_filename}_{self.voice}.json"

    def load_cache(self):
        if not os.path.exists(self.cache_filename):
            with open(self.cache_filename, 'w') as f:
                json.dump({}, f)

        with open(self.cache_filename, 'r') as f:
            self.cache = json.load(f)

        if not os.path.exists(self.cache_directory):
            os.makedirs(self.cache_directory)

    def save_vocal(self, vocal_text):
        try:
            unique_name = str(uuid.uuid4()).replace('-','')
            self.load_cache()

            self.cache[unique_name] = vocal_text
            os.rename('temp.mp3', os.path.join(self.cache_directory, unique_name + '.mp3'))

            self.write_to_disk()

        except Exception as e:
            print(f"There was an error saving the vocal with the text {vocal_text}.")
            print(e)
            exit(1)

    def get_vocal(self, vocal_text):
        try:
            self.load_cache()

            if vocal_text in self.cache.values():
                for key, value in self.cache.items():
                    if value == vocal_text:
                        return open(os.path.join(self.cache_directory, key + '.mp3'), 'rb')

            else:
                return None

        except Exception as e:
            print(f"There was an error getting the seemingly existing vocal with the text {vocal_text}.")
            print(e)
            exit(1)

    def get_cached_strings(self):
        self.load_cache()

        for key in self.cache.copy():
            if not os.path.exists(os.path.join(self.cache_directory, key + '.mp3')):
                del self.cache[key]

        self.write_to_disk()
        return self.cache.values()

    def write_to_disk(self):
        with open(self.cache_filename, 'w') as f:
            json.dump(self.cache, f)
