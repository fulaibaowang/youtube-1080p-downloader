# youtube-1080p-downloader

- main.ipynb
script of using yt-dlp and ffmpeg with subprocess; downloading and merging video and audio

- youtube_download_merge.py
script of using yt-dlp as python library; it seems that by this way video and audio is automatically merged; so there are redundant code

- youtube_download.py
script of using yt-dlp as python library and convert to MOV format for IOS

usage:
```
python  youtube_download.py https://www.youtube.com/watch?v=5u94P5gOixI
```

requirements:
```
pip install yt-dlp
```

FFmpeg on win11: https://github.com/BtbN/FFmpeg-Builds/releases

To solve error message yt-dlp HTTP Error 403: Forbidden, often you need to upgrade yt-dlp.
```
pip install --upgrade yt-dlp
```