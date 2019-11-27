"""Endpoint for API access."""

from flask import Flask, jsonify, send_file
from yt_to_mp3 import download_yt_video, convert_mp4_to_mp3


APP = Flask(__name__)


@APP.route("/download/<video_id>")
def download(video_id):
    """Download video via cURL command or other API methods."""
    video_filename = download_yt_video(f"https://www.youtube.com/watch?v={video_id}")
    if not video_filename:
        return jsonify(error="Could not download from YouTube.")
    print(video_filename)
    converted = convert_mp4_to_mp3(video_filename)
    if not converted:
        return jsonify(error="Could not convert to mp3.")
    send_file(video_filename + ".mp3", as_attachment=True)
    return jsonify(message=f"File saved as '{video_filename}.mp3'")


if __name__ == "__main__":
    APP.run()
