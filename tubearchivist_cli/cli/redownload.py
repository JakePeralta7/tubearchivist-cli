from tubearchivist_cli.api.client import TubeArchivistAPI
from tubearchivist_cli.cache.video import VideoTable
import json
import time


class Redownload:
    """Redownload videos based on resolution or other criteria"""

    def __init__(self):
        self.client = TubeArchivistAPI()
        self.video_table = VideoTable()

    def resolution(self, target_resolution):
        """Redownload all videos with the specified resolution"""
        if not target_resolution:
            print("Error: Resolution argument is required")
            print("Usage: python tube.py redownload resolution <resolution>")
            print("Example: python tube.py redownload resolution 360")
            return

        print(f"Searching for videos with {target_resolution}p resolution...")
        
        # Query videos with the target resolution
        videos = self._get_videos_by_resolution(target_resolution)
        
        if not videos:
            print(f"No videos found with {target_resolution}p resolution.")
            return

        print(f"Found {len(videos)} videos with {target_resolution}p resolution.")
        
        # Confirm before proceeding
        confirm = input(f"Do you want to redownload all {len(videos)} videos? (y/N): ")
        if confirm.lower() not in ['y', 'yes']:
            print("Operation cancelled.")
            return

        # Redownload each video
        success_count = 0
        failed_count = 0
        
        for i, video in enumerate(videos, 1):
            video_id = video[0]
            title = video[1]
            
            print(f"[{i}/{len(videos)}] Redownloading: {title} ({video_id})")
            
            if self.client.redownload_video(video_id):
                success_count += 1
            else:
                failed_count += 1
                print(f"  ❌ Failed to queue {video_id}")
            
            # Add a small delay to avoid overwhelming the API
            time.sleep(0.5)

        print(f"\nRedownload Summary:")
        print(f"✅ Successfully queued: {success_count}")
        print(f"❌ Failed: {failed_count}")
        print(f"📥 Total videos processed: {len(videos)}")

    def _get_videos_by_resolution(self, target_resolution):
        """Get videos from cache that have the specified resolution"""
        query = """
        SELECT youtube_id, title, streams 
        FROM videos 
        WHERE streams IS NOT NULL AND streams != ''
        """
        
        results = self.video_table.execute(query)
        matching_videos = []
        
        for video_id, title, streams_json in results:
            try:
                if streams_json:
                    streams = json.loads(streams_json)
                    # Check if any stream matches the target resolution
                    for stream in streams:
                        if stream.get('height') == int(target_resolution):
                            matching_videos.append((video_id, title, streams_json))
                            break
            except (json.JSONDecodeError, ValueError):
                # Skip videos with invalid stream data
                continue
        
        return matching_videos

    def failed(self):
        """Redownload videos that previously failed to download"""
        print("Searching for failed video downloads...")
        
        # Query videos that are marked as inactive or have no media file
        query = """
        SELECT youtube_id, title 
        FROM videos 
        WHERE active = 0 OR media_url IS NULL OR media_url = ''
        """
        
        results = self.video_table.execute(query)
        
        if not results:
            print("No failed videos found.")
            return

        print(f"Found {len(results)} failed videos.")
        
        # Confirm before proceeding
        confirm = input(f"Do you want to redownload all {len(results)} failed videos? (y/N): ")
        if confirm.lower() not in ['y', 'yes']:
            print("Operation cancelled.")
            return

        # Redownload each failed video
        success_count = 0
        failed_count = 0
        
        for i, (video_id, title) in enumerate(results, 1):
            print(f"[{i}/{len(results)}] Redownloading failed: {title} ({video_id})")
            
            if self.client.redownload_video(video_id):
                success_count += 1
            else:
                failed_count += 1
                print(f"  ❌ Failed to queue {video_id}")
            
            # Add a small delay to avoid overwhelming the API
            time.sleep(0.5)

        print(f"\nRedownload Summary:")
        print(f"✅ Successfully queued: {success_count}")
        print(f"❌ Failed: {failed_count}")
        print(f"📥 Total videos processed: {len(results)}")
