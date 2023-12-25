from cli_parser import get_args
from elevenlabs_service import ElevenLabsService
from subtitle_helper import SubtitleHelper

def main():
    # Parse command line arguments
    args = get_args()
    elevenLabsService = ElevenLabsService()

    if args.list_voices:
        elevenLabsService.list_voices()

    elif args.input_file:
        subtitleHelper = SubtitleHelper(args.input_file)
        strings_to_generate = subtitleHelper.get_strings()

        if args.debug:
            print(f"Successfully retrieved {len(strings_to_generate)} strings.")

if __name__ == "__main__":
    main()