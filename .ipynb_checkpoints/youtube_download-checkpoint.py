from yt_dlp import YoutubeDL
import sys

def download_to_mov_remux(url):
    """
    Download best 1080p video + best audio, then attempt to remux into .mov
    WITHOUT re-encoding.
    This only works if original codecs are MOV-compatible (e.g. h264 + aac).
    """
    ydl_opts = {
        'format': 'bv[height=1080]+ba/b[height=1080]',
        'outtmpl': '%(title)s.%(ext)s',
        'postprocessors': [
            {
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mov'
            }
        ],
        'cookiefile': 'cookies.txt'  # If needed for restricted videos
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])  # passes a list of URLs


if __name__ == '__main__':
    youtube_url = sys.argv[1] if len(sys.argv) > 1 else input("Enter YouTube URL: ")
    download_to_mov_remux(youtube_url)
