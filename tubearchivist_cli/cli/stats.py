from tubearchivist_cli.cache.video import VideoTable
from tubearchivist_cli.cache.playlist import PlaylistTable
from tubearchivist_cli.cache.channel import ChannelTable
from tubearchivist_cli.cache.config import ConfigTable
import os
import json
from pathlib import Path


class Stats:
    """Display statistics about cached TubeArchivist data"""
    
    def __init__(self):
        self.video_table = VideoTable()
        self.playlist_table = PlaylistTable()
        self.channel_table = ChannelTable()
        self.config_table = ConfigTable()
    
    def overview(self):
        """Display overview statistics of all cached data"""
        print("TubeArchivist CLI - Cache Statistics")
        print("=" * 40)
        
        # Get counts
        video_count = self._get_video_count()
        channel_count = self._get_channel_count()
        playlist_count = self._get_playlist_count()
        
        print(f"Videos:    {video_count:,}")
        print(f"Channels:  {channel_count:,}")
        print(f"Playlists: {playlist_count:,}")
        
        # Database file info
        db_path = Path(self.video_table.database_path)
        if db_path.exists():
            db_size = db_path.stat().st_size
            print(f"\nDatabase size: {self._format_bytes(db_size)}")
            print(f"Database path: {db_path.absolute()}")
        
        # Configuration status
        config = self.config_table.get_config()
        if config:
            print(f"\nConfiguration: ✓ Configured")
            print(f"TubeArchivist URL: {config[0][0]}")
        else:
            print(f"\nConfiguration: ✗ Not configured")
    
    def videos(self):
        """Display detailed video statistics"""
        print("Video Statistics")
        print("=" * 20)
        
        video_count = self._get_video_count()
        if video_count == 0:
            print("No videos in cache.")
            return
        
        print(f"Total videos: {video_count:,}")
        
        # Get video stats
        stats = self._get_video_stats()
        if stats:
            print(f"Active videos: {stats.get('active', 0):,}")
            print(f"Inactive videos: {stats.get('inactive', 0):,}")
            
            if stats.get('total_size'):
                print(f"Total video size: {self._format_bytes(stats['total_size'])}")
                print(f"Average video size: {self._format_bytes(stats['avg_size'])}")
            
            if stats.get('latest_download'):
                print(f"Latest download: {stats['latest_download']}")
    
    def channels(self):
        """Display detailed channel statistics"""
        print("Channel Statistics")
        print("=" * 20)
        
        channel_count = self._get_channel_count()
        if channel_count == 0:
            print("No channels in cache.")
            return
        
        print(f"Total channels: {channel_count:,}")
        
        # Get channel stats
        stats = self._get_channel_stats()
        if stats:
            print(f"Subscribed channels: {stats.get('subscribed', 0):,}")
            print(f"Active channels: {stats.get('active', 0):,}")
    
    def playlists(self):
        """Display detailed playlist statistics"""
        print("Playlist Statistics")
        print("=" * 20)
        
        playlist_count = self._get_playlist_count()
        if playlist_count == 0:
            print("No playlists in cache.")
            return
        
        print(f"Total playlists: {playlist_count:,}")
        
        # Get playlist stats
        stats = self._get_playlist_stats()
        if stats:
            print(f"Active playlists: {stats.get('active', 0):,}")
            if stats.get('total_entries'):
                print(f"Total playlist entries: {stats['total_entries']:,}")
                print(f"Average entries per playlist: {stats['avg_entries']:.1f}")
    
    def database(self):
        """Display database file information and statistics"""
        print("Database Information")
        print("=" * 20)
        
        db_path = Path(self.video_table.database_path)
        if not db_path.exists():
            print("Database file not found.")
            return
        
        # File info
        db_size = db_path.stat().st_size
        print(f"File path: {db_path.absolute()}")
        print(f"File size: {self._format_bytes(db_size)}")
        print(f"Last modified: {self._format_timestamp(db_path.stat().st_mtime)}")
        
        # Table info
        tables = ['videos', 'channels', 'playlists', 'config']
        print(f"\nTables:")
        for table in tables:
            count = self._get_table_count(table)
            print(f"  {table}: {count:,} records")
    
    def _get_video_count(self):
        """Get total video count"""
        result = self.video_table.execute("SELECT COUNT(*) FROM videos")
        return result[0][0] if result else 0
    
    def _get_channel_count(self):
        """Get total channel count"""
        result = self.channel_table.execute("SELECT COUNT(*) FROM channels")
        return result[0][0] if result else 0
    
    def _get_playlist_count(self):
        """Get total playlist count"""
        result = self.playlist_table.execute("SELECT COUNT(*) FROM playlists")
        return result[0][0] if result else 0
    
    def _get_table_count(self, table_name):
        """Get count for any table"""
        try:
            result = self.video_table.execute(f"SELECT COUNT(*) FROM {table_name}")
            return result[0][0] if result else 0
        except:
            return 0
    
    def _get_video_stats(self):
        """Get detailed video statistics"""
        try:
            # Active/inactive counts
            active_result = self.video_table.execute("SELECT COUNT(*) FROM videos WHERE active = 1")
            inactive_result = self.video_table.execute("SELECT COUNT(*) FROM videos WHERE active = 0")
            
            # Size statistics
            size_result = self.video_table.execute(
                "SELECT SUM(media_size), AVG(media_size) FROM videos WHERE media_size IS NOT NULL AND media_size > 0"
            )
            
            # Latest download
            latest_result = self.video_table.execute(
                "SELECT MAX(date_downloaded) FROM videos WHERE date_downloaded IS NOT NULL"
            )
            
            stats = {
                'active': active_result[0][0] if active_result else 0,
                'inactive': inactive_result[0][0] if inactive_result else 0
            }
            
            if size_result and size_result[0][0]:
                stats['total_size'] = int(size_result[0][0])
                stats['avg_size'] = int(size_result[0][1]) if size_result[0][1] else 0
            
            if latest_result and latest_result[0][0]:
                stats['latest_download'] = self._format_timestamp(latest_result[0][0])
            
            return stats
        except:
            return {}
    
    def _get_channel_stats(self):
        """Get detailed channel statistics"""
        try:
            subscribed_result = self.channel_table.execute("SELECT COUNT(*) FROM channels WHERE channel_subscribed = 1")
            active_result = self.channel_table.execute("SELECT COUNT(*) FROM channels WHERE active = 1")
            
            return {
                'subscribed': subscribed_result[0][0] if subscribed_result else 0,
                'active': active_result[0][0] if active_result else 0
            }
        except:
            return {}
    
    def _get_playlist_stats(self):
        """Get detailed playlist statistics"""
        try:
            active_result = self.playlist_table.execute("SELECT COUNT(*) FROM playlists WHERE active = 1")
            
            # Count playlist entries
            entries_result = self.playlist_table.execute("SELECT playlist_entries FROM playlists WHERE playlist_entries IS NOT NULL")
            total_entries = 0
            playlist_count = 0
            
            if entries_result:
                for row in entries_result:
                    try:
                        entries = json.loads(row[0]) if row[0] else []
                        if isinstance(entries, list):
                            total_entries += len(entries)
                            playlist_count += 1
                    except:
                        continue
            
            stats = {
                'active': active_result[0][0] if active_result else 0,
                'total_entries': total_entries
            }
            
            if playlist_count > 0:
                stats['avg_entries'] = total_entries / playlist_count
            
            return stats
        except:
            return {}
    
    def _format_bytes(self, bytes_size):
        """Format bytes into human readable format"""
        if bytes_size == 0:
            return "0 B"
        
        units = ["B", "KB", "MB", "GB", "TB"]
        unit_index = 0
        size = float(bytes_size)
        
        while size >= 1024 and unit_index < len(units) - 1:
            size /= 1024
            unit_index += 1
        
        return f"{size:.1f} {units[unit_index]}"
    
    def _format_timestamp(self, timestamp):
        """Format timestamp into human readable format"""
        try:
            from datetime import datetime
            if isinstance(timestamp, str):
                return timestamp
            dt = datetime.fromtimestamp(timestamp)
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except:
            return str(timestamp)
