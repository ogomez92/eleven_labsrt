# Eleven_labsrt

This project helps you generate audio files using .srt (subtitle) files and [ElevenLabs](https://www.elevenlabs.io).

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

You will then need to obtain an ElevenLabs API key by registering for an account and paying for one of their plans (otherwise you are limited to a small number of characters).

To get your API key just go into the user dropdown and select `Profile`.

There is a modal dialog that pops up and your API key is in there, just create a .env file like this:

```env
ELEVENLABS_API_KEY = xxxxxx
``````

Where xxxxx is your API key.

## Usage

This is a command line app which accepts the following arguments:

## Documentation for Command Line Arguments

This application accepts several command line arguments to customize its behavior. Here is a brief description of each:

- `-l`, `--list-voices`: This flag, when specified, lists all available voices from your ElevenLabs account, excluding default voices not cloned by you. Note that specifying this action does not convert anything.

- `-i`, `--input-file`: This argument should be followed by the path to the input SRT file to be processed (-i 01.srt).

- `-o`, `--output-file`: This argument should be followed by the path to the output mp3 file to generate. If not specified, the default is `output.mp3`.

- `-d`, `--debug`: This flag, when specified, enables the debug or verbose mode.

- `-v`, `--voice`: This argument should be followed by the name of the voice to use when converting subtitles. The voice must be a valid voice on the ElevenLabs user account whose API key is used. If no voice is specified, the app will bail out.

- `-q`, `--prefer-queue`: This flag, when specified, places overlapping subtitles sequentially. If neither this nor `--prefer-speedup` is specified, the app will use this by default.

- [WIP]`-s`, `--prefer-speedup`: This flag, when specified, prefers speeding up audio to fit overlapping subtitles. If neither `--prefer-speedup` nor `--prefer-queue` is specified, queue is used.
