import webbrowser
import sys
from googleapiclient.discovery import build

import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="config\.env")

API_KEY = os.getenv("YOUTUBE_API_KEY")

def main(query):
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    search_response = youtube.search().list(
        q=query,
        part='snippet',
        maxResults=1
    ).execute()

    if search_response['items']:
        video = search_response['items'][0]
        video_id = video['id']['videoId']
        video_title = video['snippet']['title']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        print(f"Opening video: {video_title}")
        print(f"URL: {video_url}")
        webbrowser.open(video_url)
        print(f"Playing video: {video_title} on youtube...; include no extra information")
    else:
        print("No video found.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        main(query)
    else:
        print("Please provide a search query.")