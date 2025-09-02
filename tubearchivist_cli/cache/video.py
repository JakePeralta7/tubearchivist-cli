from tubearchivist_cli.cache.table import DatabaseTable
import json


class VideoTable(DatabaseTable):
    def __init__(self):
        super().__init__()
        self.database_name = "videos"
        self.create_table()

    def create_table(self):
        query = f"""
        CREATE TABLE IF NOT EXISTS {self.database_name} (
            youtube_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            published TEXT,
            date_downloaded INTEGER,
            active BOOLEAN,
            vid_last_refresh TEXT,
            vid_thumb_url TEXT,
            vid_type TEXT,
            media_url TEXT,
            media_size INTEGER,
            comment_count INTEGER,
            category TEXT,
            tags TEXT,
            channel TEXT,
            player TEXT,
            playlist TEXT,
            sponsorblock TEXT,
            stats TEXT,
            streams TEXT,
            subtitles TEXT,
            _index TEXT,
            _score REAL
        )
        """
        self.execute(query)
        self.commit()

    def add_video(self, video_data):
        query = """
        INSERT OR REPLACE INTO videos (
            youtube_id, title, description, published, date_downloaded, active, 
            vid_last_refresh, vid_thumb_url, vid_type, media_url, media_size, 
            comment_count, category, tags, channel, player, playlist, 
            sponsorblock, stats, streams, subtitles, _index, _score
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        # Extract and prepare data
        values = (
            video_data.get('youtube_id'),
            video_data.get('title'),
            video_data.get('description'),
            video_data.get('published'),
            video_data.get('date_downloaded'),
            video_data.get('active'),
            video_data.get('vid_last_refresh'),
            video_data.get('vid_thumb_url'),
            video_data.get('vid_type'),
            video_data.get('media_url'),
            video_data.get('media_size'),
            video_data.get('comment_count'),
            json.dumps(video_data.get('category', [])),
            json.dumps(video_data.get('tags', [])),
            json.dumps(video_data.get('channel', {})),
            json.dumps(video_data.get('player', {})),
            json.dumps(video_data.get('playlist', [])),
            json.dumps(video_data.get('sponsorblock')),
            json.dumps(video_data.get('stats', {})),
            json.dumps(video_data.get('streams', [])),
            json.dumps(video_data.get('subtitles', [])),
            video_data.get('_index'),
            video_data.get('_score')
        )

        self.execute(query, values)
        self.commit()
