import json
import uuid
import os

class VocalCache:
    cache_filename = 'cache.json'
    cache_directory = 'cache'

    def __init__(self):
        self.cache = {}
        self.load_cache()

    def load_cache(self):
        with open(self.cache_filename, 'r') as f:
            self.cache = json.load(f)

        if not os.path.exists(self.cache_directory):
            os.makedirs(self.cache_directory)

    def save_vocal(self, vocal_text):
        try:
            unique_name = str(uuid.uuid4())
            self.load_cache()

            self.cache[unique_name] = vocal_text
            os.rename('temp.wav', os.path.join(self.cache_directory, unique_name + '.wav'))

            with open(self.cache_filename, 'w') as f:
                json.dump(self.cache, f)

        except Exception as e:
            print(f"There was an error saving the vocal with the text {vocal_text}.")
            print(e)
            exit(1)

    def get_vocal_if_exists(self, vocal_text):
        try:
            self.load_cache()

            if vocal_text in self.cache:
                with open(os.path.join(self.cache_directory, vocal_text + '.wav'), 'rb') as f:
                    return f.read()

            else:
                return None

        except Exception as e:
            print(f"There was an error getting the seemingly existing vocal with the text {vocal_text}.")
            print(e)
            exit(1)
