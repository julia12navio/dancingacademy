from odoo import models, fields, api
import json
import requests

class AcademyClass(models.Model):
    _inherit = 'dancingacademy.class'

    youtube_playlist_url = fields.Char(string="YouTube Playlist URL")
    videos_list = fields.Text(string="Videos List", readonly=True, default="[]")  # Inicializado como lista vacía

    def fetch_youtube_videos(self):
        """Fetch videos from a YouTube playlist."""
        api_key = "AIzaSyBGzOTSs-XKVm-cAWzrnU_Zo0vg7L-n33w"  # Reemplaza con tu clave de API de YouTube
        if not self.youtube_playlist_url:
            raise ValueError("Please provide a YouTube Playlist URL.")

        playlist_id = self.youtube_playlist_url.split("list=")[1]
        url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={playlist_id}&key={api_key}&maxResults=10"

        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            videos = []
            for item in data.get('items', []):
                video_id = item['snippet']['resourceId']['videoId']
                video_title = item['snippet']['title']
                videos.append({
                    'title': video_title,
                    'url': f"https://www.youtube.com/watch?v={video_id}",
                    'thumbnail': f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
                })
            self.videos_list = json.dumps(videos)  # Serializa como JSON
        else:
            raise ValueError("Error fetching videos from YouTube API")



