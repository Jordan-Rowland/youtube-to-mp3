import os
import subprocess

from pytube import YouTube


videos = """
""".split()

for index, video in enumerate(videos):
    print(f"{index + 1} of {len(videos)}")
    try:
        yt = YouTube(video)
        print(yt.title)
        stream = yt.streams.filter(only_audio=True).filter(subtype="mp4").first()
        print(stream)

        # Uncomment this to download
        print("Downloading video...")
        stream.download()
    except Exception:
        print("Could not get video :(")
        cont
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
