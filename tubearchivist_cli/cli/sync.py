from tubearchivist_cli.api.client import TubeArchivistAPI
from tubearchivist_cli.cache.video import VideoTable
from tubearchivist_cli.cache.playlist import PlaylistTable
from tubearchivist_cli.cache.channel import ChannelTable


class Sync:
    """Synchronize data from TubeArchivist API to local cache"""

    def __init__(self):
        self.client = TubeArchivistAPI()
        self.video_table = VideoTable()
        self.playlist_table = PlaylistTable()
        self.channel_table = ChannelTable()

    def videos(self):
        """Sync all videos from TubeArchivist to local cache"""
        print("Syncing videos...")
        self.video_table.clear_table()
        videos = self.client.get_all_videos()
        for video in videos:
            self.video_table.add_video(video)
        print(f"Synced {len(videos)} videos to local cache.")

    def playlists(self):
        """Sync all playlists from TubeArchivist to local cache"""
        print("Syncing playlists...")
        self.playlist_table.clear_table()
        playlists = self.client.get_all_playlists()
        for playlist in playlists:
            self.playlist_table.add_playlist(playlist)
        print(f"Synced {len(playlists)} playlists to local cache.")

    def channels(self):
        """Sync all channels from TubeArchivist to local cache"""
        print("Syncing channels...")
        self.channel_table.clear_table()
        channels = self.client.get_all_channels()
        for channel in channels:
            self.channel_table.add_channel(channel)
        print(f"Synced {len(channels)} channels to local cache.")

    def all(self):
        """Sync all data (videos, playlists, channels) from TubeArchivist"""
        print("Syncing all data (videos, playlists, channels)...")
        self.videos()
        self.playlists()
        self.channels()
        print("All data synced successfully.")
