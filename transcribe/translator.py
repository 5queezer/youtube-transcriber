import openai

from transformers import pipeline, MarianMTModel, MarianTokenizer
from abc import ABC, abstractmethod


class Translator(ABC):
    @abstractmethod
    def translate(self, text: str, target_language: str) -> str:
        pass


class OpusMTTranslator(Translator):
    def __init__(self):
        self.model_name_template = "Helsinki-NLP/opus-mt-en-{}"

    def translate(self, text: str, target_language: str) -> str:
        model_name = self.model_name_template.format(target_language)
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)
        translation_pipeline = pipeline("translation", model=model, tokenizer=tokenizer)

        translated_text = translation_pipeline(text, max_length=512)[0]['translation_text']
        return translated_text


class GPTTranslator(Translator):
    def __init__(self, api_key: str):
        openai.api_key = api_key

    def translate(self, text: str, target_language: str) -> str:
        prompt = f"Translate the following text to {target_language}:\n\n{text}"

        response = openai.Completion.create(
            engine="text-davinci-003",  # Use the appropriate model
            prompt=prompt,
            max_tokens=1000,
            n=1,
            stop=None,
            temperature=0.7,
        )

        translated_text = response.choices[0].text.strip()
        return translated_text


def translate_text(text: str, target_language: str, translator: Translator) -> str:
    return translator.translate(text, target_language)
