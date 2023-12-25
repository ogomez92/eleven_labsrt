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

        total_characters = 0
        for string in strings_to_generate:
            total_characters += len(string)

        if total_characters > 5000:
            # Ask the user if they want to continue (y/n) displaying the number of chracters to be processed.
            print(f"Warning: {total_characters} characters will be processed through ElevenLabs. Do you want to continue? (y/n)")

            if input() != "y":
                print("Aborting...")
                exit()

if __name__ == "__main__":
    main()