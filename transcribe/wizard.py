import click


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
