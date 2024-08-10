from transformers import pipeline, MarianMTModel, MarianTokenizer


def translate_text(text, target_language):
    if text is None:
        print("No valid text provided; skipping translation.")
        return None

    model_name = f"Helsinki-NLP/opus-mt-en-{target_language}"
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    translation_pipeline = pipeline("translation", model=model, tokenizer=tokenizer)

    translated_text = translation_pipeline(text, max_length=512)[0]['translation_text']
    return translated_text
