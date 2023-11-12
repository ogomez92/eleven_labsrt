from cli_parser import create_arg_parser
from elevenlabs_service import ElevenLabsService

def main():
    # Parse command line arguments
    args = create_arg_parser()
    elevenLabsService = ElevenLabsService()

    if args.list_voices:
        elevenLabsService.list_voices()



if __name__ == "__main__":
    main()