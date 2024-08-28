import os
import sys
import click
from rich.console import Console
from rich.progress import track
from rich import box
from rich.table import Table
from transcribe.youtube_downloader import download_youtube_video, extract_video_metadata, check_ffmpeg
from transcribe.transcriber import transcribe_video, transcribe_video_to_srt
from transcribe.translator import translate_text, OpusMTTranslator, GPTTranslator
from transcribe.summarizer import summarize_text
from transcribe.utils import change_file_extension

console = Console()

class TranscriptionWizard:
    def __init__(self):
        self.video_url = None
        self.summarize = False
        self.translate = None
        self.translator = "opus"
        self.openai_api_key = None

    def run(self):
        self.prompt_for_video_url()
        self.prompt_for_summarize()
        self.prompt_for_translation()

    def prompt_for_video_url(self):
        self.video_url = click.prompt("Please enter the YouTube video URL")

    def prompt_for_summarize(self):
        self.summarize = click.confirm("Do you want to summarize the transcription?", default=True)

    def prompt_for_translation(self):
        self.translate = click.prompt("Enter the language code to translate the transcription (or leave blank to skip translation)", default="", show_default=False)
        if self.translate:
            self.translator = click.prompt("Choose the translator", type=click.Choice(['opus', 'chatgpt']), default="opus")
            if self.translator == "chatgpt":
                self.openai_api_key = click.prompt("Enter your OpenAI API key", hide_input=True)


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        # No subcommand was provided, run the wizard by default
        wizard_instance = TranscriptionWizard()
        wizard_instance.run()
        ctx.invoke(transcribe_and_summarize,
                   video_url=wizard_instance.video_url,
                   summarize=wizard_instance.summarize,
                   translate=wizard_instance.translate,
                   translator=wizard_instance.translator,
                   openai_api_key=wizard_instance.openai_api_key)


@click.command()
@click.argument('video_url', required=False)
@click.option('--summarize', is_flag=True, default=False)
@click.option('--translate', default=None)
@click.option('--translator', default="opus")
@click.option('--openai-api-key', default=None)
def transcribe_and_summarize(video_url, summarize, translate, translator, openai_api_key):
    """
    Download, transcribe, and optionally summarize and/or translate a YouTube video.
    """

    if not video_url:
        console.print("[bold red]ERROR:[/bold red] Video URL is required.", file=sys.stderr)
        return

    console.print("[bold cyan]Starting the transcription process...[/bold cyan]")

    # Download the YouTube video
    console.print("[yellow]Downloading the YouTube video...[/yellow]")
    path = download_youtube_video(video_url)

    if path is None:
        console.print("[bold red]Video download failed; exiting.[/bold red]", file=sys.stderr)
        return
    console.print(f"[green]Video downloaded successfully to {path}[/green]")

    # Extract and save video metadata
    console.print("[yellow]Extracting video metadata...[/yellow]")
    yaml_file_name = extract_video_metadata(video_url, path)
    if yaml_file_name:
        console.print(f"[green]Metadata saved to {yaml_file_name}[/green]")

    # Transcribe the downloaded video with timestamps and save to SRT
    console.print("[yellow]Transcribing the video...[/yellow]")
    srt_text = transcribe_video_to_srt(path)
    if srt_text:
        srt_file_name = change_file_extension(path, '.srt')
        with open(srt_file_name, 'w') as file:
            file.write(srt_text)
        console.print(f"[green]SRT file saved to {srt_file_name}[/green]")

    # Transcribe without timestamps for further processing
    transcription = transcribe_video(path)

    if translate and transcription:
        console.print(f"[yellow]Translating the transcription to {translate}...[/yellow]")
        if translator == "chatgpt":
            if not openai_api_key:
                console.print("[bold red]ERROR: OpenAI API key is required when using chatgpt translator.[/bold red]", file=sys.stderr)
                return
            translator_instance = GPTTranslator(api_key=openai_api_key)
        else:
            translator_instance = OpusMTTranslator()

        translated_text = translate_text(transcription, translate, translator_instance)
        if translated_text:
            translated_file_name = change_file_extension(path, f'_{translate}.txt')
            with open(translated_file_name, 'w') as file:
                file.write(translated_text)
            console.print(f"[green]Translated transcription saved to {translated_file_name}[/green]")

            if summarize:
                console.print("[yellow]Summarizing the translated transcription...[/yellow]")
                translated_summary = summarize_text(translated_text)
                if translated_summary:
                    translated_summary_file_name = change_file_extension(path, f'_{translate}_summary.txt')
                    with open(translated_summary_file_name, 'w') as file:
                        file.write(translated_summary)
                    console.print(f"[green]Translated summary saved to {translated_summary_file_name}[/green]")

    if summarize and transcription:
        console.print("[yellow]Summarizing the transcription...[/yellow]")
        summary = summarize_text(transcription)
        if summary:
            summary_file_name = change_file_extension(path, '_summary.txt')
            with open(summary_file_name, 'w') as file:
                file.write(summary)
            console.print(f"[green]Summary saved to {summary_file_name}[/green]")


@click.command()
@click.argument('file_path')
def summarize_from_file(file_path):
    """
    Summarize text from a given .txt file.
    """
    if not os.path.isfile(file_path):
        console.print(f"[bold red]File {file_path} does not exist.[/bold red]")
        return

    with open(file_path, 'r') as file:
        text = file.read()

    console.print("[yellow]Summarizing the text...[/yellow]")
    # Summarize the text
    summary = summarize_text(text)
    if summary:
        summary_file_name = change_file_extension(file_path, '_summary.txt')
        with open(summary_file_name, 'w') as file:
            file.write(summary)
        console.print(f"[green]Summary saved to {summary_file_name}[/green]")


cli.add_command(transcribe_and_summarize)
cli.add_command(summarize_from_file)

if __name__ == "__main__":
    cli()
