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

## Best Hardware to Run On

To run this tool efficiently, especially for larger videos or when using more resource-intensive models like Whisper and GPT, the following hardware is recommended:

### General Recommendations

- **GPU**: A recent NVIDIA GPU with CUDA support, such as the RTX 30 series or later, significantly accelerates transcription and summarization tasks.
  - For local Whisper-based transcriptions, a GPU will greatly speed up the process.
- **CPU**: For CPU-only environments, an Intel i7 (10th gen or higher) or AMD Ryzen 7 (4000 series or higher) is recommended for acceptable performance.
- **RAM**: At least 16 GB of RAM, with 32 GB or more preferred for handling longer videos and larger model workloads.
- **Disk Space**: Ensure you have enough free disk space to handle video downloads, transcription outputs, and temporary audio files. While the extracted audio files often only consume a few MB, larger video files may require more storage, so having a few GB free is recommended.
- **ffmpeg**: `ffmpeg` must be installed and accessible via the system's PATH.

### Apple Silicon (M1/M2)

- **Apple Silicon (M1/M2/M3)**: Apple Silicon offers great performance even without a dedicated GPU. The Whisper model, in particular, runs efficiently on the Neural Engine.
  - **Whisper**: Works well on Apple Silicon, especially when using the `coreml` version optimized for these processors.
  - **Translation & Summarization**: OpenAI API-based models (like GPT) run remotely, so performance is not hardware-dependent. For local translation (Opus MT) and summarization (DistilBART), the M1/M2 chip provides excellent performance for most tasks.
- **RAM**: 16 GB unified memory is generally sufficient for typical use, but for large videos or processing many tasks simultaneously, 32 GB is preferred.
- **Disk Space**: Similar to other setups, ensure a few GB of free space for video downloads and outputs.
- **ffmpeg**: Ensure `ffmpeg` is installed and accessible via PATH, as it's required for video processing.

## Installation

### Prerequisites

- Python 3.7+
- `ffmpeg` (Make sure `ffmpeg` is installed and accessible via your PATH)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/yourgithubrepo/youtube-transcriber-summarizer.git
cd youtube-transcriber-summarizer
```

2. Install the package:

```bash
python setup.py install
```

This will install all the required dependencies and make the CLI tool available for use.

## Usage

Once installed, you can use the CLI tool like this:

```bash
youtube-transcriber transcribe-and-summarize [OPTIONS] VIDEO_URL
```

### Options:
- `--summarize`: Summarize the transcription.
- `--translate TEXT`: Translate the transcription to the specified language (e.g., 'es' for Spanish).
- `--translator [opus|chatgpt]`: Choose the translator: 'opus' for Opus MT, 'chatgpt' for OpenAI GPT.
- `--openai-api-key TEXT`: Your OpenAI API key (required if using chatgpt).

### Example:

```bash
youtube-transcriber transcribe-and-summarize https://www.youtube.com/watch?v=example --summarize --translate es --translator opus
```

This will download the YouTube video, transcribe it, summarize the transcription, and translate it to Spanish using the Opus MT model.
