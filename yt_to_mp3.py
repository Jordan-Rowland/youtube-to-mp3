#!/usr/bin/env python3.7

"""Download MP3 files from YouTube videos"""

import os
import re
import subprocess

from pytube import YouTube


def safe_name(name, safe_chars=" -()[]"):
    """Convert filename to safe characters so file renaming function works."""
    return "".join(
        [character for character in name if character.isalnum() or character in safe_chars]
    )


def download_yt_video(video_url):
    """Downloads audio-stream and returns the name of the saved file."""
    try:
        yt = YouTube(video_url)
        title = yt.title
        print(title)
        stream = yt.streams.filter(only_audio=True).filter(subtype="mp4").first()
        print(stream)
        print("Downloading video...")
        new_title = safe_name(title)
        stream.download(filename=new_title)
    except Exception:
        print("Could not get video")
    return new_title


def convert_mp4_to_mp3(title):
    """Invokes bash commands to convert file to MP3 and delete original video file."""
    bash_command_1 = subprocess.Popen(
        ["ffmpeg", "-i", f"{title}.mp4", "-vn", "-f", "wav", "-"], stdout=subprocess.PIPE,
    )
    bash_command_2 = subprocess.Popen(
        ["lame", "-V", "3", "-", f"{title}.mp3"], stdin=bash_command_1.stdout,
    )
    bash_command_1.stdout.close()
    print("Converting to MP3...")
    output = bash_command_2.communicate()[0]
    print("Deleting original video file...")
    os.remove(f"{title}.mp4")
    print(f"Saved as '{title}.mp3'")


def rename_mp3s(directory):
    """Collects mp3 files from a directory and normalizes the names if the fit (artist) - (title)
    format."""
    title_match = re.compile(r"([\w+\s+]+)-([\w+\s+]+)")
    files_renamed = 0
    mp3s = [file for file in directory if file.endswith(".mp3")]
    for file in mp3s:
        match = re.search(title_match, file)
        if match:
            new_title = f"{match.groups()[0].strip()} - " f"{match.groups()[1].strip()}.mp3"
            if file != new_title:
                print(f"Renaming file: \n{file}\n==> {new_title}")
                os.rename(file, new_title)
                files_renamed += 1
    print(f"Files renamed: {files_renamed}")


if __name__ == "__main__":
    VIDEOS = """

    """.split()

    for index, video in enumerate(VIDEOS, 1):
        print(f"{index} of {len(VIDEOS)}")
        video_filename = download_yt_video(video)
        convert_mp4_to_mp3(video_filename)

    rename_mp3s(os.listdir())
