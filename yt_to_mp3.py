#!/usr/bin/env python3.7

"""Download MP3 files from YouTube videos"""

import os
import re
import subprocess

from pytube import YouTube


def safe_name(name, safe_chars=" -()[]\"'!"):
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
        print("Downloading video...")
        # new_title = "_".join(safe_name(title).split())
        new_title = safe_name(title)
        stream.download(filename=new_title)
    except Exception:
        return False
    return new_title


def convert_mp4_to_mp3(title, output_title=None):
    """Invokes bash commands to convert file to MP3 and delete original video file."""
    if not output_title:
        output_title = title
    try:
        bash_command_1 = subprocess.Popen(
            ["ffmpeg", "-i", f"{title}.mp4", "-vn", "-f", "wav", "-"], stdout=subprocess.PIPE,
        )
        bash_command_2 = subprocess.Popen(
            ["lame", "-V", "3", "-", f"{output_title}.mp3"], stdin=bash_command_1.stdout,
        )
        bash_command_1.stdout.close()
        print("Converting to MP3...")
        output = bash_command_2.communicate()[0]
        print("Deleting original video file...")
        os.remove(f"{title}.mp4")
        print(f"Saved as '{output_title}.mp3'")
        return True
    except Exception:
        print("Could not convert to mp3.")
        return False


def rename_mp3s(directory, ask_confirmation=False):
    """Collects mp3 files from a directory and normalizes the names if they fit (artist) - (title)
    format. Optional argument to ask for confirmation for renaming."""
    title_match = re.compile(r"([\w+\s+]+)-([\w\s'\",]+)")
    files_renamed = 0
    mp3s = [file for file in directory if file.endswith(".mp3")]
    for file in mp3s:
        match = re.search(title_match, file)
        if not match:
            continue
        artist = match.groups()[0].strip()
        title = match.groups()[1].strip()
        new_title = f"{artist} - {title}.mp3"
        if file == new_title or new_title in mp3s:
            continue
        if ask_confirmation:
            print(f"{file} ==> {new_title}")
            confirm_rename = input("Rename? ['y' to confirm]: ")
            confirmed = confirm_rename.lower() in ["y", "yes"]
            if not confirmed:
                print("File unchanged")
                continue
        os.rename(file, new_title)
        print(f"Renaming file: \n{file}\n==> {new_title}\n")
        files_renamed += 1
    print(f"Files renamed: {files_renamed}")


if __name__ == "__main__":
    VIDEOS = """

    """.split()

    # for index, video in enumerate(VIDEOS, 1):
    #     print(f"{index} of {len(VIDEOS)}")
    #     video_filename = download_yt_video(video)
    #     if not video_filename:
    #         print("Could not get file")
    #     convert_mp4_to_mp3(video_filename)

    rename_mp3s(os.listdir())
