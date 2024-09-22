from setuptools import setup, find_packages

# Read the README.md content for the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="youtube-transcriber",
    version="0.1.0",
    author="Christian Pojoni",
    author_email="christian.pojoni@gmail.com",
    description="A Python CLI tool to download, transcribe, translate, and summarize YouTube videos",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/5queezer/youtube-transcriber",
    packages=find_packages(include=["transcribe", "transcribe.*"]),
    py_modules=["transcribe.main"],
    install_requires=[
        "langchain",
        "click",
        "openai-whisper",
        "transformers",
        "nltk",
        "PyYAML",
        "yt-dlp",
        "sentencepiece",
        "openai",
        "rich"
    ],
    entry_points={
        "console_scripts": [
            "youtube-transcriber=transcribe.main:cli"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
