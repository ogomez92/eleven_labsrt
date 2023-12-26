import argparse

def get_args():
    parser = argparse.ArgumentParser(description='Convert SRT subtitle entries to audio using ElevenLabs and sync them.')

    # Define possible arguments
    parser.add_argument('-l', '--list-voices', help='List available voices from ElevenLabs. specifying this action does not convert anything', action='store_true')
    parser.add_argument('-i', '--input-file', help='Input SRT file to be processed.', type=str)
    parser.add_argument('-d', '--debug', help='Debug/verbose mode.', action='store_true')
    parser.add_argument('-v', '--voice', help='Voice to use when converting subtitles. Must be a valid voice on the ElevenLabs user account whose API key is used', type=str)
    parser.add_argument('-s', '--prefer-speedup', help='Prefer speeding up audio to fit overlapping subtitles. If neither --prefer-speedup nor --prefer-queue is specified, queue is used.', action='store_true')
    parser.add_argument('-q', '--prefer-queue', help='Place overlapping subtitles sequentially. If this nor --prefer-speedup is specified, the app will use this by default.', action='store_true')
    parser.add_argument('-o', '--output-file', default='output.mp3', help='Output mp3 file to generate. Default is output.mp3', type=str)



    # Return the parsed arguments
    return parser.parse_args()
