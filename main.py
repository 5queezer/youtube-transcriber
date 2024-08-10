import os
import click
from transcribe.youtube_downloader import download_youtube_video, extract_video_metadata, check_ffmpeg
from transcribe.transcriber import transcribe_video, transcribe_video_to_srt
from transcribe.translator import translate_text
from transcribe.summarizer import summarize_text
from transcribe.utils import change_file_extension


@click.group()
def cli():
    pass


@click.command()
@click.argument('video_url')
@click.option('--summarize', is_flag=True, help="Summarize the transcription")
@click.option('--translate', default=None, help="Translate the transcription to the specified language (e.g., 'es' for Spanish)")
def transcribe_and_summarize(video_url, summarize, translate):
    """
    Download, transcribe, and optionally summarize and/or translate a YouTube video.
    """

    # Download the YouTube video
    path = download_youtube_video(video_url)

    if path is None:
        print("Video download failed; exiting.")
        return

    # Extract and save video metadata
    yaml_file_name = extract_video_metadata(video_url, path)
    if yaml_file_name:
        print(f"Metadata saved to {yaml_file_name}")

    # Transcribe the downloaded video with timestamps and save to SRT
    srt_text = transcribe_video_to_srt(path)
    if srt_text:
        srt_file_name = change_file_extension(path, '.srt')
        with open(srt_file_name, 'w') as file:
            file.write(srt_text)
        print(f"SRT file saved to {srt_file_name}")

    # Transcribe without timestamps for further processing
    transcription = transcribe_video(path)

    if translate and transcription:
        # Translate the transcription
        translated_text = translate_text(transcription, translate)
        if translated_text:
            translated_file_name = change_file_extension(path, f'_{translate}.txt')
            with open(translated_file_name, 'w') as file:
                file.write(translated_text)
            print(f"Translated transcription saved to {translated_file_name}")

            if summarize:
                # Summarize the translated transcription
                translated_summary = summarize_text(translated_text)
                if translated_summary:
                    translated_summary_file_name = change_file_extension(path, f'_{translate}_summary.txt')
                    with open(translated_summary_file_name, 'w') as file:
                        file.write(translated_summary)
                    print(f"Translated summary saved to {translated_summary_file_name}")

    if summarize and transcription:
        # Summarize the original transcription
        summary = summarize_text(transcription)
        if summary:
            summary_file_name = change_file_extension(path, '_summary.txt')
            with open(summary_file_name, 'w') as file:
                file.write(summary)
            print(f"Summary: {summary}")


@click.command()
@click.argument('file_path')
def summarize_from_file(file_path):
    """
    Summarize text from a given .txt file.
    """
    if not os.path.isfile(file_path):
        print(f"File {file_path} does not exist.")
        return

    with open(file_path, 'r') as file:
        text = file.read()

    # Summarize the text
    summary = summarize_text(text)
    if summary:
        summary_file_name = change_file_extension(file_path, '_summary.txt')
        with open(summary_file_name, 'w') as file:
            file.write(summary)
        print(f"Summary: {summary}")


cli.add_command(transcribe_and_summarize)
cli.add_command(summarize_from_file)

if __name__ == "__main__":
    cli()
