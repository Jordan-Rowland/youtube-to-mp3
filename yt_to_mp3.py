import os
import subprocess

from pytube import YouTube

videos = [
    "https://www.youtube.com/watch?v=0ok0glLJsr4"
]


for index, video in enumerate(videos):
    print(f"Getting {index + 1} of {len(videos)}...")
    yt = YouTube(video)
    print(yt.title)
    stream = yt.streams.filter(only_audio=True).filter(subtype="mp4").first()
    print(stream)

    # Uncomment this to download
    stream.download()
    bash_command_1 = subprocess.Popen(
        ["ffmpeg", "-i", f"{yt.title}.mp4", "-vn", "-f", "wav", "-"],
        stdout=subprocess.PIPE,
    )
    bash_command_2 = subprocess.Popen(
        ["lame", "-V", "3", "-", f"{yt.title}.mp3"], stdin=bash_command_1.stdout
    )
    bash_command_1.stdout.close()
    output = bash_command_2.communicate()[0]
    os.remove(f"{yt.title}.mp4")
