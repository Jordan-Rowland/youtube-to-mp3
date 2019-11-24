import os
import re
import subprocess

from pytube import YouTube


videos = """

""".split()

for index, video in enumerate(videos, 1):
    print(f"{index} of {len(videos)}")
    try:
        yt = YouTube(video)
        print(yt.title)
        stream = yt.streams.filter(only_audio=True).filter(subtype="mp4").first()
        print(stream)
        print("Downloading video...")
        stream.download()
    except Exception:
        print("Could not get video")
        continue
    bash_command_1 = subprocess.Popen(
        ["ffmpeg", "-i", f"{yt.title}.mp4", "-vn", "-f", "wav", "-"],
        stdout=subprocess.PIPE,
    )
    bash_command_2 = subprocess.Popen(
        ["lame", "-V", "3", "-", f"{yt.title}.mp3"], stdin=bash_command_1.stdout
    )
    bash_command_1.stdout.close()
    print("Converting to MP3...")
    output = bash_command_2.communicate()[0]
    print("Deleting original video file...")
    os.remove(f"{yt.title}.mp4")


mp3s = [x for x in os.listdir() if x.endswith(".mp3")]

title_match = re.compile("([\w+\s+]+)-([\w+\s+]+)")

for file in mp3s:
    match = re.search(title_match, file)
    if match:
        new_title = (
            f"{match.groups()[0].strip()} - " \
            f"{match.groups()[1].strip()}.mp3"
            )
        if file != new_title:
            print(f"Renaming file {file} to:\n" \
                  f"{new_title}"
            )
            os.rename(file, new_title)
