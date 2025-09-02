from tubearchivist_cli.cache.table import DatabaseTable
import json


class PlaylistTable(DatabaseTable):
    def __init__(self):
        super().__init__()
        self.database_name = "playlists"
        self.create_table()

    def create_table(self):
        query = f"""
        CREATE TABLE IF NOT EXISTS {self.database_name} (
            playlist_id TEXT PRIMARY KEY,
            playlist_name TEXT NOT NULL,
            playlist_description TEXT,
            playlist_channel TEXT,
            playlist_channel_id TEXT,
            playlist_thumbnail TEXT,
            playlist_last_refresh TEXT,
            playlist_entries TEXT,
            date_downloaded INTEGER,
            active BOOLEAN,
            _index TEXT,
            _score REAL
        )
        """
        self.execute(query)
        self.commit()

    def add_playlist(self, playlist_data):
        query = """
        INSERT OR REPLACE INTO playlists (
            playlist_id, playlist_name, playlist_description, playlist_channel, 
            playlist_channel_id, playlist_thumbnail, playlist_last_refresh, 
            playlist_entries, date_downloaded, active, _index, _score
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        # Extract and prepare data
        values = (
            playlist_data.get('playlist_id'),
            playlist_data.get('playlist_name'),
            playlist_data.get('playlist_description'),
            playlist_data.get('playlist_channel'),
            playlist_data.get('playlist_channel_id'),
            playlist_data.get('playlist_thumbnail'),
            playlist_data.get('playlist_last_refresh'),
            json.dumps(playlist_data.get('playlist_entries', [])),
            playlist_data.get('date_downloaded'),
            playlist_data.get('active'),
            playlist_data.get('_index'),
            playlist_data.get('_score')
        )

        self.execute(query, values)
        self.commit()
