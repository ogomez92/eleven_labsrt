from cli_parser import get_args
from elevenlabs_service import ElevenLabsService
from audio_manager import AudioManager
from subtitle_helper import SubtitleHelper
from vocal_cache import VocalCache

def main():
    # Parse command line arguments
    args = get_args()
    elevenLabsService = ElevenLabsService()

    if args.list_voices:
        elevenLabsService.list_voices()
        exit(0)
    
    if args.voice:
        elevenLabsService.set_voice(args.voice)

    if not args.input_file:
        print("No input file specified, exiting...")
        exit(0)

    if not args.voice:
        print("Error: No voice selected. Please select a voice using the -v argument.")
        exit(1)

    subtitleHelper = SubtitleHelper(args.input_file)
    strings_to_generate = subtitleHelper.get_strings()

    if args.debug:
        print(f"Successfully retrieved {len(strings_to_generate)} strings.")

    vocalCache = VocalCache(args.voice)
    cached_strings = vocalCache.get_cached_strings()

    if args.debug:
        print(f"Number of cached strings is {len(cached_strings)}")

    total_characters = 0

    for string in strings_to_generate:
        if string not in cached_strings:
            total_characters += len(string)

    if total_characters > 5000:
        print(f"Warning: {total_characters} characters will be processed through ElevenLabs. Do you want to continue? (y/n)")

        if input() != "y":
            print("Aborting...")
            exit()

    audioManager = AudioManager(subtitleHelper, vocalCache, elevenLabsService)
    audioManager.generate_audio_files()
    audioManager.create_mix()

if __name__ == "__main__":
    main()