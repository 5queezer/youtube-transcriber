import whisper


def transcribe_video(path: str):
    if path is None:
        print("No valid video path provided; skipping transcription.")
        return None

    model = whisper.load_model("base")
    result = model.transcribe(path)
    return result["text"]


def transcribe_video_to_srt(path: str):
    if path is None:
        print("No valid video path provided; skipping transcription to SRT.")
        return None

    model = whisper.load_model("base")
    result = model.transcribe(path, word_timestamps=True)

    srt_output = []
    for i, segment in enumerate(result['segments']):
        start = segment['start']
        end = segment['end']
        text = segment['text'].strip()

        # Convert time to SRT format
        start_time = convert_seconds_to_srt_timestamp(start)
        end_time = convert_seconds_to_srt_timestamp(end)

        srt_output.append(f"{i + 1}\n{start_time} --> {end_time}\n{text}\n")

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
