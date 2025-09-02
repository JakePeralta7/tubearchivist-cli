from tubearchivist_cli.cache.table import DatabaseTable
import json


class ChannelTable(DatabaseTable):
    def __init__(self):
        super().__init__()
        self.database_name = "channels"
        self.create_table()

    def create_table(self):
        query = f"""
        CREATE TABLE IF NOT EXISTS {self.database_name} (
            channel_id TEXT PRIMARY KEY,
            channel_name TEXT NOT NULL,
            channel_banner_url TEXT,
            channel_thumb_url TEXT,
            channel_description TEXT,
            channel_last_refresh TEXT,
            channel_subscribed BOOLEAN,
            channel_overwrites TEXT,
            date_downloaded INTEGER,
            active BOOLEAN,
            _index TEXT,
            _score REAL
        )
        """
        self.execute(query)
        self.commit()

    def add_channel(self, channel_data):
        query = """
        INSERT OR REPLACE INTO channels (
            channel_id, channel_name, channel_banner_url, channel_thumb_url, 
            channel_description, channel_last_refresh, channel_subscribed, 
            channel_overwrites, date_downloaded, active, _index, _score
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        # Extract and prepare data
        values = (
            channel_data.get('channel_id'),
            channel_data.get('channel_name'),
            channel_data.get('channel_banner_url'),
            channel_data.get('channel_thumb_url'),
            channel_data.get('channel_description'),
            channel_data.get('channel_last_refresh'),
            channel_data.get('channel_subscribed'),
            json.dumps(channel_data.get('channel_overwrites', {})),
            channel_data.get('date_downloaded'),
            channel_data.get('active'),
            channel_data.get('_index'),
            channel_data.get('_score')
        )

        self.execute(query, values)
        self.commit()
