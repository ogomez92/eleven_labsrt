# Eleven_labsrt

This project helps you generate audio files using .srt (subtitle) files and a text-to-speech provider. Two providers are supported and are fully interchangeable: [ElevenLabs](https://www.elevenlabs.io) (default) and [60db](https://60db.ai). Select one per run with the `-p`/`--provider` flag.

The idea is that it will first generate (and cache) all strings in your subtitles and then mix in the results in an audio file, respecting times as much as possible, for example if two subtitles overlap it will append them next to each other, never stripping any parts of the audio.

**IMPORTANT NOTE**: This project requires ffmpeg. Please follow the installation instructions for your operating system:

on mac with homebrew:

```bash
brew install ffmpeg
```

on Linux (using aptitude):

```bash
apt install ffmpeg
```

On windows you have several options like winget or chocolately. the easiest one is with winget if you have Windows 10 or 11.

```shell
winget install --id=Gyan.FFmpeg -e
```

## Installation

First, install dependencies:
```bash
pip install -r requirements.txt
```

You will then need an API key for whichever provider you want to use.

- **ElevenLabs:** register for an account (paying for a plan lifts the small free character limit). Open the user dropdown, select `Profile`, and your API key is in the modal dialog that pops up.
- **60db:** obtain an API key from your [60db](https://60db.ai) account.

Create a `.env` file like this:

```env
ELEVENLABS_API_KEY = xxxxxx
SIXTYDB_API_KEY = yyyyyy
``````

Where `xxxxx` is your ElevenLabs API key and `yyyyyy` is your 60db API key. You only need to set the key for the provider(s) you intend to use.

## Usage

This is a command line app which accepts the following arguments:

## Documentation for Command Line Arguments

This application accepts several command line arguments to customize its behavior. Here is a brief description of each:

- `-p`, `--provider`: The TTS provider to use for this run. One of `elevenlabs` (default) or `60db`. All other behavior (voices, caching, mixing) is identical regardless of provider. Caches are kept separate per provider under `cache/<provider>/<voice>/`.

- `-l`, `--list-voices`: This flag, when specified, lists all available voices from the selected provider's account. Note that specifying this action does not convert anything.

- `-i`, `--input-file`: This argument should be followed by the path to the input SRT file to be processed (-i 01.srt).

- `-o`, `--output-file`: This argument should be followed by the path to the output mp3 file to generate. If not specified, the default is `output.mp3`.

- `-d`, `--debug`: This flag, when specified, enables the debug or verbose mode.

- `-v`, `--voice`: This argument should be followed by the name (or voice ID) of the voice to use when converting subtitles. The voice must exist on the account of the selected provider (whose API key is used). If no voice is specified, the app will bail out.

- `-q`, `--prefer-queue`: This flag, when specified, places overlapping subtitles sequentially. If neither this nor `--prefer-speedup` is specified, the app will use this by default.

- [WIP]`-s`, `--prefer-speedup`: This flag, when specified, prefers speeding up audio to fit overlapping subtitles. If neither `--prefer-speedup` nor `--prefer-queue` is specified, queue is used.

## Choosing a provider

The app supports two interchangeable TTS providers, selected per run with `-p`/`--provider`. ElevenLabs is the default, so existing commands keep working unchanged.

```bash
# List the voices available on each provider
python src/main.py -l                       # ElevenLabs (default)
python src/main.py -p 60db -l               # 60db

# Generate audio with ElevenLabs (default provider)
python src/main.py -v "Rachel" -i 01.srt -o out.mp3

# Generate the same thing with 60db
python src/main.py -p 60db -v "VoiceName" -i 01.srt -o out.mp3
```

Everything other than the provider choice is identical: voice selection, the character-count cost prompt, caching, and the final mix. Caches are kept separate per provider under `cache/<provider>/<voice>/`, so the same voice name on different providers never collides.

## Providers

| Provider | Flag value | API key (.env) | Endpoints used |
|----------|------------|----------------|----------------|
| ElevenLabs (default) | `elevenlabs` | `ELEVENLABS_API_KEY` | `text_to_speech.convert` (SDK), `voices.get_all` |
| 60db | `60db` | `SIXTYDB_API_KEY` | `POST /tts-synthesize`, `GET /myvoices` |

The 60db integration uses the synchronous `tts-synthesize` endpoint (returns base64-encoded MP3) with sensible tuning defaults (speed `1`, stability `50`, similarity `75`, enhance `true`).

## Generating only a set of subtitles

You can create a file called `include.txt` with the following format:

```txt
1
2
3
```

This is lines containing only single numbers which are subtitle indexes.

when you open this tool and this file is detected, you will be asked if you want to use this include file or generate the entire subtitle list.
