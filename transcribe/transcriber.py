import whisper
from rich.progress import Progress
from rich.console import Console

# Initialize the Rich console
console = Console()


def transcribe_video(path: str):
    if path is None:
        console.print("[bold red]No valid video path provided; skipping transcription.[/bold red]")
        return None

    model = whisper.load_model("base")

    # Transcribe the video with a progress bar
    console.print("[yellow]Transcribing video...[/yellow]")
    result = model.transcribe(path)

    # Calculate the total duration of the video
    total_duration = sum(segment['end'] - segment['start'] for segment in result['segments'])

    transcribed_text = []
    with Progress() as progress:
        task = progress.add_task("[green]Transcribing...", total=total_duration)

        for segment in result['segments']:
            transcribed_text.append(segment['text'])
            # Update the progress bar
            progress.update(task, advance=segment['end'] - segment['start'])

    console.print("[bold green]Transcription completed.[/bold green]")
    return ''.join(transcribed_text)


def transcribe_video_to_srt(path: str):
    if path is None:
        console.print("[bold red]No valid video path provided; skipping transcription to SRT.[/bold red]")
        return None

    model = whisper.load_model("base")

    # Transcribe the video with word timestamps
    console.print("[yellow]Transcribing video to SRT...[/yellow]")
    result = model.transcribe(path, word_timestamps=True)

    # Calculate the total duration of the video
    total_duration = sum(segment['end'] - segment['start'] for segment in result['segments'])

    srt_output = []
    with Progress() as progress:
        task = progress.add_task("[green]Transcribing to SRT...", total=total_duration)

        for i, segment in enumerate(result['segments']):
            start = segment['start']
            end = segment['end']
            text = segment['text'].strip()

            # Convert time to SRT format
            start_time = convert_seconds_to_srt_timestamp(start)
            end_time = convert_seconds_to_srt_timestamp(end)

            srt_output.append(f"{i + 1}\n{start_time} --> {end_time}\n{text}\n")

            # Update the progress bar
            progress.update(task, advance=end - start)

    console.print("[bold green]SRT transcription completed.[/bold green]")
    srt_text = '\n'.join(srt_output)
    return srt_text


def convert_seconds_to_srt_timestamp(seconds):
    milliseconds = int((seconds % 1) * 1000)
    seconds = int(seconds)
    minutes = int(seconds // 60)
    hours = int(minutes // 60)
    seconds = int(seconds % 60)
    minutes = int(minutes % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"
