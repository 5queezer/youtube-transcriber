import os
import re
from pathlib import Path
from yt_dlp import YoutubeDL
import yaml
from datetime import datetime
import shutil
from .utils import change_file_extension


def check_ffmpeg():
    """Check if ffmpeg is installed and accessible."""
    ffmpeg_path = "/usr/local/bin"
    os.environ["PATH"] += os.pathsep + ffmpeg_path

    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path is None:
        print("ERROR: ffmpeg is not installed or not found in the system PATH.")
        print("Please install ffmpeg or provide the correct path.")
        exit(1)
    else:
        print(f"ffmpeg is installed and accessible at {ffmpeg_path}.")
    return ffmpeg_path


def sanitize_title(title):
    """Sanitize a string to be used as a safe filename."""
    sanitized_title = re.sub(r'[^a-zA-Z0-9-_]+', '_', title)
    sanitized_title = sanitized_title.strip('_')
    sanitized_title = Path(sanitized_title).stem
    return sanitized_title


def download_youtube_video(video_url):
    ffmpeg_path = check_ffmpeg()

    # Extract video information to get the title
    ydl_opts_info = {
        'format': 'bestaudio/best',
        'ffmpeg_location': ffmpeg_path,
        'noplaylist': True,
    }

    with YoutubeDL(ydl_opts_info) as ydl:
        info_dict = ydl.extract_info(video_url, download=False)
        video_title = sanitize_title(info_dict.get('title', 'downloaded_video'))

    # Set the output template to use the sanitized video title
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'aac',
            'preferredquality': '192',
        }],
        'outtmpl': f'{video_title}.%(ext)s',
        'ffmpeg_location': ffmpeg_path,
        'keepvideo': True
    }

    with YoutubeDL(ydl_opts) as ydl:
        assert ydl.download([video_url]) == 0
        return ydl.prepare_filename(info_dict)


def extract_video_metadata(video_url, download_path):
    if download_path is None:
        print("No valid video path provided; skipping metadata extraction.")
        return None

    ydl_opts = {
        'skip_download': True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=False)

    metadata = {
        "title": info_dict.get('title'),
        "creator": info_dict.get('uploader'),
        "publish_date": info_dict.get('upload_date'),
        "description": info_dict.get('description'),
        "tags": info_dict.get('tags'),
        "views": info_dict.get('view_count'),
        "rating": info_dict.get('average_rating'),
        "length_seconds": info_dict.get('duration'),
        "video_url": video_url,
        "download_date": datetime.now(),
    }

    yaml_file_name = change_file_extension(download_path, '.yaml')
    with open(yaml_file_name, 'w') as yaml_file:
        yaml.dump(metadata, yaml_file, default_flow_style=False)
    return yaml_file_name
