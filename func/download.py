#!/bin/python3
import argparse
import os
from yt_dlp.utils import DownloadError
import yt_dlp

def download_video(url, output_dir, playlist=False):
    ydl_opts = {
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'format': 'bestvideo+bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
    }

    if playlist:
        ydl_opts.update({
            'extract_flat': True,
            'noplaylist': not playlist,
            'merge_output_format': 'mp4',
        })

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except DownloadError as e:
        if "Private video" in str(e):
            print(f"Skipping private video: {url}")
        else:
            raise

def download_audio(url, output_dir, playlist=False):
    ydl_opts = {
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'format': 'bestaudio/best',
        'extract_audio': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }],
    }

    if playlist:
        ydl_opts.update({
            'extract_flat': True,
            'noplaylist': not playlist,
        })

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except DownloadError as e:
        if "Private video" in str(e):
            print(f"Skipping private video: {url}")
        else:
            raise

def main():
    parser = argparse.ArgumentParser(description='YouTube Video Downloader using yt-dlp')
    parser.add_argument('-u', '--url', help='URL of the video or playlist')
    parser.add_argument('-f', '--file', help='File containing URLs or playlist URLs (default: "urls")')
    parser.add_argument('-o', '--outputdir', help='Output directory for downloaded videos (default: current directory)', default=os.getcwd())
    parser.add_argument('-p', '--playlist', help='Download as playlist in video format (default: True)', action='store_true')
    parser.add_argument('-v', '--video', help='Download in video format (default: False)', action='store_true')
    parser.add_argument('-a', '--audio', help='Download in audio format (default: False)', action='store_true')

    args = parser.parse_args()

    if args.file:
        try:
            with open(args.file, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        if args.video or args.playlist:
                            download_video(line, args.outputdir, args.playlist)
                        elif args.audio:
                            download_audio(line, args.outputdir, args.playlist)
                        else:
                            print("Please specify either -v/--video or -a/--audio.")
        except FileNotFoundError:
            print(f"File not found: {args.file}")
    elif args.url:
        if args.video or args.playlist:
            download_video(args.url, args.outputdir, args.playlist)
        elif args.audio:
            download_audio(args.url, args.outputdir, args.playlist)
        else:
            # Default to downloading in video format
            download_video(args.url, args.outputdir, args.playlist)
    else:
        print("Please provide either -u/--url or -f/--file.")

if __name__ == '__main__':
    main()

