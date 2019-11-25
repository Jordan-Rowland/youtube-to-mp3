from flask import Flask, jsonify, send_file, send_from_directory
from youtube_downloader.yt_to_mp3 import download_yt_video, convert_mp4_to_mp3


app = Flask(__name__)

@app.route("/download/<video_id>")
def download(video_id):
    video_filename = download_yt_video(f"https://www.youtube.com/watch?v={video_id}")
    convert_mp4_to_mp3(
        video_filename,
        output_title="_".join(video_filename.split()))
    send_file(
        video_filename + ".mp3",
        as_attachment=True)
    return "<h1>Thank you for downloading</h1>"

if __name__ == '__main__':
   app.run()


