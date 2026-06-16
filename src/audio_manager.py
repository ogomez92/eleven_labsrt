from cli_parser import get_args
import pydub

class AudioManager:
    subtitles = None
    strings = None
    vocal_cache = None
    args = get_args()
    tts_service = None

    def __init__(self, subtitles, cache, tts_service):
        self.subtitles = subtitles;
        self.vocal_cache = cache
        self.tts_service = tts_service

    def generate_audio_files(self):
        self.strings = self.subtitles.get_strings()

        counter = 0

        for string in self.strings:
            if self.vocal_cache.get_vocal(string) is None:
                try:
                    print(f"Generating vocal for text {string}...")
                    self.tts_service.generate_audio(string)
                    counter += 1
                    print(f"Generated string {counter} of {len(self.strings)}")

                except Exception as e:
                    print(f"Error generating vocal for text {string}: {e}")
                    print(e)
                    exit(1)

                self.vocal_cache.save_vocal(string)

            else:
                counter += 1

    def create_mix(self):
        print("Creating mix...")
        
        entire_mix = pydub.AudioSegment.empty()

        for subtitle in self.subtitles:
            print(f"Adding subtitle {subtitle['content']} to mix...")
            audio_subtitle = pydub.AudioSegment.from_mp3(self.vocal_cache.get_vocal(subtitle['content']))
            if entire_mix.duration_seconds * 1000.0 < subtitle['start_time']:
                entire_mix += pydub.AudioSegment.silent(duration=subtitle['start_time'] - entire_mix.duration_seconds * 1000.0)

            entire_mix += audio_subtitle

        entire_mix.export(self.args.output_file, format="mp3")