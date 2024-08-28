import nltk
from nltk.tokenize import sent_tokenize
from transformers import pipeline, AutoTokenizer


def summarize_text(text):
    if text is None:
        print("No valid text provided; skipping summarization.")
        return None

    # Download the NLTK 'punkt' data if not already available
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')

    # Download the NLTK 'punkt_tab' data if not already available
    try:
        nltk.data.find('tokenizers/punkt_tab')
    except LookupError:
        nltk.download('punkt_tab')

    model_name = "sshleifer/distilbart-cnn-12-6"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    summarizer = pipeline("summarization", model=model_name)

    max_input_length = tokenizer.model_max_length
    sentences = sent_tokenize(text)

    # Split text into chunks if it exceeds the model's maximum input length
    text_chunks = []
    current_chunk = []
    current_length = 0

    for sentence in sentences:
        sentence_length = len(tokenizer.encode(sentence))
        if current_length + sentence_length <= max_input_length:
            current_chunk.append(sentence)
            current_length += sentence_length
        else:
            text_chunks.append(' '.join(current_chunk))
            current_chunk = [sentence]
            current_length = sentence_length

    if current_chunk:
        text_chunks.append(' '.join(current_chunk))

    # Summarize each chunk and combine the summaries
    summaries = [summarizer(chunk, max_length=150, min_length=30, do_sample=False)[0]['summary_text'] for chunk in
                 text_chunks]
    final_summary = ' '.join(summaries)

    return final_summary
