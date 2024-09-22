# YouTube Video Transcriber & Summarizer

This Python CLI tool allows you to download YouTube videos, transcribe them, and optionally summarize and translate the transcriptions. It supports multiple translation engines, including local and API-based models.

## Features

- **Download and transcribe YouTube videos** using the local [Whisper base model](https://github.com/openai/whisper) 
  - Generate SRT files with timestamps
- **Translate transcriptions** into different languages:
  - **Local model**: [Opus-MT](https://github.com/Helsinki-NLP/Opus-MT) (no key required, runs locally)
  - **API-based model**: OpenAI's GPT (requires an API key, runs as a service)
- **Summarize transcriptions or translated text**:
  - **Local model**: [sshleifer/distilbart-cnn-12-6](https://huggingface.co/sshleifer/distilbart-cnn-12-6) (no key required, runs locally)
  - **API-based model**: OpenAI's GPT (requires an API key, runs as a service)
- **Interactive wizard**: The tool includes a CLI wizard that guides you through the transcription process using `click`, prompting for input like:
  - The YouTube video URL
  - Whether you want a summary of the transcription
  - Translation options, including language selection and translation model (Opus MT or OpenAI's GPT)
  - If OpenAI's GPT is chosen, the wizard will prompt for your OpenAI API key
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

