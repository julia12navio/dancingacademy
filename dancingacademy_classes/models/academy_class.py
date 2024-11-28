from odoo import models, fields, api
import requests

class AcademyClass(models.Model):
    _inherit = 'dancingacademy.class'

    youtube_playlist_url = fields.Char(string="YouTube Playlist URL")
    youtube_videos = fields.One2many(
        'dancingacademy.youtube.video', 'class_id', string="YouTube Videos"
    )

    @api.onchange('youtube_playlist_url')
    def fetch_youtube_videos(self):
        """
        Fetch videos from YouTube playlist using the YouTube API.
        """
        if self.youtube_playlist_url:
            # Reemplaza con tu clave válida de API de YouTube
            api_key = "AIzaSyBGzOTSs-XKVm-cAWzrnU_Zo0vg7L-n33w"
            playlist_id = self.youtube_playlist_url.split("list=")[-1]
            url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId={playlist_id}&key={api_key}"
            
            response = requests.get(url)
            if response.status_code == 200:
                videos_data = response.json().get('items', [])
                
                # Borra los registros existentes
                self.youtube_videos = [(5, 0, 0)]
                
                # Añade nuevos registros
                video_records = []
                for video in videos_data:
                    video_snippet = video.get('snippet', {})
                    video_id = video_snippet.get('resourceId', {}).get('videoId')
                    if video_id:
                        video_records.append((0, 0, {
                            'video_title': video_snippet.get('title'),
                            'video_url': f"https://www.youtube.com/watch?v={video_id}",
                        }))
                
                self.youtube_videos = video_records


class YouTubeVideo(models.Model):
    _name = 'dancingacademy.youtube.video'
    _description = "YouTube Video"

    video_title = fields.Char(string="Video Title")
    video_url = fields.Char(string="Video URL")
    class_id = fields.Many2one('dancingacademy.class', string="Class")

    def play_video(self):
        """
        Retorna una acción para abrir el video en una nueva pestaña.
        """
        return {
            'type': 'ir.actions.act_url',
            'url': self.video_url,
            'target': 'new',  # Esto abrirá el video en una nueva pestaña
        }



