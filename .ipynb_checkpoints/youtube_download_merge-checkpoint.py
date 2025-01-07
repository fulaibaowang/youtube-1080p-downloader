import subprocess
import sys
import os

# pip install yt-dlp
from yt_dlp import YoutubeDL

def download_and_convert_youtube(url):
    """
    Downloads 1080p video + audio from YouTube via yt-dlp,
    then merges & converts them to a .mov file using ffmpeg (H.264 + AAC).
    """
    # 1) Configure yt-dlp options
    ydl_opts = {
        # "bv[height=1080]+ba" = best video at 1080p + best audio
        # "/b[height=1080]"    = fallback if that exact combo is not found
        'format': 'bv[height=1080]+ba/b[height=1080]',
        
        # If the YouTube video is age/region restricted,
        # you might need cookies for authentication:
        'cookiefile': 'cookies.txt',

        # Save files as "<video_title>.<ext>"
        'outtmpl': '%(title)s.%(ext)s',
    }

    # 2) Download with yt-dlp
    with YoutubeDL(ydl_opts) as ydl:
        print("Downloading video and audio streams...")
        info = ydl.extract_info(url, download=True)
    
    # 3) Identify the downloaded video & audio files
    #    If yt-dlp downloads separate streams, info["requested_downloads"]
    #    typically contains two items: one video-only and one audio-only.
    video_file_path = None
    audio_file_path = None

    requested_downloads = info.get("requested_downloads", [])
    for d in requested_downloads:
        # If it's video-only, "acodec" is "none"; audio-only => "vcodec" is "none"
        if d.get("acodec") == "none":
            video_file_path = d.get("filepath")
        elif d.get("vcodec") == "none":
            audio_file_path = d.get("filepath")

    # If we didn't get separate streams, yt-dlp might have merged them automatically
    # or only a single file was needed. In that case, there's nothing to merge.
    if not video_file_path or not audio_file_path:
        print("It seems yt-dlp did not produce separate audio/video files.")
        print("The final file might already be merged, or no 1080p is available.")
        return

    print(f"Video path: {video_file_path}")
    print(f"Audio path: {audio_file_path}")

    # 4) Create a .mov file name based on the video title
    #    The top-level "info" usually has a "title" key.
    #    On Windows, we replace slashes to avoid invalid filenames.
    title = info.get("title", "output").replace("/", "_").replace("\\", "_")
    mov_file_name = f"{title}.mov"

    # 5) Merge & re-encode to .mov with ffmpeg (H.264 + AAC)
    ffmpeg_cmd = [
        "ffmpeg",
        "-y",  # overwrite without asking
        "-i", video_file_path,
        "-i", audio_file_path,
        "-c:v", "libx264",      # Encode video as H.264
        "-c:a", "aac",          # Encode audio as AAC
        "-strict", "experimental",
        mov_file_name
    ]
    print("Merging & converting to .mov with ffmpeg...")
    subprocess.run(ffmpeg_cmd, check=True)

    print(f"Finished! Output file: {mov_file_name}")


if __name__ == "__main__":
    """
    Example usage:
      python download_and_convert.py  <YouTube-URL>
    or just run it and paste the URL when prompted.
    """
    if len(sys.argv) > 1:
        youtube_url = sys.argv[1]
    else:
        youtube_url = input("Enter YouTube URL: ").strip()
    
    download_and_convert_youtube(youtube_url)
