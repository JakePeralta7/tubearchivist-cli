from tubearchivist_cli.api.client import TubeArchivistAPI
from tubearchivist_cli.cache.video import VideoTable
from tubearchivist_cli.cache.playlist import PlaylistTable
from tubearchivist_cli.cache.channel import ChannelTable


class Sync:
    def __init__(self):
        self.client = TubeArchivistAPI()
        self.video_table = VideoTable()
        self.playlist_table = PlaylistTable()
        self.channel_table = ChannelTable()

    def video(self):
        print("Syncing videos...")
        self.video_table.clear_table()
        videos = self.client.get_all_videos()
        for video in videos:
            self.video_table.add_video(video)
        print(f"Synced {len(videos)} videos to local cache.")

    def playlist(self):
        print("Syncing playlists...")
        self.playlist_table.clear_table()
        playlists = self.client.get_all_playlists()
        for playlist in playlists:
            self.playlist_table.add_playlist(playlist)
        print(f"Synced {len(playlists)} playlists to local cache.")

    def channel(self):
        print("Syncing channels...")
        self.channel_table.clear_table()
        channels = self.client.get_all_channels()
        for channel in channels:
            self.channel_table.add_channel(channel)
        print(f"Synced {len(channels)} channels to local cache.")

    def all(self):
        print("Syncing all data (videos, playlists, channels)...")
        self.video()
        self.playlist()
        self.channel()
        print("All data synced successfully.")
