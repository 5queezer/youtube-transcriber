# YouTube Video Transcriber & Summarizer

This Python CLI tool allows you to download YouTube videos, transcribe them, and optionally summarize and translate the transcriptions. It supports multiple translation engines, including Opus MT and OpenAI's GPT.

## Features

- Download and transcribe YouTube videos
- Generate SRT files with timestamps
- Translate transcriptions into different languages
- Summarize transcriptions or translated text
- Easy-to-use command-line interface (CLI)

## Installation

### Prerequisites

- Python 3.7+
- `ffmpeg` (Make sure `ffmpeg` is installed and accessible via your PATH)

## Usage
```
python main.py transcribe-and-summarize [OPTIONS] VIDEO_URL
```

Options:
- `--summarize`: Summarize the transcription.
- `--translate TEXT`: Translate the transcription to the specified language (e.g., 'es' for Spanish).
- `--translator [opus|chatgpt]`: Choose the translator: 'opus' for Opus MT, 'chatgpt' for OpenAI GPT.
- `--openai-api-key TEXT`: Your OpenAI API key (required if using chatgpt).

