from tubearchivist_cli.cache.video import VideoTable
from tubearchivist_cli.cache.playlist import PlaylistTable
from tubearchivist_cli.cache.channel import ChannelTable
import json


class Search:
    """Search through cached TubeArchivist data"""

    def __init__(self):
        self.video_table = VideoTable()
        self.playlist_table = PlaylistTable()
        self.channel_table = ChannelTable()

    def videos(self, query=None):
        """Search videos by title, description, or tags"""
        if not query:
            print("Error: Search query is required")
            print("Usage: python tube.py search videos <query>")
            return

        print(f"Searching videos for: '{query}'")
        
        # Search in title, description, and tags
        sql_query = """
        SELECT youtube_id, title, published, channel, tags
        FROM videos 
        WHERE title LIKE ? OR description LIKE ? OR tags LIKE ?
        ORDER BY title
        """
        
        search_term = f"%{query}%"
        results = self.video_table.execute(sql_query, (search_term, search_term, search_term))
        
        if not results:
            print("No videos found matching your search.")
            return

        print(f"Found {len(results)} video(s):")
        print("-" * 80)
        
        for video_id, title, published, channel_json, tags_json in results:
            # Parse channel info
            channel_name = "Unknown Channel"
            try:
                if channel_json:
                    channel_data = json.loads(channel_json)
                    channel_name = channel_data.get('channel_name', 'Unknown Channel')
            except:
                pass
            
            # Parse tags
            tags = []
            try:
                if tags_json:
                    tags = json.loads(tags_json)
            except:
                pass
            
            print(f"Title: {title}")
            print(f"ID: {video_id}")
            print(f"Channel: {channel_name}")
            print(f"Published: {published or 'Unknown'}")
            if tags:
                print(f"Tags: {', '.join(tags[:5])}")  # Show first 5 tags
            print("-" * 80)

    def channels(self, query=None):
        """Search channels by name or description"""
        if not query:
            print("Error: Search query is required")
            print("Usage: python tube.py search channels <query>")
            return

        print(f"Searching channels for: '{query}'")
        
        sql_query = """
        SELECT channel_id, channel_name, channel_description, channel_subscribed, active
        FROM channels 
        WHERE channel_name LIKE ? OR channel_description LIKE ?
        ORDER BY channel_name
        """
        
        search_term = f"%{query}%"
        results = self.channel_table.execute(sql_query, (search_term, search_term))
        
        if not results:
            print("No channels found matching your search.")
            return

        print(f"Found {len(results)} channel(s):")
        print("-" * 80)
        
        for channel_id, name, description, subscribed, active in results:
            status_indicators = []
            if subscribed:
                status_indicators.append("📺 Subscribed")
            if active:
                status_indicators.append("✅ Active")
            else:
                status_indicators.append("❌ Inactive")
            
            print(f"Name: {name}")
            print(f"ID: {channel_id}")
            if status_indicators:
                print(f"Status: {' | '.join(status_indicators)}")
            if description:
                # Truncate long descriptions
                desc = description[:200] + "..." if len(description) > 200 else description
                print(f"Description: {desc}")
            print("-" * 80)

    def playlists(self, query=None):
        """Search playlists by name or description"""
        if not query:
            print("Error: Search query is required")
            print("Usage: python tube.py search playlists <query>")
            return

        print(f"Searching playlists for: '{query}'")
        
        sql_query = """
        SELECT playlist_id, playlist_name, playlist_description, playlist_channel, playlist_entries, active
        FROM playlists 
        WHERE playlist_name LIKE ? OR playlist_description LIKE ?
        ORDER BY playlist_name
        """
        
        search_term = f"%{query}%"
        results = self.playlist_table.execute(sql_query, (search_term, search_term))
        
        if not results:
            print("No playlists found matching your search.")
            return

        print(f"Found {len(results)} playlist(s):")
        print("-" * 80)
        
        for playlist_id, name, description, channel, entries_json, active in results:
            # Count entries
            entry_count = 0
            try:
                if entries_json:
                    entries = json.loads(entries_json)
                    if isinstance(entries, list):
                        entry_count = len(entries)
            except:
                pass
            
            status = "✅ Active" if active else "❌ Inactive"
            
            print(f"Name: {name}")
            print(f"ID: {playlist_id}")
            print(f"Channel: {channel or 'Unknown'}")
            print(f"Entries: {entry_count}")
            print(f"Status: {status}")
            if description:
                # Truncate long descriptions
                desc = description[:200] + "..." if len(description) > 200 else description
                print(f"Description: {desc}")
            print("-" * 80)

    def all(self, query=None):
        """Search across all content types (videos, channels, playlists)"""
        if not query:
            print("Error: Search query is required")
            print("Usage: python tube.py search all <query>")
            return

        print(f"Searching all content for: '{query}'")
        print("=" * 80)
        
        # Search videos
        print("\n📹 VIDEOS:")
        video_results = self._get_video_search_results(query)
        if video_results:
            print(f"Found {len(video_results)} video(s):")
            for i, (video_id, title, channel_name) in enumerate(video_results[:5], 1):
                print(f"  {i}. {title} - {channel_name} ({video_id})")
            if len(video_results) > 5:
                print(f"  ... and {len(video_results) - 5} more")
        else:
            print("  No videos found")
        
        # Search channels
        print("\n📺 CHANNELS:")
        channel_results = self._get_channel_search_results(query)
        if channel_results:
            print(f"Found {len(channel_results)} channel(s):")
            for i, (channel_id, name, subscribed) in enumerate(channel_results[:5], 1):
                sub_status = " (Subscribed)" if subscribed else ""
                print(f"  {i}. {name}{sub_status} ({channel_id})")
            if len(channel_results) > 5:
                print(f"  ... and {len(channel_results) - 5} more")
        else:
            print("  No channels found")
        
        # Search playlists
        print("\n📋 PLAYLISTS:")
        playlist_results = self._get_playlist_search_results(query)
        if playlist_results:
            print(f"Found {len(playlist_results)} playlist(s):")
            for i, (playlist_id, name, entry_count) in enumerate(playlist_results[:5], 1):
                print(f"  {i}. {name} ({entry_count} entries) ({playlist_id})")
            if len(playlist_results) > 5:
                print(f"  ... and {len(playlist_results) - 5} more")
        else:
            print("  No playlists found")

        total_results = len(video_results) + len(channel_results) + len(playlist_results)
        print(f"\nTotal results: {total_results}")
        if total_results > 0:
            print("Use specific search commands for detailed results:")
            print(f"  python tube.py search videos '{query}'")
            print(f"  python tube.py search channels '{query}'")
            print(f"  python tube.py search playlists '{query}'")

    def _get_video_search_results(self, query):
        """Helper method to get video search results"""
        sql_query = """
        SELECT youtube_id, title, channel
        FROM videos 
        WHERE title LIKE ? OR description LIKE ? OR tags LIKE ?
        ORDER BY title
        LIMIT 50
        """
        
        search_term = f"%{query}%"
        results = self.video_table.execute(sql_query, (search_term, search_term, search_term))
        
        processed_results = []
        for video_id, title, channel_json in results:
            channel_name = "Unknown Channel"
            try:
                if channel_json:
                    channel_data = json.loads(channel_json)
                    channel_name = channel_data.get('channel_name', 'Unknown Channel')
            except:
                pass
            processed_results.append((video_id, title, channel_name))
        
        return processed_results

    def _get_channel_search_results(self, query):
        """Helper method to get channel search results"""
        sql_query = """
        SELECT channel_id, channel_name, channel_subscribed
        FROM channels 
        WHERE channel_name LIKE ? OR channel_description LIKE ?
        ORDER BY channel_name
        LIMIT 20
        """
        
        search_term = f"%{query}%"
        return self.channel_table.execute(sql_query, (search_term, search_term))

    def _get_playlist_search_results(self, query):
        """Helper method to get playlist search results"""
        sql_query = """
        SELECT playlist_id, playlist_name, playlist_entries
        FROM playlists 
        WHERE playlist_name LIKE ? OR playlist_description LIKE ?
        ORDER BY playlist_name
        LIMIT 20
        """
        
        search_term = f"%{query}%"
        results = self.playlist_table.execute(sql_query, (search_term, search_term))
        
        processed_results = []
        for playlist_id, name, entries_json in results:
            entry_count = 0
            try:
                if entries_json:
                    entries = json.loads(entries_json)
                    if isinstance(entries, list):
                        entry_count = len(entries)
            except:
                pass
            processed_results.append((playlist_id, name, entry_count))
        
        return processed_results
